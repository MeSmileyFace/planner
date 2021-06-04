# YOUR PROJECT TITLE PLANNER
#### Video Demo:  https://youtu.be/imsyJhAaGuc
#### Description:  

My project is a web application that allows you to log tasks via the calendar tab and keep track of tasks via the homepage tab. I have chosen this design and colour scheme for I believe they are welcoming but also work well with each other to give the user the perfect experience when using it, I have debated whether the tables on the homepage should be stylized in the same way, but later came to the conclusion that the simplicity of the tables is complementary to the purpose of the homepage and the finished tasks part of the application which is to be concise while also containing all the necessary information you could want.

## The project consists of these elements:

   1. The SQL folder which contains a few queries I often needed at quick disposal
   2. The folder where I kept the style.css folder which contains all the style for the project
   3. The file calendarScript that contains all the javascript the page had
   4. The templates folder that contains all the templates the project contains with all the HTML and jinja
   5. The file app.py which contains all the python code used in the project
   6. The planner.db which stores all the data inputted by the user
   7. Finally helpers.py which contains all the helper functions I used which I did not want clogging up space in the main app.py file

### 1. The python script is comprised of the next parts:

 - The imports and functions I used from various libraries.
 - The syntax used to integrate flask and python.
 - The code required to keep a user in session
 - CS50's syntax that interconnects my database with the python code 
 - The **index** route that is responsible for rendering the homepage template, that is found in the templates folder to which i will get to shortly, in which I have used various filters in conjunction with the proper sqlite3 queries to precisely display the tables that are to be represented in the appropriate means.
 Registration tab which requires username, password and a password confirmation all of which
 - Next is the **calendar** route which is fairly bare seeing as how its only purpose is to render the calendar template, the rest of the relevant coding was done in javascript.
 - Next up is the **ftasks** route which contains the map function that uses a lambda function to remap the finishedTasks and add a daysUntilEnd variable inside the list which is filtered to only show the finished tasks.
 - After that we have the **register** route which is the one you will inevitably have to use to create your account to use the application, It has guards to make sure the account registration is carried out as the format requires, for example: it will not allow you to create an account if the username you are trying to use is already registered to another account, as well as making sure your passwords match and contain 8 or more characters with at least one being uppercase and one being lowercase. When you meet all of the preset requirements your credentials will be stored in the database, your username will be stored in the format u have inputted but your password will be hashed and saved in that way. If everything went as planned you will then be redirected to the login screen where u can access your newly made account.
 - The next route is **login** which begins with clearing of the session so that your account is yours alone. In the login part of the script you input your credentials which are checked and cross-referenced with the database and if they are found and are correct you will be logged in and if incorrect you will get an error message giving you the reason for the error and the matching code along with it.


 - Then we have the **logout** route that simply logs the user out by clearing the session and you are redirected to the log in page.
 - After which we have the **dateEvent** route which is just used to display the date you have chosen to log a task in by constructing a date by means of getting the elements off of the calendar form and applying some simple methods of transforming dates.
 - The next route is **dateEventAjax** where we use Ajax to relay information between javascript and python and return the json object from the json dumps. The javascript hides and shows the forms depending on what the user has clicked on the page and adds event listeners to all the elements which we want to give the user a response to after the user interacted with it. 
 - The **deleteEventAjax** route is used to delete an event we have previously logged and again uses Ajax syntax to pass values between python and javascript in the case of an error on the server end I have implemented a guard that disallows the user to remove any tasks that do not belong to him.
 - Lastly in the python script we have the **saveTask** route where we just request.form.get the name, description and due date(the dates are formatted by a helper function I have implemented that simply standardizes the dates so the always appear in the same format), and insert them into the database.

### 2. The templates folder contains: 
   - All of the html templates for the whole project with the layout.html containing all of the tags that are to be displayed on every page. 
  
### 3. The style.css file 
- Contains all of the style properties in the whole project.

### 4. calendarScript.js
- Contains almost all of the code responsible for the calendar page, dynamically generates all of the dates and displays them using for loop and some back-ticks.
- Has event listeners on the arrow keys which renders the calendar but with the next or previous month.
- The ajax syntax that gives the task with the id given by python the hidden attribute.
- The *fix date* function simply adds a zero in front of the month and day if they originally do not have one.
- The jquery part of the dateEventAjax function which hides and shows the form with which you input the dates after choosing one via the previously mentioned method.
- And lastly the last part is an anonymous function that starts after the click of the add task button and hides said button and shows the form and automatically scrolls down the page for your convenience.

### 5. Helpers.py
- Contains the helper function used across the main python script
- The requires login decorator makes sure that any functions in the main app.py script that contain the decorator have to have the user logged in. 
- Apology helper functions simply takes a message and a code and displays it on a page.
- The striptime function strips the date to match the y-m-d format.

made by me :)
