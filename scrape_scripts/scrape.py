from HTMLParser import HTMLParser
import MySQLdb
import time
from random import randint

users=set()
my_semaphore  = 2

db = MySQLdb.connect(host="localhost",
                       port = 3306,
                       user="root",
                     passwd="qwerty", # your password
                     db="vimeo") # name of the data base

# taking out an unvisited URL for 

def markError(my_url):
    '''
    db = MySQLdb.connect(host="localhost",
                        port = 3306,
                        user="root",
                      passwd="qwerty", # your password
                      db="vimeo") # name of the data base
    '''
    cur = db.cursor() 
    try:
       cur.execute("""UPDATE link set visited = 3 where url = %s""",(my_url))
       db.commit()        
    except Exception, e:
       #cur.rollback()
       print "There was an error while marking error : ", e
    #db.close()
def getUnvisitedURL():
    my_url = "NULL" # just an initialisation value
    '''
    db = MySQLdb.connect(host="localhost",
                        port = 3306,
                        user="root",
                      passwd="qwerty", # your password
                      db="vimeo") # name of the data base
    '''
    cur = db.cursor() 
    try:
       cur.execute("select url from link where visited = 0 limit 1")
       for row in cur.fetchall() :
            my_url = row[0]
            print "[INFO] : crawling ",my_url
       if my_url != "NULL" :
            cur= db.cursor()
            #update link set visited = 0 where url = 'http://vimeo.com/b/likes'

            cur.execute("""UPDATE link set visited = 1 where url = %s""",(my_url))
       else:
            pass
       db.commit()        
    except Exception, e:
       #cur.rollback()
       print "There was an error while fetching UnvisitedURL : ", e
    #db.close()
    return my_url

# This method inserts the crawled linked into the local MySQL database

def insertLink(my_link):
    '''
    db = MySQLdb.connect(host="localhost",
                        port = 3306,
                        user="root",
                      passwd="qwerty", # your password
                      db="vimeo") # name of the data base
    '''
    cur = db.cursor() 
    try:
       cur.execute("""INSERT into link(url,type,visited) VALUES(%s,%s,0)""",(str(my_link),"arb"))
       #cursor.execute("""INSERT INTO anooog1 VALUES (%s,%s)""",(188,90))
       db.commit()
       print "link:", my_link
    except Exception,e:
       #cur.rollback()
       print "already present ",e
    #db.close()
def insertUser(my_user):
    print "trying to insert"
    '''
    db = MySQLdb.connect(host="localhost",
                        port = 3306,
                        user="root",
                      passwd="qwerty", # your password
                      db="vimeo") # name of the data base
    '''
    cur = db.cursor() 
    try:
       cur.execute("""INSERT into user(name, url,has_video,has_featured_video,is_paid) VALUES(%s,%s,%s,%s,%s)""",(my_user['name'],my_user['url'],my_user["hasVideo"],my_user["isFeatured"],my_user["isPlusUser"]))
       #cur.execute("""INSERT into user(name, url,has_video,has_featured_video,is_paid) VALUES(%s,%s,%s,%s,%s)""",("boka12chele",my_user['url'],my_user["hasVideo"],my_user["isFeatured"],my_user["isPlusUser"]))       
       #cursor.execute("""INSERT INTO anooog1 VALUES (%s,%s)""",(188,90))
       print int(my_user["hasVideo"]),int(my_user["isFeatured"]),int(my_user["isPlusUser"])
       db.commit()
    except Exception, e:
       #cur.rollback()
       print e
    #db.close()


