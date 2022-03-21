import psycopg2

def register(first_name,last_name,email,password):
	conn = psycopg2.connect(
	    host="ec2-52-86-123-180.compute-1.amazonaws.com",
	    port="5432",
	    database="d2o2cbpkkb06fc",
	    user="zunhwbfmndzghr",
	    password="97e2dd8a68587ef47ecc4ced5b9137bf7ab6daadada6757c028cf96b81c8ac3b"
	)

	cursor=conn.cursor()
	cursor.execute("select count (*) from IXUsers where email like '{}'".format(email))
	
	if(cursor.fetchone()[0] !=0):
		cursor.close()
		return {"result":"failed","errormsg":"user email already exists"}
	
	cursor.execute("INSERT INTO IXUsers (firstName, lastName, email, password) values ('{}','{}','{}','{}');".format(first_name,last_name,email,password))

	conn.commit()
	cursor.close()
	assert update_settings(email)["result"]!="failed"
	return {"result":"succeed"}

def update_settings(email):
	conn = psycopg2.connect(
	    host="ec2-52-86-123-180.compute-1.amazonaws.com",
	    port="5432",
	    database="d2o2cbpkkb06fc",
	    user="zunhwbfmndzghr",
	    password="97e2dd8a68587ef47ecc4ced5b9137bf7ab6daadada6757c028cf96b81c8ac3b"
	)

	cursor=conn.cursor()
	cursor.execute("select count (*) from IXUsers where email like '{}'".format(email))
	
	if(cursor.fetchone()[0] ==0):
		cursor.close()
		return {"result":"failed","errormsg":"user does not exist"}

	# update_sql="update Users set "
	# for i in survey_options:
	# 	update_sql+=("{}={}".format(i,option_params[i]))
	# 	if(i!=survey_options[-1]):
	# 		update_sql+=(",")
	# update_sql+=(" where email like '{}';".format(email))
	# print(update_sql)
	# cursor.execute(update_sql)

	conn.commit()
	cursor.close()
	return {"result":"succeed"}

def get_settings(email):
	conn = psycopg2.connect(
	    host="ec2-52-86-123-180.compute-1.amazonaws.com",
	    port="5432",
	    database="d2o2cbpkkb06fc",
	    user="zunhwbfmndzghr",
	    password="97e2dd8a68587ef47ecc4ced5b9137bf7ab6daadada6757c028cf96b81c8ac3b"
	)
	cursor=conn.cursor()
	cursor.execute("select count (*) from IXUsers where email like '{}'".format(email))
	if(cursor.fetchone()[0] ==0):
		cursor.close()
		return {"result":"failed","errormsg":"user does not exist"}

	
	cursor.execute("select * from IXUsers where email like '{}'".format(email));
	res=cursor.fetchone()
	#print(res)

	result={}
	# for i in range(len(survey_options)):
	# 	result[survey_options[i]]=res[4+i]
	conn.commit()
	cursor.close()
	return {"result":"succeed","data":result}

# print(register("abby","x","test@gmail.com","password"))
#print(get_settings("test@gmail.com"))