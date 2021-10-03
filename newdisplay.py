from signal import signal, SIGTERM, SIGHUP, pause
from rpi_lcd import LCD
import time
import subprocess
from datetime import datetime

# custom funcs
def get_temp():
  result = subprocess.check_output('sensors').decode('utf-8')
  for line in result.split('\n'):
    if 'temp1' in line:
      restemp = line.split('+')[1].split('°')
      return restemp[0]

def get_ping(address, port):
  response = subprocess.run(['nc', '-vz', '-w', '5', address, str(port)]).returncode
  if response == 0:
    return 'Online'
  else:
    return 'Offline'

def get_ram(): 
  result = subprocess.check_output(['free', '--mega']).decode('utf-8')
  for line in result.split('\n'):
    if 'Mem' in line: 
      resmem = line.split()
      return (int(resmem[2]), int(resmem[1]))

def get_time():
  return datetime.now().strftime('%I:%M %p | %b%-d')
  
def get_pic_count():
  result = subprocess.check_output(['ls', '-1', '/mnt/dietpi_userdata/webcam']).decode('utf-8').count('\n')
  return result

def get_ban_count():
  try:
    result = subprocess.check_output(['curl', 'http://sleepyarchimedes.com:1234/files/scriptfiles/bancount.log', '--connect-timeout', '5']).decode('utf-8')
  except subprocess.CalledProcessError:
    result = 'Timed out'
  else:
    result = result[:-1] + ' addresses'
  return result

# custom funcs
def get_temp():
  result = subprocess.check_output('sensors').decode('utf-8')
  for line in result.split('\n'):
    if 'temp1' in line:
      restemp = line.split('+')[1].split('°')
      return restemp[0]

def get_ping(address, port):
  response = subprocess.run(['nc', '-vz', '-w', '5', address, str(port)]).returncode
  if response == 0:
    return 'Online'
  else:
    return 'Offline'

def get_ram(): 
  result = subprocess.check_output(['free', '--mega']).decode('utf-8')
  for line in result.split('\n'):
    if 'Mem' in line: 
      resmem = line.split()
      return (int(resmem[2]), int(resmem[1]))

def get_time():
  return datetime.now().strftime('%I:%M %p | %b%-d')
  
def get_pic_count():
  result = subprocess.check_output(['ls', '-1', '/mnt/dietpi_userdata/webcam']).decode('utf-8').count('\n')
  return result

def get_ban_count():
  try:
    result = subprocess.check_output(['curl', 'http://sleepyarchimedes.com:1234/files/scriptfiles/bancount.log', '--connect-timeout', '5']).decode('utf-8')
  except subprocess.CalledProcessError:
    result = 'Timed out'
  else:
    result = result[:-1] + ' addresses'
  return result
lcd = LCD()
def safe_exit(signum, frame):
    exit(1)
# main
try:
    signal(SIGTERM, safe_exit)
    signal(SIGHUP, safe_exit)
    lcd.backlight_enabled = False
    while True:
      lcd.text('SleepyArchimedes', 1)
      lcd.text('Pinging...', 2)
      lcd.text(get_ping('sleepyarchimedes.com', 1234), 2)
      time.sleep(5)
      
      lcd.text('Banned IP count', 1)
      lcd.text('curling...', 2)
      lcd.text(get_ban_count(), 2)
      time.sleep(5)

      for i in range(5):
          lcd.text('Time & Date', 1)
          lcd.text(get_time(), 2)
          time.sleep(1.5)
      
      for i in range(5):
          freemem = get_ram()[1] - get_ram()[0]
          lcd.text('Temp     FreeMem',1)
          lcd.text(get_temp() + ' C     ' + str(freemem) + 'MB',2)
          time.sleep(1.5)

      for i in range(5):
          lcd.text('Timelapse Count', 1)
          lcd.text(str(get_pic_count()) + ' images', 2)
          time.sleep(1.5)
      
      
except KeyboardInterrupt:
    pass
finally:
    lcd.clear()

# data grabbing

