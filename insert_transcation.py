# import pymysql
from datetime import datetime
from dateutil.relativedelta import relativedelta
import string
from random import choice
# from flask_mysqldb import MySQL
import os 

# Open database connection
# db = pymysql.connect("cloud-computing-db.cirxi9zqffnf.us-east-1.rds.amazonaws.com","admin1","MasterPwd11","mydb")


# myplan = "Gold"
# mycust_id = 1
mybilling_id = 1
def transaction(cursor,planId,mycust_id):
	# cursor = db.cursor()
	planId = str(planId)
	mycust_id = str(mycust_id)
	select_plan = "SELECT p_name, validity FROM plan where p_Id = %s"
	cursor.execute(select_plan, planId)
	myplan_details = cursor.fetchone()

	# print(myplan_details[0])
	# print("Plan id {} & Validity {} for {} Plan".format(myplan_id[0], myplan_id[1] ,myplan))


	mydate = datetime.date(datetime.now())
	date_after_month = datetime.date(datetime.now())+ relativedelta(months= myplan_details[1] )

	chars = string.digits
	random =  ''.join(choice(chars) for _ in range(4))

	# mybuck_name = "{}-{}-{}".format(myplan, random, mydate.strftime("%d%m%y"))
	# mybuck_name = str(mybuck_name)
	mybuck_name = mycust_id
	# print(mybuck_name)
	# print(date_after_month)

	# prepare a cursor object using cursor() method
	# cursor = db.cursor()



	# execute SQL query using execute() method.
	sql = "INSERT INTO transaction (customer_id, plan_id, tran_date, plan_exp_date, bucket_ref, billing_id) VALUES (%s, %s , %s, %s, %s, %s)"
	val = (mycust_id, planId, mydate, date_after_month, mybuck_name, mybilling_id )
	cursor.execute(sql, val)

	# db.commit() 
	# print(cursor.rowcount, "record inserted.")

# if cursor.rowcount ==1:
# 	parent_dir = "/mys3bucket"
# 	mode = 0o756
# 	path = os.path.join(parent_dir, mybuck_name)
# 	os.mkdir(path, mode) 
