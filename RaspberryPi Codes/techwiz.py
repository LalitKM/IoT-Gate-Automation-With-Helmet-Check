import mysql.connector
from mysql.connector import Error
import serial
import RPi.GPIO as GPIO
import time
import os
import sys, traceback


ser = serial.Serial('/dev/ttyACM0', 9600)
mydb = mysql.connector.connect(
      host="192.168.137.197",
      user="jitu",
      passwd="root",
      database='iotdashb'  
    )

    #rfid ='C1:D4:H2:A2'

print(mydb)
mycursor = mydb.cursor()
print("\n***connection successful***")


  
def read_arduino():
    while True :
        try:
            data=str(ser.readline())
            data=data[:-2]
            print("fetched from arduino: ",data)
            check_rfid(data)
        except Exception as e:
            print(e)
            ser.close()
            print("connection is closed\n")
            break;

def opengate():
    print("opening gate")
    try:
                
                GPIO.setmode(GPIO.BOARD)
                GPIO.setup(40 , GPIO.OUT)
                GPIO.setup(38 , GPIO.OUT)
                
                print("open")
                GPIO.output(40,1)
                GPIO.output(38,0)
                time.sleep(12)
              
                print("close")
                GPIO.output(40,0)
                GPIO.output(38,1)
                time.sleep(12)
                GPIO.cleanup()

    except KeyboardInterrupt:
        print("\n\nShutdown requested...\n\nclosing serial port && cleaning GPIO pins\n")
        GPIO.cleanup()
    except Exception:
        traceback.print_exc(file=sys.stdout)
        GPIO.cleanup()
    
    
   

def check_rfid(rfid):
    mycursor.execute("SELECT name,veh_type,veh_no from register where rfid =%s",(rfid,))
    myresult = mycursor.fetchone()
    print(type(myresult))
    print("=================\n")
    print("Name : ",myresult[0])
    print("Vechile Type : ",myresult[1])
    print("Vechile Number : ",myresult[2])
    if(myresult):
        if(myresult[1]=='B'):
            #run image uploader
            cmd ="fswebcam -r 640x480 --jpeg 85 -D 1 testimage.jpg"
            os.system(cmd)
            cmd2 = "python3 publisher.py "+rfid
            os.system(cmd2)
            opengate()
            print("\nimage uploading")
        else:
            #just open the gate
            cmd2 = "python3 publisher.py "+rfid
            os.system(cmd2)
            opengate()
            print("\n gateopen() finished")
            
    sql = "INSERT INTO logbook (name, veh_no) VALUES (%s, %s)"
    val = (myresult[0], myresult[2])
    mycursor.execute(sql, val)    
    mydb.commit()
    print("\nDatabase updated")   



def main():
    try:
        #opengate()
        read_arduino()
    except KeyboardInterrupt:
        print "\n\nShutdown requested...\n\nclosing serial port && cleaning GPIO pins\n"
        GPIO.cleanup()
        ser.close()
    except Exception:
        traceback.print_exc(file=sys.stdout)
        GPIO.cleanup()
        ser.close()
    

if __name__ == "__main__":
    main()
