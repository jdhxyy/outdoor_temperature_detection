"""
Copyright 2021-2021 The jdh99 Authors. All rights reserved.
室外温度检测服务
Authors: jdh99 <jdh821@163.com>
"""

import tziot
import time
import machine, onewire, ds18x20

# 本节点地址和密码
IA = 0x2141000000010001
PWD =

# WIFI账号密码
WIFI_SSID = 'JDHOME_MASTER'
WIFI_PWD =

# 服务号
# 读取温度
RID_GET_TEMP = 1

# 温度传感器
ds_sensor = 0
rom = None

# 当前温度.分度0.1摄氏度
temp_now = 0


def main():
    # 初始化温度传感器
    init_temp_sensor()
    # 连接wifi
    connect_wifi()

    tziot.bind_pipe_net(IA, PWD, '0.0.0.0', 12025)
    tziot.register(RID_GET_TEMP, get_temp_service)
    tziot.run(app)


def init_temp_sensor():
    global ds_sensor, rom

    ds_pin = machine.Pin(4)
    ds_sensor = ds18x20.DS18X20(onewire.OneWire(ds_pin))
    roms = ds_sensor.scan()
    print('Found DS devices: ', roms)
    if len(roms) == 0:
        # 检测不到温度传感器则复位
        time.sleep(10)
        machine.reset()
    rom = roms[0]


def connect_wifi():
    print('connect wifi')
    ok = tziot.connect_wifi(WIFI_SSID, WIFI_PWD)
    if ok is False:
        print('connect wifi failed')
        machine.reset()
    print('connect wlan success')


def get_temp_service(pipe: int, src_ia: int, req: bytearray) -> (bytearray, int):
    """读取温度服务"""
    global temp_now
    print('src ia=0x%x' % src_ia)

    data = bytearray()
    data.append((temp_now >> 8) & 0xff)
    data.append(temp_now & 0xff)
    return data, 0


def app():
    """业务程序.每10s检测一次温度"""
    global ds_sensor, rom, temp_now

    run_time = 0
    while True:
        ds_sensor.convert_temp()
        time.sleep(1)
        temp_now = int(ds_sensor.read_temp(rom) * 10)
        print('temp:', temp_now)

        # 转换成int8
        if temp_now < 0:
            temp_now = 0x10000 + temp_now

        time.sleep(10)

        # 每半小时定时复位
        run_time += 10
        if run_time >= 1800:
            print('reset system!')
            machine.reset()


if __name__ == '__main__':
    main()
