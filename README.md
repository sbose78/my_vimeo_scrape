Architecture 
-------------

	Deployed application uses :

		1. Database: MySQL 5.5 hosted on Amazon RDS .
		2. Application: Django hosted on Redhat Paas Openshift.
		3. Front-end design & dev : HTML5 + CSS + Javascript + JQuery1.8

	Development environment consisted of :
		1. Database: MySQL 5.5 ( local )
		2. Python



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
				DB_LOCAL_HOST = "vimXXXXXXXXXXXXXXazonaws.com"
				DB_LOCAL_PORT =3306
				DB_LOCAL_USER = "root"
				DB_LOCAL_PASSWORD = "qXXXXXXX6"
				DB_LOCAL_DATABASE = "vimeodb"

