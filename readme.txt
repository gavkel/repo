sudo apt-get update  
sudo apt-get install -y libreadline-dev libconfig-dev libssl-dev lua5.2 liblua5.2-dev libevent-dev libjansson-dev libssl1.0-dev
cd ~  
git clone --recursive https://github.com/vysheng/tg.git  
cd tg  
./configure
make  


sudo cp ~/tg/bin/telegram-cli /usr/bin  
sudo mkdir -p /etc/telegram-cli  
sudo mv ~/tg/tg-server.pub /etc/telegram-cli/server.pub


telegram-cli -W

msg @gavkel Hello again!
<msg> @gavkel Hello again!

rm -rf ~/.telegram-cli

telegram-cli -W -e "msg @gavkel hello from the command line"

import subprocess
subprocess.Popen(["/home/pi/telegram_send_message.sh", "hello world"])

#!/bin/bash
telegram-cli -W -e "msg @gavkel $1"

chmod ug+x telegram_send_message.sh

./telegram_send_message.sh "hello wold"

sh telegram_send_message.sh "hello wold"

sudo -u pi sh telegram_send_message.sh "Detection"
sudo -u pi sh /home/pi/telegram_send_message.sh "Detection"
sh chmod +x run.sh|./run.sh

@reboot sh /home/pi/launcher.sh >/home/pi/logs/cronlog 2>&1
*/1 * * * * www-data php5 /var/www/web/includes/crontab/queue_process.php >> /var/www/web/includes/crontab/queue.log 2>&1
*/1 * * * *          php5 /var/www/web/includes/crontab/queue_process.php >> /var/www/web/includes/crontab/queue.log 2>&1  

---

import RPi.GPIO as GPIO
import schedule
import time
import subprocess

def heartbeat(t):
    # print "I'm working...", t
	subprocess.Popen(["/home/pi/telegram_send_message.sh", "Heartbeat ", t])
    return

def detection_callback(channel):
    # print("Button was pushed!")
    subprocess.Popen(["/home/pi/telegram_send_message.sh", "Detection"])

# setup gpio and detection section
GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 10 to be an input pin and set initial value to be pulled low (off)

GPIO.add_event_detect(10,GPIO.RISING,callback=detection_callback) # Setup event on pin 10 rising edge

# setup heartbeat section
schedule.every().day.at("20:00").do(job,'It is 20:00')

# schedule.run_pending()

# message = input("Press enter to quit\n\n") # Run until someone presses enter

while True:
    schedule.run_pending()
    time.sleep(60) # wait one minute

GPIO.cleanup() # Clean up

export ALARM_SET=1

@reboot sh /home/pi/launcher.sh >/home/pi/logs/cronlog 2>&1

--