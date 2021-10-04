from signal import signal, SIGTERM, SIGHUP, pause
from rpi_lcd import LCD
import time
import subprocess
import threading
import socket
from datetime import datetime


##########################
# no idea, but i need it #
##########################
lcd = LCD()
def safe_exit(signum, frame):
    exit(1)


#################
# Data Grabbers #
#################
class DataGrab():
  def get_temp():
    """Get raspi temp from sensors output."""
    result = subprocess.check_output('sensors').decode('utf-8')
    for line in result.split('\n'):
      if 'temp1' in line:
        restemp = line.split('+')[1].split('°')
        return restemp[0]

  def get_ping(address, port):
    """Grab server status from netcat response code."""
    response = subprocess.run(['nc', '-vz', '-w', '5', address, str(port)], stderr=subprocess.DEVNULL).returncode
    if response == 0:
      return 'Online'
    else:
      return 'Offline'

  def get_ram():
    """Get raspi free memory in megabytes."""
    result = subprocess.check_output(['free', '--mega']).decode('utf-8')
    for line in result.split('\n'):
      if 'Mem' in line: 
        resmem = line.split()
        return (int(resmem[2]), int(resmem[1]))

  def get_time():
    """Get date and time."""
    return datetime.now().strftime('%I:%M %p | %b%-d')
    
  def get_pic_count():
    """Get number of timelapse pictures from directory."""
    result = subprocess.check_output(['ls', '-1', '/mnt/dietpi_userdata/webcam']).decode('utf-8').count('\n')
    return result

  def get_ban_count():
    """Curl the number of banned clients in fail2ban from my server."""
    try:
      result = subprocess.check_output(['curl', 'http://sleepyarchimedes.com:1234/files/scriptfiles/bancount.log', '--connect-timeout', '5'], stderr=subprocess.DEVNULL).decode('utf-8')
    except subprocess.CalledProcessError:
      result = 'Timed out'
    else:
      result = result[:-1] + ' addresses'
    return result


################
# server stuff #
################

HOST = "100.64.3.3" 
RECV_PORT = 9999

class Server: 
  """Main class to handle connections."""

  def __init__(self):
    """Create socket for server use."""

    address_tuple = (HOST, RECV_PORT)
    self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.sock.bind(address_tuple)

  def run_server(self):
    self.sock.listen(20)
    print("Waiting...")
    while True:
      cli_sock, address = self.sock.accept()
      while True:
        data = cli_sock.recv(4096)
        if not data:
          # if there's no data...
          break
        else:
          print("client connection.")
          decoded = data.decode("ascii")
          print("Original data: " + decoded)

  def close_server(self):
    self.sock.close()
    print("Shutting down server and quitting...")


######## 
# main #
########
if __name__ == '__main__':
  server = Server()
  serverThread = threading.Thread(target=server.run_server)
  serverThread.setDaemon(True)
  serverThread.start()
  try:
      signal(SIGTERM, safe_exit)
      signal(SIGHUP, safe_exit)
      print("Beginning cycle...")
      while True:
        lcd.text('SleepyArchimedes', 1)
        lcd.text('Pinging...', 2)
        lcd.text(DataGrab.get_ping('sleepyarchimedes.com', 1234), 2)
        time.sleep(5)
        
        lcd.text('Banned IP count', 1)
        lcd.text('Curling...', 2)
        lcd.text(DataGrab.get_ban_count(), 2)
        time.sleep(5)

        for i in range(5):
          lcd.text('Time & Date', 1)
          lcd.text(DataGrab.get_time(), 2)
          time.sleep(1.5)
        
        for i in range(5):
            lcd.text('Temp     FreeMem',1)
            freemem = DataGrab.get_ram()[1] - DataGrab.get_ram()[0]
            lcd.text(DataGrab.get_temp() + ' C     ' + str(freemem) + 'MB',2)
            time.sleep(1.5)

        for i in range(5):
            lcd.text('Timelapse Count', 1)
            lcd.text(str(DataGrab.get_pic_count()) + ' images', 2)
            time.sleep(1.5)
        
        
  except KeyboardInterrupt:
      pass
  finally:
    server.close_server()
    lcd.clear()
