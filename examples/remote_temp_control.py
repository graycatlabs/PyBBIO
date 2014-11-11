'''
 remote_temp_control.py   
 Rekha Seethamraju  

 An example to demonstrate the use of PyBBIO to control room temperature   
 remotely with the help of a fan and heater.  
 
 This example uses leds to depict a fan and a heater.  
 The temperature sensor used is a ADT7310. 
 Below 18 C, heater is switched ON. Above 25, fan os switched ON.
 It sends an email if temperature is above critical temperature (40 C).
 
 Working video : Coming soon
 
 This example program is in the public domain.  
'''
from bbio import *
from bbio.libraries.ADT7310 import *
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

adt = ADT7310(0,0)
#critical pin
pinc = GPIO1_18
heaterled = GPIO1_28
fanled = GPIO3_17
# sender == sender email address
# reciever == recipient's email address
sender = "sender@email.com"
reciever = "reciever@email.com"


def criticalalarm():
  text = "Temperature is too high and not controllable.\n \
            Check controls.\n"
  sendmsg(text)     

def sendmsg(message):
  print "Sending email notifcation"
  text = message
  msg = MIMEMultipart('alternative')
  msg['Subject'] = "Beaglebone Temperature Control"
  msg['From'] = sender
  msg['To'] = reciever
  msg.attach(MIMEText(text, 'plain'))
  server = smtplib.SMTP("smtp.gmail.com", 587)
  server.starttls()
  server.login(sender,'password')
  server.sendmail(sender, reciever, msg.as_string())
  print "send"
  

def setup():
  #sets low temperature threshold
  adt.setLowTemp(18)
  #sets high temperature threshold
  adt.setHighTemp(25)
  #sets critical temperature threshold
  adt.setCriticalTemp(40)
  #sets the function to call when interrupt pin in active.
  adt.setCriticalAlarm(pinc,criticalalarm)
  pinMode(heaterled,OUTPUT)
  pinMode(fanled,OUTPUT)
  digitalWrite(heaterled,LOW)
  digitalWrite(fanled,LOW)
  
def loop():
  temp = adt.getTemp()
  
  if (temp <= 18):
    digitalWrite(heaterled,HIGH)
    digitalWrite(fanled,LOW)

  elif (temp > 18 and temp <= 25 ):
    digitalWrite(heaterled,LOW)
    digitalWrite(fanled,LOW)
  
  elif(temp > 25):
    digitalWrite(heaterled,LOW)
    digitalWrite(fanled,HIGH)
    
  delay(5000)
  
run(setup,loop)
    