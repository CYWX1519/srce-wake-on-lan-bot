import socket
import binascii
import re

'''
使用Python发送魔法数据包, 用以唤醒电脑。
1. 格式化mac地址 
2. 生成魔法唤醒包
3. 然后发送。
'''

MAC = "18:31:BF:B0:36:8F"

class WakeOnLan:
    def __init__(self) -> None:
        pass

    # 格式化MAC数据
    def format_mac(self, mac) -> str:
        mac_re = re.compile(r'''
                          (^([0-9A-F]{1,2}[-]){5}([0-9A-F]{1,2})$
                          |^([0-9A-F]{1,2}[:]){5}([0-9A-F]{1,2})$
                          |^([0-9A-F]{1,2}[.]){5}([0-9A-F]{1,2})$
                          )''', re.VERBOSE | re.IGNORECASE)
        if re.match(mac_re, mac):
            if mac.count(':') == 5 or mac.count('-') == 5 or mac.count('.'):
                sep = mac[2]
                mac_fm = mac.replace(sep, '')
                return mac_fm
        else:
            raise ValueError('Incorrect MAC format')
        
    # 使用binascii.unhexlify()方法创建唤醒包
    def create_magic_packet(self, mac) -> str:
        data = 'FF' * 6 + str(mac) * 16
        send_data = binascii.unhexlify(data)
        return send_data

    # 发送数据包
    def send_magic_packet(self, send_data) -> None:
        broadcast_address = '192.168.0.255'
        port = 9
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        s.sendto(send_data, (broadcast_address, port))

    def wakeonlan(self):
        mac = self.format_mac(MAC)
        send_data = self.create_magic_packet(mac)
        self.send_magic_packet(send_data)

if __name__ == '__main__':
    print("Running in single file...")
    wakeonlan = WakeOnLan()
    wakeonlan.wakeonlan()