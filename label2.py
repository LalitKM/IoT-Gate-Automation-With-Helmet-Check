import cv2
import label_image
import mysql.connector
import os
import paho.mqtt.client as mqtt

size = 4

def storeimage():

    db = mysql.connector.connect(user='root', password='',
                                  host='localhost',
                                  database='iotdashb')

    blob_value = open('testimage.jpg', 'rb').read()
    sql = 'INSERT INTO helmet(image) VALUES(%s)'
    args = (blob_value, )
    cursor=db.cursor()
    cursor.execute(sql,args)
    print("Success")
    db.commit()
    db.close()

def on_connect(client, userdata, flags, rc):
  print("Connected with result code "+str(rc))
  client.subscribe("inTopic")

def on_message(client, userdata, msg):
  if(msg.payload.decode()=='uploaded'):
      print("recieved")
      remote_host = "pi@192.168.137.223"
      img_loc = "/home/pi/Downloads/testimage.jpg"
      my_loc = "D:/IoTProject/finalfol/"
      os.system('pscp -pw raspberry "%s:%s" "%s"'%(remote_host,img_loc,my_loc))
      print("file fetched")
      im = cv2.imread("testimage.jpg")
      im=cv2.flip(im,1,0) 
      mini = cv2.resize(im, (int(im.shape[1]/size), int(im.shape[0]/size)))
      FaceFileName = "testimage.jpg"
      text = label_image.main(FaceFileName)
      if text == "nohelmet":
          storeimage()


client = mqtt.Client()
client.connect("localhost",1883,60)

client.on_connect = on_connect
client.on_message = on_message
client.loop_forever()


