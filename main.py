import os, sys
import utime
from machine import UART, Pin

print(os.uname())

# LED
led = machine.Pin(25, machine.Pin.OUT)
led.value(0)
utime.sleep(0.5)
led.value(1)

# UART
# uart = machine.UART(0, baudrate=115200, tx=Pin(0), rx=Pin(1))
uart = machine.UART(1, baudrate=115200, tx=Pin(8), rx=Pin(9))
print("UART Setting...")
print(uart)


# Functions
def sendCMD_waitResp(cmd, timeout=3000):
    print("CMD: " + cmd)
    uart.write(cmd)
    waitResp(timeout)
    print()


def waitResp(timeout=3000):
    prvMills = utime.ticks_ms()
    resp = b""
    while (utime.ticks_ms() - prvMills) < timeout:
        if uart.any():
            resp = b"".join([resp, uart.read(1)])
    print(resp.decode("utf-8"))


# AT command Test
sendCMD_waitResp("AT\r\n")  # AT
sendCMD_waitResp("AT+GMR\r\n")  # AT ver

utime.sleep(1)
# sendCMD_waitResp("AT+RST\r\n") #reset
sendCMD_waitResp("AT+CWMODE_CUR=1\r\n")  # Station Mode
sendCMD_waitResp("AT+CWDHCP_CUR=1,1\r\n")  # DHCP on

utime.sleep(1)
sendCMD_waitResp('AT+CWJAP_CUR="TP-Link_Guest_171C","stupavska"\r\n')  # AP connecting
sendCMD_waitResp("AT+CIPSTA_CUR?\r\n")  # network chk

# Get time
sendCMD_waitResp('AT+CIPSNTPCFG=1,0,"time.google.com"\r\n')     # 1 - enabled, 0 - timezone

while True:
    sendCMD_waitResp('AT+CIPSNTPTIME?\r\n')
    sendCMD_waitResp('AT+PING="www.google.com"\r\n')
    utime.sleep(3)
