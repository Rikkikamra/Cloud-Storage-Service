from flask import Flask, render_template , request, session, url_for, Response
from flask_mysqldb import MySQL
from createBucket import createBucket
from datetime import datetime
from dateutil.relativedelta import relativedelta
import string
from random import choice
import logging
import boto3
from werkzeug.utils import secure_filename
from hurry.filesize import size


logging.basicConfig(filename='/CloudStorage/mylog.log',level=logging.DEBUG)

app = Flask(__name__)
app.secret_key = "CloudProject2020"

app.config['MYSQL_USER'] = 'admin1'
app.config['MYSQL_PASSWORD'] = 'MasterPwd11'
app.config['MYSQL_HOST'] = 'cloud-computing-db.cirxi9zqffnf.us-east-1.rds.amazonaws.com'
app.config['MYSQL_DB'] = 'mydb'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

@app.route('/')
def hello():
    session['logged']=0
    logging.debug("Home Page Loaded")
    return render_template("home.html")

@app.route('/press',methods=['GET','POST'])
def press():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        passwd = request.form['passwd']
        logging.debug("name: %s", name)
        try:
            cur = mysql.connection.cursor()
            sql = "INSERT INTO customer ( cust_name, email_id, Ph_no, cust_pwd) VALUES (%s, %s , %s, %s)"
            val = (name,email,phone,passwd)
            cur.execute(sql, val)
            mysql.connection.commit()
            cur.close()
            return render_template("home.html")
        except Exception as e:
            print("Couldn't insert into Db")
            print(e)
            return render_template("signup.html")

@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/signup')
def signup():
    return render_template("signup.html", db_values="123")

@app.route('/plans')
def plans():
    return render_template("plans.html")

@app.route('/fixed')
def fixed():
    return render_template("fixed.html")



@app.route('/check',methods=['GET','POST'])
def check():
    if request.method == 'POST':
        uname = request.form['username']
        passwd = request.form['passwd']
        logging.debug("name: %s", uname)
        try:
            cur = mysql.connection.cursor()
            sql = "SELECT custId from customer where email_id= %s and cust_pwd=%s"
            val = (uname,passwd)
            cur.execute(sql, val)
            logging.debug(sql)
            custId = cur.fetchall()
            mysql.connection.commit()
            cur.close()
            session['custId'] = custId[0]['custId']
            session['logged']=1
            return render_template("plans.html")
        except Exception as e:
            logging.debug("Login exception")
            print("Couldn't insert into Db")
            print(e)
            return render_template("login.html")

@app.route('/planSelect',methods=['GET','POST'])
def planSelect():
    planId = request.form['planId']
    sizeData = request.form['size']
    mybilling_id =1
    mycust_id = 0
    mycust_id += session['custId']
    logging.debug(planId)
    cur = mysql.connection.cursor()
    select_plan = "SELECT p_name, validity FROM plan where p_Id = %s"
    cur.execute(select_plan, planId)
    myplan_details = cur.fetchone()
    logging.debug(myplan_details['validity'])
    mydate = datetime.date(datetime.now())
    date_after_month = datetime.date(datetime.now())+ relativedelta(months= myplan_details['validity'] )
    chars = string.digits
    random =  ''.join(choice(chars) for _ in range(4))
    mybuck_name = mycust_id
    sql = "INSERT INTO transaction (customer_id, plan_id, tran_date, plan_exp_date, bucket_ref, billing_id, size) VALUES (%s, %s , %s, %s, %s, %s,%s)"
    val = (mycust_id, planId, mydate, date_after_month, mybuck_name, mybilling_id,sizeData )
    createBucket(mybuck_name)
    cur.execute(sql, val)
    mysql.connection.commit()
    cur.close()
    return render_template("home.html")

@app.route('/dashboard')
def dashboard():
    total_size=0
    s3 = boto3.resource('s3')
    mybucket = "datastorage-project"
    folder = "user/"+str(session['custId'])+"/"
    s3_bucket = s3.Bucket(mybucket)
    files_in_s3 = [f.key.split(folder)[1] for f in s3_bucket.objects.filter(Prefix=folder).all()]
    lengthLoop = len(files_in_s3)
    for k in s3_bucket.objects.filter(Prefix=folder).all():
        total_size += k.size
    total_size = size(total_size)

    return render_template("dashboard.html",total_size=total_size,files_in_s3=files_in_s3,lengthLoop=lengthLoop)

@app.route('/fileUpload',methods=['GET','POST'])
def fileUpload():
    uploadFile = request.files['file']
    fileName = secure_filename(uploadFile.filename)
    s3 = boto3.resource('s3')
    file_name ="user/"+str(session['custId'])+"/"+fileName
    s3.Bucket('datastorage-project').put_object(Key=file_name, Body=uploadFile)

    logging.debug("uploaded file for testing")
    logging.debug("Checking for the bucket list")
    mybucket = "datastorage-project"
    folder = "user/"+str(session['custId'])+"/"
    s3_bucket = s3.Bucket(mybucket)
    files_in_s3 = [f.key.split(folder)[1] for f in s3_bucket.objects.filter(Prefix=folder).all()]
    logging.debug("the list of files inside the folder")
    logging.debug(files_in_s3)
    total_size=0
    for k in s3_bucket.objects.filter(Prefix=folder).all():
        total_size += k.size
    total_size = size(total_size)
    lengthLoop = len(files_in_s3)
        

    return render_template("dashboard.html",total_size=total_size,files_in_s3 = files_in_s3,lengthLoop=lengthLoop  )

@app.route('/fileAction',methods=['GET','POST'])
def fileAction():
    fileName = request.form['fileName']
    btnClick = request.form['btnClick']
    fileLoc = "user/"+str(session['custId'])+"/"+fileName
    if btnClick=="Download":
        s3 = boto3.client('s3')
        file = s3.get_object(Bucket='datastorage-project', Key=fileLoc)
        return Response(
            file['Body'].read(),
            mimetype='text/plain',
            headers={"Content-Disposition": "attachment;filename="+fileName}
        )
    if btnClick=="Delete":
        s3 = boto3.resource('s3')
        s3.Object('datastorage-project',fileLoc).delete()
        return render_template("home.html")

    

@app.route('/logout')
def logout():
    session['custId']=0
    session['logged']=0
    return render_template("home.html")

if __name__ == '__main__':
	app.run(debug= True)

