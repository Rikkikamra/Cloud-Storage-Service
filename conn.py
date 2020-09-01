#!/usr/bin/python3

import pymysql

# Open database connection
db = pymysql.connect("cloud-computing-db.cirxi9zqffnf.us-east-1.rds.amazonaws.com","admin1","MasterPwd11","mydb")

# prepare a cursor object using cursor() method
cursor = db.cursor()

# execute SQL query using execute() method.
cursor.execute("SELECT * FROM plan")

# Fetch a single row using fetchone() method.
data = cursor.fetchall()
for x in data:
	print (x)

# disconnect from server

# cur = mysql.connection.cursor()

sql = "INSERT INTO customer ( cust_name, email_id, Ph_no, cust_pwd) VALUES (%s, %s , %s, %s)"
val = ("Karishma","kk@gmail.com",4584348,"Kc123")
cursor.execute(sql, val)
cursor.commit()
cursor.close()
db.close()
