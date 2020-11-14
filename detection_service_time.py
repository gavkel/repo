import RPi.GPIO as GPIO
import schedule
import datetime
import time, datetime
import telepot
from telepot.loop import MessageLoop
import subprocess
import os

# create ALART_SET environment variable and set as 1 default
alarm_set = 1
# os.environ["ALARM_SET"] = "1"
now = datetime.datetime.now()

def command_received(msg):
    chat_id = msg['chat']['id']
    command = msg['text']
    # print 'Received: %s' % command
    if command == '/hi':
        telegram_bot.sendMessage(chat_id, str("Hi VillageFarm From Workshop"))
        # telegram_bot.sendPhoto (chat_id, photo = "http://www.freeimageslive.com/galleries/festive/easter/pics/sheep_and_lamb.jpg")
        # telegram_bot.sendDocument(chat_id, document=open('/home/pi/Aisha.py'))
        # telegram_bot.sendAudio(chat_id, audio=open('/home/pi/test.mp3'))
    elif command == '/time':
        telegram_bot.sendMessage(chat_id, str(now.hour)+str(":")+str(now.minute))
    elif command == '/alarmon':
        set_alarm_on()
        telegram_bot.sendMessage(chat_id, str("Alarm Manually Enabled In Workshop"))
    elif command == '/alarmoff':
        set_alarm_off()
        telegram_bot.sendMessage(chat_id, str("Alarm Manually Disabled In Workshop"))
    elif command == '/alarmstatus':
        global alarm_set
        if alarm_set == 1:
            # enabled
            telegram_bot.sendMessage(chat_id, str("Alarm On"))
        else:
            # disabled
            telegram_bot.sendMessage(chat_id, str("Alarm Off"))
    return

def is_time_between(begin_time, end_time, check_time=None):
    # If check time is not given, default to current UTC time
    check_time = check_time or datetime.utcnow().time()
    if begin_time < end_time:
        return check_time >= begin_time and check_time <= end_time
    else: # crosses midnight
        return check_time >= begin_time or check_time <= end_time

def set_alarm_on():
    global alarm_set
    # os.environ['ALARM_SET'] == '1'
    alarm_set = 1
    os.system("sudo -u pi sh /home/pi/telegram_send_message.sh 'Alarm Set In Workshop'")
    return

def set_alarm_off():
    global alarm_set
    #os.environ['ALARM_SET'] == '0'
    alarm_set = 0
    os.system("sudo -u pi sh /home/pi/telegram_send_message.sh 'Alarm Disabled In Workshop'")
    return

def heartbeat(t):
    # print "I'm working...", t
    # subprocess.Popen(["/home/pi/telegram_send_message.sh", "Heartbeat ", t])
    os.system("sudo -u pi sh /home/pi/telegram_send_message.sh 'Heartbeat In Workshop'")
    return

def detection_callback(channel):
    global alarm_set
    # print("Button was pushed!")
    # if os.environ['ALARM_SET'] == '1':
    if alarm_set == 1:
        time.sleep(1.5)  # confirm the movement by waiting 1.5 sec 
        if GPIO.input(8): # and check again the input
            # subprocess.Popen(["/home/pi/telegram_send_message.sh", "Detection"])
            os.system("sudo -u pi sh /home/pi/telegram_send_message.sh 'Detection In Workshop'")

            # stop detection for 10 sec
            GPIO.remove_event_detect(8)
            time.sleep(10)
            GPIO.add_event_detect(8, GPIO.RISING, callback=detection_callback, bouncetime=300)

    return

# setup telegram telebot events
telegram_bot = telepot.Bot('883023226:AAEBG4n9mNoWAPy7CpURyFxg3IKquAsqB28')
# print (telegram_bot.getMe())
MessageLoop(telegram_bot, command_received).run_as_thread()
# print 'Up and Running....'

# setup gpio and detection section
GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
GPIO.setup(8, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 8 to be an input pin and set initial value to be pulled low (off)

GPIO.add_event_detect(8, GPIO.RISING, callback=detection_callback, bouncetime=300) # Setup event on pin 8 rising edge

# enable alarm schedule
schedule.every().day.at("21:01").do(set_alarm_on)

# disable alarm schedule
schedule.every().day.at("06:44").do(set_alarm_off)
# schedule.every().day.at("12:30").do(set_alarm_off,'It is 12:30')

# schedule.run_pending()

# message = input("Press enter to quit\n\n") # Run until someone presses enter

while True:
    schedule.run_pending()
    time.sleep(1) # wait one sec

GPIO.cleanup() # Clean up
