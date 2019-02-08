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
neuropy = NeuroPy("COM4")
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
    return render_template("home.html")
@app.route("/salvador")
def salvador():
    return "Hello, Salvador"

@app.route('/reg',methods=['POST'])
def reg():
    
    p=False
    q=False
   
    try:
        # Open database connection
        connection = sqlite3.connect("myTable.db") 
        
        # prepare a cursor object using cursor() method
        cursor = connection.cursor()
       
        if request.method == 'POST':
            student_name=request.form['Name']
            student_id=request.form['email']
            password=request.form['Password']
            Repassword=request.form['confirm-password']
           
        if password == Repassword :
            q=True
            print("NIT")
        if q:
            sql_command = "INSERT INTO student VALUES ('"+ student_id +"','"+student_name+"','"+password+"');"
            print("INSERT INTO student VALUES ('"+ student_id +"','"+student_name+"','"+password+"');")
            # Execute the SQL command
            cursor.execute(sql_command)
            p=True
            print("NIT1")
    except:
        print ("Error: unable to fecth data")
    finally :
    # disconnect from server
        connection.commit()
        connection.close()
    if q:
        if p :
            print("NIT2")
            return render_template('videolist.html')
    else:
        return render_template('home.html')

@app.route('/videolist',methods=['POST'])
def login():
   
    p=False
    r=False
    q=False
    print(p)
    try:
        # Open database connection
        connection = sqlite3.connect("myTable.db") 

        # prepare a cursor object using cursor() method
        cursor = connection.cursor()
        print("NIT221")
        if request.method == 'POST':
            student_id=request.form['username']
            password=request.form['password']
            if student_id == "admin" and password == "admin" :
                q=True
                print(q)
            # sql = """SELECT * FROM student ;"""
        
            # Execute the SQL command
            cursor.execute("SELECT * FROM student")
            print("NIT22222")
            # Fetch all the rows in a list of lists.
            results = cursor.fetchall()
        
            for row in results:
                s_id = row[0]
                pass_word = row[1]
                if student_id == s_id and password == pass_word :
                    global user
                    user=student_id
                    print(user)
                    p=True
                    print("145214521")
            if p:
                cursor.execute("SELECT * FROM lecture where subject_name='ML'")
                data = cursor.fetchall()
                cursor.execute("SELECT * FROM lecture where subject_name='DS'")
                data1 = cursor.fetchall()
                cursor.execute("SELECT * FROM lecture where subject_name='AT'")
                data2 = cursor.fetchall()
                cursor.execute("SELECT * FROM lecture where subject_name='NS'")
                data3 = cursor.fetchall()
                r=True
                print("vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv")
                
    except:
        print ("Error: unable to fecth data")
    finally :
    # disconnect from server
        connection.commit()
        connection.close()
    
    if r :
        return render_template('videolist.html',data=data,data1=data1,data2=data2,data3=data3)
    elif q:
        return render_template('admin.html')
    else:
        return render_template('home.html')



@app.route('/upload_file', methods=['GET', 'POST'])
def upload_file():
    p=False
    try:
        # Open database connection
        connection = sqlite3.connect("myTable.db") 
        
        # prepare a cursor object using cursor() method
        cursor = connection.cursor()
        
        if request.method == 'POST':
            Prof_id=request.form['pid']
           
            name=request.form['pname']
            
            subject=request.form['subject']
            print("nit3")
            module=request.form['module']
            print("nit4")
            vno=request.form['vno']
            v_dis=request.form['v_dis']
            print("nit5")
            print("NIT")
            target=os.path.join(APP_ROOT,'static/upload/')
            print(target)
            if not os.path.isdir(target):
                os.mkdir(target)
            # check if the post request has the file part
            if 'file' not in request.files:
                print("NIT1")
                flash('No file part')
                return redirect(request.url)
           
            for file in request.files.getlist("file"):
                print("NIT3")
                #filename = request.files['file'].read()
                print("NIT4 " +file.filename)
                destination="/".join([target,file.filename])
                file.save(destination)
                sql_command = "INSERT INTO lecture VALUES ('"+ Prof_id+"','"+name+"','"+subject+"','"+v_dis+"',"+module+","+vno+",'"+file.filename+"');"
                #print("INSERT INTO lecture VALUES ('"+ Prof_id+"','"+name+"','"+subject+"',"+module+","+vno+",'"+file.filename+"');")
                # Execute the SQL command
                #sql_command = "INSERT INTO lecture VALUES ('10','vv','c',1,1,'"+file.filename+"');"
                cursor.execute(sql_command)
                p=True
    except:
        print ("Error: unable to fecth data")
    finally :
    # disconnect from server
        connection.commit()
        connection.close()
    if p :
        return render_template('videolist.html')
    else:
        return render_template('home.html')
               
@app.route('/display/<string:value>')
def display(value):
    # Get query_name from request
    print("BKP")
    connection = sqlite3.connect("myTable.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM lecture where lecture_add='"+value+"'")
    data = cursor.fetchall()
    #query = request.Get.get('value')
    print(data[0])
    print(user)
    return render_template('project.html',data=data,data1=data,results=user)


def hello():
    print("hello world")



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
    global counter,f
    counter=0
    f.close()
    print("Unsuccessful")
    print(counter)
    return 'welcome %s' % name
    
    

@app.route('/success/<name>')
def success(name):
    global counter
    counter = 0
    print('On Over')
    file_path="guru99.csv"
    fileExist =checkFileExistByOSPath(file_path)
    if(not fileExist):
        createNewFile(file_path)
    else:
        global f
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
              
              print("working for time",counter)
            
            #except KeyboardInterrupt:
              if(counter==0):
                  neuStop()
                  f.close()
                  print("Not working")
                  break
               
    
    
    return 'welcome %s' % name



if __name__ == "__main__":
    app.run(debug=True)
  
