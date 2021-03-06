from signal import signal, SIGTERM, SIGHUP, pause
from rpi_lcd import LCD
import time
import subprocess
import threading
from datetime import datetime
import paho.mqtt.client as mqtt
import random
import json

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
        """Return Raspberry Pi temp from lm_sensors output."""
        result = subprocess.check_output('sensors').decode('utf-8')
        for line in result.split('\n'):
            if 'temp1' in line:
                restemp = line.split('+')[1].split('°')
                return restemp[0]

    def get_ping(address, port):
        """Returns a string indicating server status from netcat response code."""
        response = subprocess.run(
            ['nc', '-vz', '-w', '5', address, str(port)], stderr=subprocess.DEVNULL).returncode
        if response == 0:
            return 'Online'
        else:
            return 'Offline'

    def get_ram():
        """Return a tuple with total memory and free memory."""
        result = subprocess.check_output(['free', '--mega']).decode('utf-8')
        for line in result.split('\n'):
            if 'Mem' in line:
                resmem = line.split()
                return (int(resmem[2]), int(resmem[1]))

    def get_time():
        """Returns current date and time.

        Example of formatting: 10:26 PM | Oct15
        """
        return datetime.now().strftime('%I:%M %p | %b%-d')

    def get_pic_count():
        """Returns number of timelapse pictures from directory."""
        result = subprocess.check_output(
            ['ls', '-1', '/mnt/dietpi_userdata/webcam']).decode('utf-8').count('\n')
        return result

    def get_ban_count():
        """Curls data from a web server.

        My use for this is to get the number of banned IPs from fail2ban on my own server.

        TODO: make this more flexible -- curl a file passed in via variable
        """
        try:
            result = subprocess.check_output(['curl', 'http://sleepyarchimedes.com:1234/files/scriptfiles/bancount.log',
                                             '--connect-timeout', '5'], stderr=subprocess.DEVNULL).decode('utf-8')
        except subprocess.CalledProcessError:
            result = 'Timed out'
        else:
            result = result[:-1] + ' addresses'
        return result


################
# server stuff #
################

broker = 'localhost'
port = 1883
topic = "arduino"
client_name = "local"

incomingJson = {}
dataAge = 1

def setup_mqtt():
    print("Starting MQTT subscription...")
    mqtt_client = mqtt.Client(client_name)
    mqtt_client.connect(broker)

    mqtt_client.loop_start()


    mqtt_client.subscribe(topic)
    mqtt_client.on_message = handle_telemetry

def handle_telemetry(client, userdata, message):
    payload = message.payload.decode()
    print("A message came in:", payload)
    global incomingJson
    incomingJson = json.loads(payload)
    global dataAge
    dataAge = 0
    
########
# main #
########
if __name__ == '__main__':
    serverThread = threading.Thread(target=setup_mqtt())
    serverThread.setDaemon(True)
    serverThread.start()
    try:
        signal(SIGTERM, safe_exit)
        signal(SIGHUP, safe_exit)
        print("Cycling through data...")
        time.sleep(2) # give time for mqtt subscription to kick in
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
                lcd.text('PiTemp   FreeMem', 1)
                freemem = DataGrab.get_ram()[1] - DataGrab.get_ram()[0]
                lcd.text(DataGrab.get_temp() + ' C     ' +
                         str(freemem) + 'MB', 2)
                time.sleep(1.5)

            for i in range(2):
                for i in range(3):
                    if dataAge == 0:
                        lcd.text('Living      Temp', 1)
                    else:
                        lcd.text('Living (!)  Temp', 1)
                    lcd.text('Room         ' + str(incomingJson.get("temp")) + "C", 2)
                    time.sleep(2)
                for i in range(3):
                    lcd.text('Humid      Press', 1)
                    lcd.text(str(incomingJson.get("humi")) + "%       " + str(incomingJson.get("pres")) + "kPa", 2)
                    time.sleep(2)
                    
            dataAge = dataAge + 1

            for i in range(5):
                lcd.text('Timelapse Count', 1)
                lcd.text(str(DataGrab.get_pic_count()) + ' images', 2)
                time.sleep(1.5)

    except KeyboardInterrupt:
        pass
    finally:
        lcd.clear()
