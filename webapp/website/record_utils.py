import psycopg2
from datetime import date
from datetime import timedelta
from datetime import datetime

def record_intake(user_id,food_name,calorie,carb,fat,protein,sodium):
	conn = psycopg2.connect(
	    host="ec2-52-86-123-180.compute-1.amazonaws.com",
	    port="5432",
	    database="d2o2cbpkkb06fc",
	    user="zunhwbfmndzghr",
	    password="97e2dd8a68587ef47ecc4ced5b9137bf7ab6daadada6757c028cf96b81c8ac3b"
	)

	cursor=conn.cursor()
	cursor.execute("insert into intake (user_id, intake_date, food_name, calorie, carb, fat, protein, sodium) values('{}','{}','{}','{}','{}','{}','{}','{}')".format(user_id,date.today(),food_name,calorie,carb,fat,protein,sodium))
	conn.commit()
	cursor.close()

#return map summarizes user intake in past 'day' days
def get_past_intake_days(user_id,day=1,end_date=''):
	day=int(day)
	if(len(end_date)!=0):
		end_date=datetime.strptime(end_date,'%B %d, %Y')
	else:
		end_date=date.today()
	target_date=end_date-timedelta(days = day)

	response={}
	keys=["intake_date", "food_name", "calorie", "carb", "fat", "protein", "sodium"]
	conn = psycopg2.connect(
	    host="ec2-52-86-123-180.compute-1.amazonaws.com",
	    port="5432",
	    database="d2o2cbpkkb06fc",
	    user="zunhwbfmndzghr",
	    password="97e2dd8a68587ef47ecc4ced5b9137bf7ab6daadada6757c028cf96b81c8ac3b"
	)

	cursor=conn.cursor()
	cursor.execute("select {} from intake where user_id like '{}' and intake_date > '{}' and intake_date <= '{}' order by intake_date desc".format(",".join(keys),user_id,target_date,end_date))
	entries=cursor.fetchall()
	conn.commit()
	cursor.close()

	#print([(a,sum([int(c) for c in [b[2] for b in entries if b[0] ==a]])) for a in list(set([i[0] for i in entries]))])
	response={
		"entries":len(entries),
		"total_calorie":sum([float(i[2]) for i in entries]),
		"total_carb":sum([float(i[3]) for i in entries]),
		"total_fat":sum([float(i[4]) for i in entries]),
		"total_protein":sum([float(i[5]) for i in entries]),
		"total_sodium":sum([float(i[6]) for i in entries]),
		"calorie_per_day":[(a,sum([int(c) for c in [b[2] for b in entries if b[0] ==a]])) for a in list(set([i[0] for i in entries]))],
		"data":[
			dict(zip(keys,i)) for i in entries
		]
	}
	return response
#print(record_intake(-1,"chicken",100,100,100,100,100))
#print(get_past_intake_days(-1,1))

#return intake records in past 7 or 30 days (default 7 days), specificlly used for analysis page
def get_past_intake(user_id,day=7,end_date=''):
	day=int(day)
	target_date=date.today()-timedelta(days = day)

	if(len(end_date)!=0):
		end_date=datetime.strptime(end_date,'%B %d, %Y')
	else:
		end_date=date.today()
	target_date=end_date-timedelta(days = day)

	response={}
	keys=["intake_date", "food_name", "calorie", "carb", "fat", "protein", "sodium"]
	conn = psycopg2.connect(
	    host="ec2-52-86-123-180.compute-1.amazonaws.com",
	    port="5432",
	    database="d2o2cbpkkb06fc",
	    user="zunhwbfmndzghr",
	    password="97e2dd8a68587ef47ecc4ced5b9137bf7ab6daadada6757c028cf96b81c8ac3b"
	)

	cursor=conn.cursor()
	cursor.execute("select {} from intake where user_id like '{}' and intake_date > '{}' order by intake_date desc".format(",".join(keys),user_id,target_date))
	entries=cursor.fetchall()
	conn.commit()
	cursor.close()

	data = [dict(zip(keys,i)) for i in entries]

	out_carb = {}
	for i in data: out_carb.setdefault(i['intake_date'],[]).append(i['carb'])
	out_calorie = {}; ca_out = {}
	for i in range(1,day): ca_out[str(target_date+timedelta(days=i))] = []
	for i in data: ca_out.setdefault(i['intake_date'],[]).append(i['calorie'])
	for i in data: out_calorie.setdefault(i['intake_date'],[]).append(i['calorie'])
	out_prot = {}
	for i in data: out_prot.setdefault(i['intake_date'],[]).append(i['protein'])
	out_fat = {}
	for i in data: out_fat.setdefault(i['intake_date'],[]).append(i['fat'])

	daily_analysis = [
		0 if len(out_carb.values())==0 else sum([float(i) for day_list in out_carb.values() for i in day_list])/len(out_carb.values()),
		0 if len(out_calorie.values())==0 else sum([float(i) for day_list in out_calorie.values() for i in day_list])/len(out_calorie.values()),
		0 if len(out_prot.values())==0 else sum([float(i) for day_list in out_prot.values() for i in day_list])/len(out_prot.values()),
		0 if len(out_fat.values())==0 else sum([float(i) for day_list in out_fat.values() for i in day_list])/len(out_fat.values())]

	# print(data)
	past_ca	= {}
	for i in ca_out.keys():
		temp = []
		for j in ca_out[i]: temp.append(float(j))
		# print(sum(temp))
		past_ca[i] = sum(temp)
	
	response={
		"daily_analysis":daily_analysis,
		"past_ca_k":list(past_ca.keys()),
		"past_ca_v":list(past_ca.values())
	}
	return response

#print(get_past_intake(11,7))
#print(get_past_intake_days(-1,1,"December 2, 2021"))
