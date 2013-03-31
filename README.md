

The URL of the deployed application
---------------------------------------

		http://myscrape-nodejstest.rhcloud.com/



The objective
---------------

The task was to scrape out the following data from 5000+ Vimeo user pages 
and save it to a MySQL database.

	1. Name of the user.

	2. URL of the profile.

	3. Whether the user has uploaded any videos.

	4. Whether the user has an videos also featured as Staff Picks.

	5. Whether the user is a paid user. ( PAID/PRO )


The algorithm
------------

De-mystifying the above requirements, 
the following elements were dug out from the user page using the hints mentioned below.

For instance, in case of http://vimeo.com/markdenega

	i. Check if the currently crawled page is a user-profile page.

		<meta property="og:type" content="profile">

	ii. Find out the name of the user.

		<meta property="og:url" content="http://vimeo.com/markdenega">

	iii. Find out the URL of the profile page.

		<meta property="og:url" content="http://vimeo.com/markdenega">

	iv. Whether the user has staff picks.

		Existence of the following tree :

			<div class="col_large">
	                 <section class="block">
	                    <h2>Featured Videos</h2>

    v. Whether the user has uploads:

    	The content of <b> </b> in the following tree: 

	    	<ul class="block floated_list stat_list bubble_list nipple_left">
	            <li>
	                <div>
	                    <a href="/markdenega/videos">
	                        <b>13</b> <span>Videos</span> 



Approach
------------

I used a Python script to crawl vimeo.com and store all the links and user data in
my local MySQL database. After details of 5000+ users were acquired, the crawling was terminated and the DJANGO application was built locally and then deployed on Redhat PaaS ( Openshift ). The local MySQL database was migrated to Amazon RDS MySQL using another Python script.

Even though there were options of using Beautiful Soup or Scrapy, I prefered experimenting with
my own low-level implementation of the self-designed user profile page scraping algorithm.


	

