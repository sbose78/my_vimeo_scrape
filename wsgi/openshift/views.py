import os
from django.shortcuts import render_to_response
from django.http import HttpResponse
import json
import MySQLdb
import dbprops

# -*- coding: utf-8 -*-

db = MySQLdb.connect(host=dbprops.DB_HOST,
                       port = dbprops.DB_PORT,
                       user=dbprops.DB_USER,
                     passwd=dbprops.DB_PASSWORD, 
                     db=dbprops.DB_DATABASE) 

def home(request):
    return render_to_response('home/home.html')
def user(request):
	return render_to_response('home/user.html')

def get_user_data(request,username):
	return HttpResponse(json.dumps(search(username)),mimetype="application/json")

'''
	This function takes the search keyword as 'INPUT' and 
	returns the JSON object containig the search results.

'''

def search(key):
	cur = db.cursor() 
	count = 0
	key="%"+key+"%"
	try:
		# get the total (count) number of users
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
		#db.close()

	except Exception, e:
		print "[EXCEPTION]" , e

	#print all_results

	return final_deliverable