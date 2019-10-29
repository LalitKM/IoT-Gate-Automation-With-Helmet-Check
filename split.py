import cv2
import label_image
import mysql.connector
import os

remote_host = "pi@192.168.137.168 "
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