In brief :


    i. 		(Staring from http://vimeo.com)
    		Scrape out each link starting from vimeo.com and save it to the 
    		local MySQL database table called "LINK"

    ii. 	Choose an unvisited link from the table "LINK", programmatically scrape out and 
    		save all the links. Recognise using the algorithm if the page is a user page. 


    iii. 	If yes, then save the user data into the "USER" table and
    		proceed with the next unvisited link from the LINK table.

    iv.		Continue the above steps till 5000+ user profiles have been scraped.

    v. 		Write the Django appliction with a REST-style request handler for requesting user 
    		info for all matching user names ( and sub-strings ). 
    		Place the function in views.py and update the urls.py

    vi.   	Write the HTML+ CSS + Javascript web page where the user has an option to 
    		query by user  name ( full or partial ) and place it under wsgi/openshift/templates/home/

    viii.  The request is made by an AJAX call and the JSON response is parsed and 
    	   shown in the web-page. The results are stored for re-presentation of the same data conditionally by filters.



Architecture 
-------------

	Deployed application uses :

		URL of deployed applicaton : http://myscrape-nodejstest.rhcloud.com/

		1. Database: MySQL 5.5 hosted on Amazon RDS .
		2. Application Server: ( Redhat Paas ) Openshift http://openshift.redhat.com/ 
		3. Front-end design & dev : HTML5 + CSS + Javascript + JQuery1.8


	Development environment consisted of :
		1. Database: MySQL 5.5 ( local )
		2. Scripting: Python
		3. OS : Ubuntu 12.04



Installation
------------

1. Clone this repository to your local system.

2. Add the properties files called dbprops.py and place it under wsgi/openshift

		The file contents should be as follows:

		DB_HOST = "127.0.0.1"
		DB_PORT =3306
		DB_USER = "my_user"
		DB_PASSWORD = "my_password"
		DB_DATABASE = "vimeodb"


		( The dbprops.py has been put in .gitignore to avoid giving out the database credentials publicly )


3. The database used in the LIVE environment is a MySQL database.

		One table named "USER" is required:

		CREATE TABLE `user` (
		  `id` int(11) NOT NULL AUTO_INCREMENT,
		  `name` varchar(45) DEFAULT NULL,
		  `url` varchar(45) DEFAULT NULL,
		  `has_video` int(11) DEFAULT NULL,
		  `has_featured_video` int(11) DEFAULT NULL,
		  `is_paid` int(11) DEFAULT NULL,
		  `inserted_into_amazon` int(11) DEFAULT '0',
		  PRIMARY KEY (`id`)
		) ENGINE=InnoDB AUTO_INCREMENT=5091 DEFAULT CHARSET=latin1;


4. All static files are placed in the wsgi/static directory.
		The static files used are:
			i. Jquery : jquery-1.8.3.min.js
			ii. loading icon: loading-vim.gif

5. The contents of the scrape_scripts are not required in the web-project. 

		i. scrape.py was used for crawling vimeo.com and saving the links in the LINK table
			and user-data in the USER table.

			The DDL for the LINK table

					CREATE TABLE `link` (
						  `id` int(11) NOT NULL AUTO_INCREMENT,
						  `url` varchar(45) DEFAULT NULL,
						  `type` varchar(45) DEFAULT NULL,
						  `visited` int(11) DEFAULT NULL,
						  PRIMARY KEY (`id`),
						  UNIQUE KEY `url_UNIQUE` (`url`)
					) ENGINE=InnoDB AUTO_INCREMENT=1179195 DEFAULT CHARSET=latin1;		

			The DDL for the USER table :

					CREATE TABLE `user` (
						  `id` int(11) NOT NULL AUTO_INCREMENT,
						  `name` varchar(45) DEFAULT NULL,
						  `url` varchar(45) DEFAULT NULL,
						  `has_video` int(11) DEFAULT NULL,
						  `has_featured_video` int(11) DEFAULT NULL,
						  `is_paid` int(11) DEFAULT NULL,
						  `inserted_into_amazon` int(11) DEFAULT '0',
						  PRIMARY KEY (`id`)
					) ENGINE=InnoDB AUTO_INCREMENT=5091 DEFAULT CHARSET=latin1;




		ii. dbtasks.py was executed to copy all the locally stored user-data to the Amazon MySQL 		database.		

		iii. The above 2 files require a dbprops.py file which contains the database connection 
			 credentials.

			 The dbprops.py needs to be added and this is how it should look like:

			 	DB_AWS_HOST = "vimeXXXXXXXXXXXXXXXXXXXxonaws.com"
			 	DB_AWS_PORT =3306
			 	DB_AWS_USER = "sbose78"
				DB_AWS_PASSWORD = "XXXXXXX"
				DB_AWS_DATABASE = "vimeodb"
				DB_LOCAL_HOST = "localhost"
				DB_LOCAL_PORT =3306
				DB_LOCAL_USER = "root"
				DB_LOCAL_PASSWORD = "qXXXXXXX6"
				DB_LOCAL_DATABASE = "vimeodb"

Notable modules
----------------------

1. wsgi/openshift/views.py  : 	views.py houses the request handlers. 

2. wsgi/openshift/settings.py : This server configuration module contains settings specific to the 									OpenShift platform as well as the local development server.
3. wsgi/openshift/urls.py : 

		i. http://<SERVER_NAME>/ loads the web(and only) page of the application.

					The web interface consists of a text box where one can key in a string and press ENTER to load the search results. The server-side requests are made as AJAX. The AJAX request URL is discussed in the next part.
		
		ii. The REST-style request for user information can be sent as follows:

					HTTP GET http://<SERVER_NAME>/user/david

					A JSON containing all the users whose name contain the substring DAVID will be returned by the server.

					A partial response: 

					        "count": 10,
					        "users": [
					            {
					                "user_id": 1176,
					                "name": "Ginevra Adamoli",
					                "url": "http://vimeo.com/user3711006",
					                "is_paid": 0,
					                "has_video": 1,
					                "has_featured_video": 0
					            },
					            {
					                "user_id": 1360,
					                "name": "Samuel Adam",
					                "url": "http://vimeo.com/survivalgear",
					                "is_paid": 0,
					                "has_video": 10,
					                "has_featured_video": 0
					            },

4. wsgi/openshift/templates/home/user.html :
		
		This is the homepage of the application and loads when the following request is made:
		http://<SERVER_NAME>/





