# UOCIS322 - Project 6 #
Brevet time calculator with MongoDB, and a RESTful API!

Read about MongoEngine and Flask-RESTful before you start: [http://docs.mongoengine.org/](http://docs.mongoengine.org/), [https://flask-restful.readthedocs.io/en/latest/](https://flask-restful.readthedocs.io/en/latest/).

## Before you begin
You *HAVE TO* copy `.env-example` into `.env` and specify your container port numbers there!
Note that the default values (5000 and 5000) will work!

*DO NOT PLACE LOCAL PORTS IN YOUR COMPOSE FILE!*

## Overview

You will reuse your code from Project 5, which already has two services:

* Brevets
	* The entire web service
* MongoDB

For this project, you will re-organize `Brevets` into two separate services:

* Web (Front-end)
	* Time calculator (basically everything you had in project 4)
* API (Back-end)
	* A RESTful service to expose/store structured data in MongoDB.

## Tasks
* Application Outline
  * This app will generate a website that calculate the opening time and closing time for ACP brevets based on the checkpoint(you typed as input) kilometers and the time you choose. In this project 6, instead of communicating with database directly, we will use Restful API to wrap the frontend and backend part respectively. When you press the submit botton, we will send your data to the flask and then pass it to our brevet api. With the form of JSON the data will be evaluated using the models.py formatting and being stored into mongoengine database; when you press the display button, in reverse, we will fetch the data from our brevet api, get the data back from the mongoengine database, and package it and send it to the frontend, then display the data thay you typed before.

* Algorithm(The way we calcute the open and the close time)
	* Basically, we will use Maximum and Minimum Speed to Calculate Open Time and Close Time respectively.
	* In different kilometer scales, we have different standard of speeds. (For example, in 0-200, the Max Speed is 34 km/hr; in 200-400, the Max Speed is 32 km/hr; in 400-600, the Max Speed is 30 km/hr...)
	* There are some special cases:
	   * The closing time for 0 km is always 1 hour, and if the km is before 60km, we will use a different rule to take care of late stater.
	   * We might have some adjustments on closing time on special kms. (For example, if your end point is 200km, the closing time is not 13h 20 min, is 13h 30min) 

*  How To Use Start(Docker instructions, Web app instructions)
	* For Docker Compose Instruction:
	  * step1: build and run our docker compose file by "docker compose up" 
	  * step2: open the browser and go into the localhost then interact with the browser
	
	* Web app instruction
	  * First, you need to choose the end km or the length of the race based on the options
	  * Second, you need to choose the date you want to query
	  * Third, you can type the checkpoint km one by one and press return, you will get the exact time for the open time and close time.
	  * Fourth, you can press the submit button to submit all the data to the api, and api will pack data to the mongoengine database. After submission, when you press display buttion, you will get all the data back in frontend through api.



## Grading Rubric

* If your code works as expected: 100 points. This includes:
    * API routes as outlined above function exactly the way expected,
    * Web application works as expected in project 5,
    * README is updated with the necessary details.

* If the front-end service does not work, 20 points will be docked.

* For each of the 5 requests that do not work, 15 points will be docked.

* If none of the above work, 5 points will be assigned assuming project builds and runs, and `README` is updated. Otherwise, 0 will be assigned.

## Authors

Michal Young, Ram Durairajan. Updated by Ali Hassani.
