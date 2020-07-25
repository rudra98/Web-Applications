# Web-Applications
While I was in my 6 months internship, I made this simple template of a web app which can be used with little to no code to deploy.
I worked with my front-end team, who helped me learn html and css which I could use to integrate it with jinja2 which is a library useful when working with flask. I used sql-alchemy for the database as this is just a template.
Explanation:
The mvt is a folder which consists almost everything from py codes to html templates. Now MVT is Model-View-Template, models are the py codes which makes/designs the structure of the data stored in database, forms are the forms visible on the front end which help to take proper data input and pass it on to models. Routes help in routing, as in to give directions to the code and add some functionality if needed. For ex: if you go from home to about page on the front end the migration from home to about with all the functionalities is taken care by routes at the backend. Functionalities which routes add is that any data passed first come to routes and it can be used to store it to database. Also data checks and diversion if particular type of data is caught can be done in this file.
I also used many other libraries to send emails for verifications, generate code to check if valid and add timer to get it in time.
For using this code you need to add your emailid, password and server details.
It is just a template but I find it very useful.