class MyHTMLParser(HTMLParser):
  
    def __init__(self):
        HTMLParser.__init__(self)
        self.isUser = 0
        self.url = "null url"
        self.isFeatured = 0
        self.hasVideo = 0
        self.name = "john"
        self.isPlusUser = 0;

        self.foundIsPlusUser=0
        self.foundUser = 0
        self.foundURL= 0
        self.foundIsFeatured = 0
        self.foundIsHasVideo = 0
        self.foundName = 0

    def getData(self):
        stats = {}
        stats["isUser"] = self.isUser
        stats["name"]=self.name
        stats["url"]=self.url
        stats["isPlusUser"] = self.isPlusUser
        stats["hasVideo"]=self.hasVideo
        stats["isFeatured"] = self.isFeatured 
        return stats

    def process_link(self, my_link):
        if "." not in my_link and "/" in my_link:
            my_link = "http://vimeo.com"+my_link
            return my_link
        else:
            return my_link

    def handle_data(self, data):
     # Scraping out the number of uploaded videos
        if self.foundIsHasVideo == 2  :
            #print data
            self.hasVideo = data
            self.foundIsHasVideo = 3 
            return 0
        elif self.foundIsFeatured == 2 :   #scraping out the "featured videos label"
            if data == "Featured Videos":
                self.isFeatured = 1
                self.foundIsFeatured = 3
        else:
            pass

    def handle_starttag(self, tag, attrs):
        # for all links encountered while parsing
        if tag == "a" :
            for attr in attrs:
                if attr[0] == "href":
                    if "/" in attr[1] and "ad" not in attr[1]:
                        p = self.process_link(attr[1])
                        #print "link:", p
                        #users.add(attr[1])
                        my_link = self.process_link(attr[1])
                        insertLink(my_link)
                    else:
                        pass
                else :
                    pass

        # locating user name, url and also whether this is a user profile

        elif tag == "meta":       
               
                for attr in attrs:
                  #  print "****",attr[0] , "----" , attr[1]
                    #print "-----SELF.isUser" , self.isUser , attr[0]


                    #finding if user

                    if attr[0] == "property" and attr[1] == "og:type":
                        #print "meta:", attr[1]
                        users.add(attr[1])
                    elif attr[0] == "content" and attr[1] == "profile":
                        self.isUser=1
                        print "FOUND USER ",self.isUser

                    #finding the name
                    if self.isUser == 1 and attr[0] == "property" and attr[1] == "og:title" and self.foundName == 0:
                        #print "FOUND NAME"
                        self.foundName =1
                    elif self.isUser == 1 and attr[0] == "content" and self.foundName == 1 :
                        self.name = attr[1]
                        self.foundName = 2
                        print self.name

                    # finding the URL

                    elif self.isUser == 1 and attr[0] == "property" and attr[1] == "og:url" and self.foundURL == 0 :
                       # print "found url"
                        self.foundURL =1
                    elif self.isUser == 1 and attr[0] == "content" and self.foundURL == 1:
                       # print attr[1]
                        self.url=attr[1]
                        self.foundURL = 2
                        print self.url
                    else : 
                        pass
        else : pass    

        if self.isUser == 1 :
        # searching featured vids

            if tag == "div" and self.foundIsFeatured == 0:
                for attr in attrs :
                    if attr[0] == "class" and attr[1] == "col_large" :
                        self.foundIsFeatured  = 1
                    else :
                        pass
            if tag == "h2" and self.foundIsFeatured == 1:
                self.foundIsFeatured = 2


            # locating the number of videos uploaded            

            elif tag == "ul" and self.foundIsHasVideo == 0 :
                #print "found a ul"
                for attr in attrs:
                    if attr[0]=="class" and attr[1] == "block floated_list stat_list bubble_list nipple_left":
                        print "bull's eye"
                        self.foundIsHasVideo = 1
                    else:
                        pass
            elif tag == "b" and self.foundIsHasVideo == 1 :
                self.foundIsHasVideo = 2
                #self.hasVideo = 1
            elif tag == "span" and self.foundIsPlusUser == 0 :
                for attr in attrs :
                    if attr[0] != "class" :
                        break;
                    elif attr[1] == "badge_plus" or attr[1] == "badge_pro":
                        self.foundIsPlusUser  = 1
                        self.isPlusUser = 1
                    else:
                        pass       
            else :
                pass
        else: 
            pass

import urllib2

#insertLink("aaa")

'''

urls = {"/a","/b","/c","/d","/e"}
base_url = "http://vimeo.com";

for each_url in urls :
    print "opening ", base_url+each_url
    f = urllib2.urlopen(base_url+each_url)     
    my_html = ""
    for line in f:
        my_html += line
    #print my_html
    parser = MyHTMLParser()
    parser.feed(my_html)  
    user_data = parser.getData() 
    print user_data
    if user_data["isUser"] == 1:
        insertUser(user_data)
    #print users
'''

def crawl_link(my_url):
    #my_semaphore --
    #f = urllib2.urlopen(my_url)        
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    f = opener.open(my_url)
    my_html = ""
    for line in f:
        my_html += line
    parser = MyHTMLParser()
    parser.feed(my_html)
    user_data = parser.getData()
    print user_data
    if user_data["isUser"] == 1:
        insertUser(user_data)
        print "[INFO] Inserted user"
    #my_semaphore++

import threading
next_url=getUnvisitedURL()
while next_url != "NULL":    
    if "vimeo.com" in next_url:
        print next_url
        try:
            random_wait = randint(1,5)
            print "-- WAITING FOR -- ",random_wait
            time.sleep(random_wait)
            crawl_link(next_url)
            '''
            while my_semaphore < 1 :
                pass
            t = threading.Thread(target=crawl_link, args = (next_url,))
            t.daemon = True
            t.start()            
            '''
        except Exception, e:
            markError(next_url)
            print "Exception - skipping ",e
    else:
        pass
    next_url = getUnvisitedURL()
db.close()

