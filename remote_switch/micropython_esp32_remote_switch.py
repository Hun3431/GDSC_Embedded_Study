# 참고자료 https://randomnerdtutorials.com/esp32-esp8266-micropython-web-server/

import time, json
from machine import Pin

try:
  import usocket as socket
except:
  import socket

from machine import Pin
import network

import esp
esp.osdebug(None)

import gc
gc.collect()

ssid = 'DoD_2.4G'
password = 'dod54321'

station = network.WLAN(network.STA_IF)

station.active(True)
station.connect(ssid, password)

while station.isconnected() == False:
  pass

print('Connection successful')
print(station.ifconfig())

led = Pin(10, Pin.OUT)
led.value(1)

btn = Pin(4, Pin.OUT)
power = Pin(5, Pin.IN)

def power_state():
  if power.value() == 1:
    gpio_state="ON"
  else:
    gpio_state="OFF"
  
  return gpio_state

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)

while True:
  conn, addr = s.accept()
  print('Got a connection from %s' % str(addr))
  request = conn.recv(1024)
  request = str(request)
  print('Content = %s' % request)
  
  start = request.find('/start')
  state = request.find('/state')
  
  if start == 6:
    print('Computer Start')
    btn.value(1)
    time.sleep(0.5)
    btn.value(0)
    time.sleep(0.5)
  elif state == 6:
    gpio_state = power_state()
    response = json.dumps({"state": gpio_state})
    
    conn.send('HTTP/1.1 200 OK\r\n')
    conn.send('Content-Type: application/json\r\n')
    conn.send('Access-Control-Allow-Origin: *\r')  # cors error
    conn.send(f'Content-Length: {len(response)}\r\n')
    conn.send('Connection: close\r\n')
    conn.send('\r\n')
    conn.sendall(response)
    
    conn.close()