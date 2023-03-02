# iWEB
This is the first submission for Group 30's ECM2434 Group Software Engineering Project.
Project members:
    - Kai Barber-Harris
    - Dimitar Sivrev
    - Bethany Whiting
    - Jude Goulding
    - Daria Sazonova
    - (no sixth member)

## Overview
iWEB is the working name for our web app. The system encourages green, sustainable behaviour by making the information to act in such a way as easily available as possible and rewarding users for acting on it.

## Technical details
iWEB's user-facing website is served by a Django web framework with custom views and functions.
The backend database is constructed in mySQL for release editions, and a database must be created and connected to in order for the site to function as intended. Optionally, you can load the packaged "test" database which includes a default admin account, a small set of "dummy" users, and a small set of items. The test database is best used to ensure iWEB is working to expected levels.

## Submission structure
This submission contains 3 primary folders, the GNU GPLv3 license, and this readme file.
Two of the folders are code submissions. The third is a miscellaneous folder with extra documentation and files.

### 1. app-mysql
The "app" folder contains all the source code and related files for iWEB to function; this is the "official" first prototype release of iWEB.
A "Getting started" setup guide is included at the bottom of this readme file, if you wish to run the app yourself.

### 2. app-sqlite
For ease of use for marking, we have also included the development branch of iWEB running on an embedded SQLite database. This is simply a copy of our most recent update to the main repository on github.
We include this as the mySQL version can be tricky to set up even with a guide, and don't want to create unnecessary roadblocks to seeing our website as it should look; the two versions act exactly the same from the user's point of view.

#### How to run the SQLite version
The SQLite app can simply be run using the command `python manage.py runserver` in `./app-sqlite/iWEB`.

### 3. misc
The "misc" folder contains important files not directly related to the running of the app, but which should be included in the submission.
One folder, "Specifications", contains various specifications written for different parts of the app. It should be noted that much of this specification work either occurred in meetings or in conversation across the team in our project Discord server we use for coordination and communication.
The second folder, "Meeting-notes", contains screenshots of our meeting notes we keep on Trello.
The third folder, "Docs", contains a detailed PDF of documentation for our map system as written by its programmer, Dimitar.
The fourth folder, "Discord", contains screenshots of our Discord server where much of the project coordination and discussion takes place. These screenshots include two examples of a typical discussion in the server and the channels we have to discuss various project aspects.
Finally, the fifth folder "Trello" is a screenshot of our Trello board as of the morning of submission. This folder also contains screenshots of the "Activity" tab of the Trello board to prove we have been using it throughout the first sprint.

### Other resources
Also relevant to the project submission are our [github repository](https://github.com/Mercuridi/iWEB) and [trello board](https://trello.com/b/xK5shoh4/project-sustainability). Both of these are private, but invites have been sent in the course of the project:
- @kaibarber invited Matt Collison on Trello
- @Mercuridi invited Liam Berrisford and Matt Collison on github (accepted, expired)
If we've missed you and you need an invite to one of these, please contact Kai (kab237@exeter.ac.uk). 
The Github repository contains our project code's most up-to-date version and related branches. This is where we actively develop the project, and a commit history can be found there to track the progress of the project.

The Trello board tracks our project's day-to-day development and process. This is where we coordinate our work, alongside our Discord server where we actively communicate what we're working on and discuss implementation as we work.

## Getting started
In order to run iWEB locally, there are certain dependencies that must be installed. Namely, these are Django and mySQL (server and client).

In order to run the server, Django must be provided with a valid user to access a valid mySQL database. This section of the readme will guide you through creating these requirements, assuming you have the earlier named dependencies installed.

### mySQL setup
1. Enter the mySQL command-line client as your root user.
2. Create an empty database "iweb":
    `CREATE DATABASE iweb;`
3. Add a new user to your mySQL:
    `CREATE USER 'iweb_sqluser'@'localhost' IDENTIFIED BY 'password';`
You may change the name of the user to whatever you wish, and the localhost to the name of the machine you plan to access the database from. If you are running the mySQL database and the Django server on the same machine, leave this as 'localhost'.
4. Grant privileges to the user on the `iweb` database:
    `GRANT ALL PRIVILEGES ON iweb.* TO 'iweb_sqluser'@'localhost';`
    `FLUSH PRIVILEGES;`
5. Check these commands have worked:
    `SHOW DATABASES;`                               (should show a new database "iweb")
    `SELECT user FROM mysql.user;`                  (should show us our new user "iweb_sqluser")
    `SHOW GRANTS FOR 'iweb_sqluser'@'localhost'`    (should show us the privileges our user has)
6. If these commands appear to return data as we expect, we can move on.

### Django setup
In the project directory, find the file `settings.py` at `./iWEB/app/iWEB/iWEB/settings.py`.
In this file, adjust the `DATABASES` key to provide Django the information it needs to find the database.
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', 
        'NAME': 'iweb',
        'USER': 'iweb_sqluser',
        'PASSWORD': 'password',
        'HOST': 'localhost',  
        'PORT': '3306',
    }
}
```
Here, the example has been filled with the default options as written in the earlier section. However, these should be changed as you wish (especially the password).

### Database pickup
At this point there are 2 options:

#### Pick up the test database
To pick up the test database, navigate to `./iWEB/app/iWEB` and run the following commands:
`python manage.py migrate --run-syncdb`
`python manage.py loaddata testdatabase.json`
This will populate the empty database we made in the mySQL command line client with the test database information. This database may still be modified later (write permissions are not affected).

#### Start from a fresh, empty database
To start from a fresh database, navigate to `./iWEB/app/iWEB` and simply run the command:
`python manage.py migrate`
This will construct the database schema required to run iWEB properly on the empty database we created in the mySQL command line client.

## Running the server
To run the server, navigate to `./iWEB/app/iWEB` and run the command:
`python manage.py runserver`
If all has gone well, this will open the server on the localhost which can be accessed through any web browser at `http://127.0.0.1:8000/`.
We are aware of an issue where the map will not properly load. In order to allow the map to load, run the server with the `--insecure` tag:
`python manage.py runserver --insecure`
This knowledge is made available for demonstration purposes, and the app prototype should not be deployed in this manner. A fix to securely load the map will be released in iWEB v2.0.

