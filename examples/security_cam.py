"""
 security_cam.py 
 Rekha Seethamraju

 An example to demonstrate the use of the WebCam and MMA7660 libraries of PyBBIO 
 to set up a security camera that takes a picture and sends an email and sms if 
 a motion is detected (pir motion sensor) or the camera is tampered with (MMA7660)

 This example program is in the public domain.
"""
from bbio import *
import smtplib
from bbio.libraries.WebCam import WebCam
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from bbio.libraries.MMA7660 import MMA7660

cam = WebCam()
pir = GPIO1_28
accel = MMA7660(2)
INT_PIN = GPIO1_16
sender = 'sender_email@gmail.com'
reciever = 'reciver_emial@gmail.com'
password = 'sender_email_password'
#change the smtp address below if not using gmail
sms = 'sms_gateway_address' 
# can be obtained from http://www.ukrainecalling.com/email-to-text.aspx

def setup():
  int_cfg = accel.INT_SHX | \
            accel.INT_SHY | \
            accel.INT_SHZ
  accel.setInterrupt(int_cfg, INT_PIN, accelCallback)
  accel.settapthreshold(30)
  accel.setTapDebounce(15)
  pinMode(pir,INPUT,PULLUP)
  attachInterrupt(pir, motiondetect, RISING)

def loop():
  print "The loop continues..."
  delay(1000)

def accelCallback(back_front, portrait_landscape, tap, shake):
  '''
  detects shake interrupt
  '''
  print "shake detected"
  cam.takeSnapshot("sample")
  if shake == 1:
    sendmsg(1)
    
def motiondetect():
  '''
  motion detect interrupt function
  '''
  print "motion detected"
  cam.takeSnapshot("sample")
  sendmsg(2)
  
def sendmsg(num):
  '''
  sends an email and sms with the picture
  '''
  if num == 1:
    text = "Shake Detected"
  if num == 2:
    text = "Motion Detected"
  print "Sending email notifcation"
  msg = MIMEMultipart()
  msg['Subject'] = "Beaglebone Remote Security"
  msg['From'] = sender
  msg['To'] = reciever
  msg.attach(MIMEText(text, 'plain'))
  img = open("sample.jpeg", "rb")
  msg.attach(MIMEImage(img.read()))
  img.close()
  # if not using gmail smtp adress has to change
  server = smtplib.SMTP("smtp.gmail.com", 587)
  server.starttls()
  server.login(sender,password)
  server.sendmail(sender, reciever, msg.as_string())
  server.sendmail(sender, sms, msg.as_string())
  print "sent email"
  
run(setup,loop)