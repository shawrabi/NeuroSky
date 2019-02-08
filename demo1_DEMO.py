from flask import Flask,render_template,request,url_for
from NeuroPy import NeuroPy
import errno
from time import sleep
import csv
import os
import errno
from flask import flash, redirect
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash
import pyodbc 
#import time
import sqlite3 
import wtforms as wtf
import os
counter=0
neuropy = NeuroPy("COM3")
user="NULL"

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

def open_db():
    # Open database connection
    connection = sqlite3.connect("myTable.db") 

    # prepare a cursor object using cursor() method
    cursor = connection.cursor()





app = Flask(__name__)
APP_ROOT=os.path.dirname(os.path.abspath(__file__))
@app.route("/")
def home():
    return render_template("project_DEMO.html")




def checkFileExistByOSPath(file_path):

    ret = False
    # If this file object exist.
    if(os.path.exists(file_path)):
        ret = True
        print(file_path + " exist.")
        # If this is a file.
        if(os.path.isfile(file_path)):
            print(" and it is a file.")
        # This is a directory.    
        else:
            print(" and it is a directory.")
    else:
        ret = False
        print(file_path + " do not exist.")
        
    return ret

def createNewFile(file_path):
    f = open(file_path, 'wb')
    writer = csv.writer(f)
    writer.writerow(['attention','meditation','rawValue','delta','theta','lowAlpha','highAlpha','lowBeta','highBeta','lowGamma','midGamma','blinkStrength','poor signal'])

def neuStart():
    neuropy.start()
def neuStop():
    print("exiting!")
    neuropy.stop()


@app.route('/Unsuccess/<name>')
def Unsuccess(name):
    global counter
    counter=0
    print("NIT")
    return 'welcome %s' % name
    

@app.route('/success/<name>')
def success(name):
    global counter
    print('On Over')
    file_path="guru99.csv"
    fileExist =checkFileExistByOSPath(file_path)
    if(not fileExist):
        createNewFile(file_path)
    else:
        f= open("guru99.csv","wb")
    #if( success.counter != 0):
       
    neuStart()
    counter +=1
    print("started writing!")
    #print("press ctrl+c when u r done with the video")
    sleep(1)

    with f:
        writer = csv.writer(f)
        
        while (counter):
            #try:        
              m = neuropy.meditation
              a = neuropy.attention
              r = neuropy.rawValue
              d = neuropy.delta
              t = neuropy.theta
              la = neuropy.lowAlpha
              ha = neuropy.highAlpha
              lb = neuropy.lowBeta
              hb = neuropy.highBeta
              lg = neuropy.lowGamma
              mg = neuropy.midGamma
              bs = neuropy.blinkStrength
              s = neuropy.poorSignal
              writer.writerow([a,m,d,t,la,ha,lb,hb,lg,mg,bs,s]); 
              sleep(1) # sleep for 1s
              
              print("working",counter)
            
            #except KeyboardInterrupt:
              if(counter==0):
                  neuStop()
                  f.close()
                  print("Not working")
                  break
               
    
    
    return 'welcome %s' % name



if __name__ == "__main__":
    app.run(debug=True)
  
