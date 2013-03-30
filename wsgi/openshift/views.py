import os
from django.shortcuts import render_to_response
from django.http import HttpResponse
import json
import MySQLdb
#8044
# -*- coding: utf-8 -*-

'''
db = MySQLdb.connect(host="localhost",
                       port = 3306,
                       user="root",
                     passwd="qwerty", # your password
                     db="vimeo") # name of the data base

'''

db = MySQLdb.connect(host="vimeo.c21gzhluapko.ap-northeast-1.rds.amazonaws.com",
                       port = 3306,
                       user="sbose78",
                     passwd="qwerty123456", # your password
                     db="vimeodb") # name of the data base


def home(request):
    return render_to_response('home/home.html')
def user(request):
	return render_to_response('home/user.html')

def get_user_data(request,username):
	#return render_to_response('home/user.html')
	'''
	all_users = list()

	for i in range(1,5):
		response_data={}
		response_data['username'] = username
		response_data['result'] = 'failed'
		response_data['message'] = 'You messed up'

		all_users.append(response_data)

	return HttpResponse(json.dumps(all_users), mimetype="application/json")
	'''

	return HttpResponse(json.dumps(search(username)),mimetype="application/json")



def search(key):
	cur = db.cursor() 
	count = 0
	key="%"+key+"%"
	try:
		# get the total number of users
		cur.execute("""SELECT count(*) from user where name LIKE %s""",(key))
		for row in cur.fetchall():
			count = row[0]
		print count
		cur.close()
		cur = db.cursor()

		# get a maximum of 100 out of the total number of users
		cur.execute("""SELECT * from user where name LIKE %s LIMIT 100""",(key))
		all_results =list()
		for row in cur.fetchall():
			user_id=row[0]
			name = row[1].decode("latin-1")
			url = row[2].decode("latin-1")
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
		final_deliverable=list()

		results = {}
		results['count']=count
		results['users']= all_results

		final_deliverable.append(results)

	except Exception, e:
		print "error---" , e

	#print all_results
	return final_deliverable