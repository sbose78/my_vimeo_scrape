import MySQLdb
import dbprops

db = MySQLdb.connect(host=dbprops.DB_LOCAL_HOST,
                       port = dbprops.DB_LOCAL_PORT,
                       user=dbprops.DB_LOCAL_USER,
                     passwd=dbprops.DB_LOCAL_PASSWORD, 
                     db=dbprops.DB_LOCAL_DATABASE) 

db_amazon = MySQLdb.connect(host=dbprops.DB_AWS_HOST,
                       port = dbprops.DB_AWS_PORT ,
                       user=dbprops.DB_AWS_USER,
                     passwd=dbprops.DB_AWS_PASSWORD , # your password
                     db=dbprops.DB_AWS_DATABASE ) # name of the data base

def search(key):
	cur = db.cursor() 
	key="%"+key+"%"
	try:
		cur.execute("""SELECT * from user where name LIKE %s""",(key))
		all_results =list()
		for row in cur.fetchall():
			user_id=row[0]
			name = row[1]
			url = row[2]
			has_video = row[3]
			has_featured_video = row[4]
			is_paid = row[5]

			user={}
			user['user_id'] = user_id
			user['name'] = name
			user['url'] = url
			user['has_video'] = has_video
			user['has_featured_video'] = has_featured_video
			user['is_paid'] = is_paid

			all_results.append(user)
	except Exception, e:
		print "error" , e

	print all_results
	return all_results

#search("adam")

def update_local_db_user_table(user):
	cur =db.cursor()
	try:
		cur.execute("""UPDATE user set inserted_into_amazon = 1 where url = %s""",(user["url"]))
		db.commit()
		print "[UPDATE_LOCAL_SUCCESS] ",user
	except Exception,e:
		print "[UPDATE_LOCAL_FAIL]: ",e


def insert_into_amazon(user):
	try:
		cur = db_amazon.cursor()
		#insert into amazon
		name= user["name"]
		url = user["url"]
		has_video = user["has_video"]
		has_featured_video = user["has_featured_video"]
		is_paid = user["is_paid"]
		cur.execute("""INSERT into user(name,url,has_video,has_featured_video,is_paid) VALUES(%s,%s,%s,%s,%s)""",(name,url,has_video,has_featured_video,is_paid))
		db_amazon.commit()
		print "[INSERT_AWS_SUCCESS] :",user
		#update local db user table
	except Exception,e:
		print "[INSERT_AWS_FAIL] ",e
		# possibly because a duplicate row was being inserted.
def get_rows_from_local_db():
	# get all un-inserted rows from local table
	users =list()
	cur = db.cursor() 
	try:
		cur.execute("SELECT * from user where inserted_into_amazon = 0")
		for row in cur.fetchall():
			user_id=row[0]
			name = row[1]
			url = row[2]
			has_video = row[3]
			has_featured_video = row[4]
			is_paid = row[5]
			user={}
			user['user_id'] = user_id
			user['name'] = name
			user['url'] = url
			user['has_video'] = has_video
			user['has_featured_video'] = has_featured_video
			user['is_paid'] = is_paid
			users.append(user)
	except Exception,e:
		print "[ERROR]",e
	return users

def main():
	users = get_rows_from_local_db()
	#print users
	amazon_and_localdb_bridge(users)
def amazon_and_localdb_bridge(users):
	for user in users:
		insert_into_amazon(user)
		update_local_db_user_table(user)
		print "[BRIDGE] ",user
main()