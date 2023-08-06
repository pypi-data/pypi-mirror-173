import math
import time
from pymavlink import mavutil

class drone:
    def __init__(self, connection=None, simulation=False, detailed=False):
        """
            * ``connection``- Belirlenen baglanti protokolu ile baglanmanizi saglar. Bos birakilirsa baglanti otomatik yapilir (default None)
            * ``simulation``- (Default False) IHA'nin simulasyon ortami icin mi pixhawka baglanmak icin mi hazirlanacagini
            belirler. Eger connection girildiyse burasi anlamsizdir. (default False)
                `True`: IHA simulasyon ortami icin hazirlanir.
                `False`: IHA pixhawk ile baglanti kurar.
            * ``detailed``- Debug amacli. Bilgilendirme mesajlari daha detayi belirlenir. (default False)
                `True`: Bilgilendirme mesajlarindaki detay artar.
                `False`: Normal bilgilendirme mesajlari alinir.
        """
        self.detailed = detailed
        
        if connection:
            self.connection = connection
        elif simulation:
            self.connection = mavutil.mavlink_connection("127.0.0.1:14550")
            self.connection.wait_heartbeat()
            print('IHA SIMULASYON ORTAMINA HAZIR')
        else:
            self.connection = mavutil.mavlink_connection("/dev/serial0", baudrate=57600)
            self.connection.wait_heartbeat()
            print('IHA PIXHAWKA BAGLANDI\n')

    def __detail(self, message):
        if self.detailed: print(message)

    def __resultMessage(self, command, success=True, failReason="BILINMEYEN BIR HATA"):
        if success:
            print(command, "KOMUTU ICRA EDILDI\n")
        else:
            print(command, "KOMUTU", failReason, "NEDENIYLE ICRA EDILEMEDI\n")

    def arm_only(self):
        """
            IHA'yi arm eder.
        """

        print("\nARM KOMUTU ALINDI")

        self.__detail("\ARM SINYALI GONDERILIYOR")
        self.connection.mav.command_long_send(self.connection.target_system,
            self.connection.target_component,
            mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM, 0, 1, 0, 0, 0, 0, 0, 0)
        self.__detail("\tARM SINYALI GONDERILDI\n")

        print("\tARAÇ ARM EDILIYOR")
        self.connection.motors_armed_wait()
        print("\tARAÇ ARM EDILDI")

        self.__resultMessage("ARM")

    def arm_and_takeoff(self, targetAltitude):
        """
            IHA arm edilir ve istenilen yukseklige ulasmak uzere kalkisa gecer. Yeterince
            yukselene kadar program bloklanir. 

            * ``targetAltitude``- IHA'nin metre cinsinden yukselmesi istenilen yukseklik.
        """
        
        print("\nTAKEOFF KOMUTU ALINDI: HEDEF_YÜKSEKLİK=%d Metre" %(targetAltitude))
        
        self.arm_only()

        self.__detail("\tTAKEOFF SINYALI GONDERILIYOR")
        self.connection.mav.command_long_send(self.connection.target_system,
            self.connection.target_component,
            mavutil.mavlink.MAV_CMD_NAV_TAKEOFF, 0, 0, 0, 0, 0, 0, 0, targetAltitude)
        self.__detail("\tTAKEOFF SINYALI GONDERILDI")

        print("\tARAÇ YÜKSELİYOR")
        while 1:
            msg = self.connection.recv_match(
                type='LOCAL_POSITION_NED', blocking=True)
            print('\t\tYUKSEKLIK: %f metre' %(-msg.z))
            if -msg.z > targetAltitude * 0.98:
                break
        print('\tHEDEF YÜKSEKLİĞE ULAŞILDI')

        self.__resultMessage("TAKEOFF")

    def changeVehicleMode(self, mode : str):
        """
            IHA'nin istenilen moda gecirilmesini saglar. Moda gecilene kadar program bloklanir.
            Eger istenilen mod gecerli degilse hata mesaji dondurur.

            * ``mode``- Gecis yapilacak mod
        """

        print("\nMOD DEGISTIRME KOMUTU ALINDI: HEDEF MOD=\"%s\"" %(mode))

        if mode not in self.connection.mode_mapping():
            print("BILINMEYEN MOD : {}".format(mode))
            print("UYGUN MODLAR : ", list(self.connection.mode_mapping().keys()))
            self.__resultMessage("MOD DEGISTIRME", success=False, failReason="BILINMEYEN MOD")
            return

        mode_id = self.connection.mode_mapping()[mode]
        self.__detail("\tMOD DEGISTIRME SINYALI GONDERILIYOR")
        self.connection.set_mode(mode_id)
        self.__detail("\tMOD DEGISTIRME SINYALI GONDERILDI")

        print("\tMOD DEGISIMI BEKLENIYOR")
        while True:
            ack_msg = self.connection.recv_match(type="COMMAND_ACK", blocking=True)
            ack_msg = ack_msg.to_dict()

            if ack_msg["command"] != mavutil.mavlink.MAV_CMD_DO_SET_MODE:
                continue

            self.__detail(mavutil.mavlink.enums["MAV_RESULT"][ack_msg["result"]].description)
            print("\tMOD DEGISTIRILDI YENI MOD:\"%s\"" %(mode))

            break

        self.__resultMessage("MOD DEGISTIRME")

    def immadiateLanding(self):
        """
            Ani inis modu. IHA inise zorlanir, inis yapilana kadar program bloklanir.        
        """

        print("\nACIL INIS KOMUTU ALINDI")

        self.changeVehicleMode("LAND")

        print("\tIHA INISE GECIYOR")
        while 1:
            msg = self.connection.recv_match(
                type='LOCAL_POSITION_NED', blocking=True)
            print('\t\tYUKSEKLIK: %f metre' %(-msg.z))
            if -msg.z > 0.1:
                break
        print('\tIHA BASARIYLA INIS YAPTI')
        
        self.__resultMessage("ACIL INIS")

    def move(self, x, y, z, vx=0, vy=0, vz=0, afx=0, afy=0, afz=0, yaw=0, yaw_rate=0, coordinate_frame=mavutil.mavlink.MAV_FRAME_LOCAL_NED, type_mask=int(0b110111111000)):
        """
            Istenilen koordinatlara gidilmesini saglar. Noktaya ulasana kadar program bloklanir.

            * ``x, y, z``- Gidilecek koordinatlar
            * ``vx, vy, vz``- Hizlar
            * ``afx, afy, afz``- Ivmeler
            * ``yaw``- Donus hizi
            * ``yaw_rate``- Donus frekansi
            * ``coordinate_frame``- Koordinatlarin tipi (global veya yerel koordinatlar gibi)
        """

        print('\nMOVE KOMUTU ALINDI')
        
        self.__detail('MOVE SINYALI GONDERILIYOR')
        self.connection.mav.send(mavutil.mavlink.MAVLink_set_position_target_local_ned_message(10, self.connection.target_system, self.connection.target_component,
            coordinate_frame, type_mask,
            x, y, z, #konum
            vx, vy, vz, #hiz
            afx, afy, afz, #ivme
            yaw, yaw_rate)) #yaw
        self.__detail('MOVE SINYALI GONDERILDI')

        print('\tIHA YOLA CIKIYOR')
        while 1:
            msg = self.connection.recv_match(
                type='LOCAL_POSITION_NED', blocking=True)

            distance = math.sqrt((msg.x - x) ** 2 + (msg.y - y) ** 2 + (msg.z - z) ** 2)
            print('\t\tKONUM: { x : %f, y : %f, z : %f } : HEDEFE UZAKLIK : %f' %(msg.x, msg.y, msg.z, distance))
            if distance < 0.1:
                print('\tHEDEFE ULASILDI')
                break

        self.__resultMessage('MOVE')

    def rotate(self, angle, angular_speed=25, direction=1, relative=1):
        """
            * ``angle``- Donulmesi istenilen aci degeri
            * ``angular_speed``- Acisal hiz
            * ``direction``-
                `1`: Saat yonu
                `-1`: Saat yonunun tersi
            * ``relative``-
                `0`: Mutlak aci
                `1`: Bagli aci
        """
        
        if direction:   print('\nROTATE KOMUTU ALINDI: %d DERECE SAAT YONUNDE DONULUYOR' %(angle))
        else:           print('\nROTATE KOMUTU ALINDI: %d DERECE SAAT YONUNUN TERSINE DONULUYOR' %(angle))
        
        self.__detail('ROTATE SINYALI GONDERILIYOR')
        self.connection.mav.command_long_send(self.connection.target_system,
            self.connection.target_component,
            mavutil.mavlink.MAV_CMD_CONDITION_YAW, 0,
            angle, angular_speed, direction, relative,
            0, 0, 0)
        self.__detail('ROTATE SINYALI GONDERILDI')

        print('\tIHA DONUSE BASLIYOR')
        
        for i in range(3, 0, -1):
            print('\t\tGERI SAYIM, %d' %(i))
            time.sleep(1)

        while 1:
            msg = self.connection.recv_match(
                type='ATTITUDE', blocking=True)

            print('\t\tDONUS HIZI: %f' %(msg.yawspeed))
            if abs(msg.yawspeed) < 0.01:
                print('\tDONUS TAMAMLANDI')
                break

        self.__resultMessage('ROTATE')

