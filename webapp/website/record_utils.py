import psycopg2
from datetime import date
from datetime import timedelta
from datetime import datetime

def record_intake(user_id,location, name, result):
	conn = psycopg2.connect(
	    host="ec2-52-86-123-180.compute-1.amazonaws.com",
	    port="5432",
	    database="d2o2cbpkkb06fc",
	    user="zunhwbfmndzghr",
	    password="97e2dd8a68587ef47ecc4ced5b9137bf7ab6daadada6757c028cf96b81c8ac3b"
	)

	cursor=conn.cursor()
	cursor.execute("insert into records (user_id, date, location, name, result) values('{}','{}','{}','{}','{}')".format(user_id,date.today(),location, name, result))
	conn.commit()
	cursor.close()

def get_past_intake_days(user_id,day=1,end_date=''):
	day=int(day)
	if(len(end_date)!=0):
		end_date=datetime.strptime(end_date,'%B %d, %Y')
	else:
		end_date=date.today()
	target_date=end_date-timedelta(days = day)

	response={}
	keys=["date", "location", "name", "result"]
	conn = psycopg2.connect(
	    host="ec2-52-86-123-180.compute-1.amazonaws.com",
	    port="5432",
	    database="d2o2cbpkkb06fc",
	    user="zunhwbfmndzghr",
	    password="97e2dd8a68587ef47ecc4ced5b9137bf7ab6daadada6757c028cf96b81c8ac3b"
	)

	cursor=conn.cursor()
	cursor.execute("select {} from records where user_id like '{}' and date > '{}' and date <= '{}' order by date desc".format(",".join(keys),user_id,target_date,end_date))
	entries=cursor.fetchall()
	conn.commit()
	cursor.close()

	response={
		"entries":len(entries),
		"date":[i[0] for i in entries],
		"location":[i[1] for i in entries],
		"name":[i[2] for i in entries],
		"result":[i[3] for i in entries],
		"data":[
			dict(zip(keys,i)) for i in entries
		]
	}
	return response

# record_intake(27, "home", "aaa", "positive")