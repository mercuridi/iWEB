Please read this entire README file.
# iWEB
This is the second submission for Group 30's ECM2434 Group Software Engineering Project.
Project members:
    - Kai Barber-Harris
    - Dimitar Sivrev
    - Bethany Whiting (unavailable between 13/3/23 - 22/3/23)
    - Jude Goulding
    - Daria Sazonova
    - (no sixth member)

## Overview
iWEB is the internal name for our web app. The system encourages green, sustainable behaviour by making the information to act in such a way as easily available as possible and rewarding users for acting on it.

## Learning to use the app
As a user learning to use the front end of the app, we have written a help page accessible from the main page of the site. This appears as a hyperlink in the top right on the `/index` page once logged in. You may also access this help page without being logged in directly at `/help`.
The help page explains all the user-facing aspects of the project.
Gamekeepers have the job of handling user location reports and resetting the leaderboard once a week. The first of these jobs can be easily performed through the `/admin` page, and the second is handled through a special button only available to gamekeepers

## Technical details
iWEB's user-facing website is served by a Django web framework with custom views and functions.
The backend database is constructed in mySQL for release editions, and a database must be created and connected to in order for the site to function as intended. Optionally, you can load the packaged "test" database which includes a default admin account, a small set of "dummy" users, and aset of themes built in. The test database is best used to ensure iWEB is working to expected levels.

## Submission structure
This submission contains 3 primary folders, the GNU GPLv3 license, and this readme file.
Two of the folders are code submissions. The third is a miscellaneous folder with extra documentation and files.

### 1. app-mysql
The "app" folder contains all the source code and related files for iWEB to function; this is the "official" second release of iWEB.
A "Getting started" setup guide is included at the bottom of this readme file, if you wish to run the app yourself.

### 2. app-sqlite
For ease of use for marking, we have also included the development branch of iWEB running on an embedded SQLite database. This is simply a copy of our most recent update to the main repository on github.
We include this as the mySQL version can be tricky to set up even with a guide, and don't want to create unnecessary roadblocks to seeing our website as it should look; the two versions act exactly the same from the user's point of view.

#### How to run the SQLite version
The SQLite app can simply be run using the command `python manage.py runserver` in `./app-sqlite/iWEB`.

### 3. misc
The "misc" folder contains important files not directly related to the running of the app, but which should be included in the submission.
The first folder, "meeting-notes", contains screenshots of our Sprint 2 meeting notes we keep on Trello.
The second folder "trello" contains many screenshots of our Trello board across the second sprint to show we've been using it to track our progress. It also contains a gif compiling these screenshots into a looping slideshow, so you can see the usage of the trello across the project's second sprint.
Note that the numbers in brackets in the trello screenshots are the work units for that task: 1 work unit represents an estimated 1 hour of work.
In this folder there is also a PDF of detailed documentation for the map system as written by Dimitar, its programmer.

### Other resources
Also relevant to the project submission are our [github repository](https://github.com/Mercuridi/iWEB), [trello board](https://trello.com/b/xK5shoh4/project-sustainability), and [gitbook](https://dimitars-organization.gitbook.io/design-system/readme/summary).
If we've missed you and you need an invite to one of these, please contact Kai (kab237@exeter.ac.uk). 
The Github repository contains our project code's most up-to-date version and related branches. This is where we actively develop the project, and a commit history can be found there to track the progress of the project.
The Trello board tracks our project's day-to-day development and process. This is where we coordinate our work, alongside our Discord server where we actively communicate what we're working on and discuss implementation as we work.
The Gitbook contains further documentation for the map system.

## Getting started
### Requirements & dependencies
In order to run iWEB locally, there are certain dependencies that must be installed. Namely, these are Django, mySQL (server and client), whitenoise, and a system for HTTPS certification. Whitenoise is an open-source Python addon we use to serve static files in our site.
The requirements for the project can be installed from the command line; we assume you already have mySQL or SQLite3 installed, along with the Python package manager pip:
`pip install django`
`pip install whitenoise`
The Javascript testing suite also has extra `npm` dependencies. These are detailed in the "Running tests" section of this README. 

The HTTPS certification to run the server can be gotten from a Linux apt-connected command line with the following sequence of commands:
`apt install libnss3-tools`
`apt install mkcert`
`mkcert -install`
If you attempt to run `mkcert -install` without the appropriate dependencies, it will tell you what you're missing. Follow instructions from mkcert and ensure this step was successful before moving on.
From this point onwards, commands must be executed in the project's root directory. This is the same directory that `manage.py` is contained in.
`mkcert -cert-file cert.pem -key-file key.pem localhost 127.0.0.1`
`pip install django-extensions Werkzeug`
`pip install pyOpenSSL`

In order to run the server, Django must also be provided with a valid user to access a valid mySQL database. This section of the readme will guide you through creating these requirements, assuming you have the earlier named dependencies installed.

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
In the project directory, find the file `settings.py` at `./iWEB/app-mysql/iWEB/iWEB/settings.py`.
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
To pick up the test database, navigate to `./iWEB/app-mysql/iWEB` and run the following commands:
`python manage.py migrate --run-syncdb`
`python manage.py loaddata testdatabase.json`
This will populate the empty database we made in the mySQL command line client with the test database information. This database may still be modified later (write permissions are not affected).

#### Start from a fresh, empty database
To start from a fresh database, navigate to `./iWEB/app-mysql/iWEB` and simply run the command:
`python manage.py migrate`
This will construct the database schema required to run iWEB properly on the empty database we created in the mySQL command line client.

## Running the server
To run the server, navigate to `./iWEB/app-mysql/iWEB` and run the command:
`python manage.py runserver`
If all has gone well, this will open the server on the localhost which can be accessed through any web browser at `http://127.0.0.1:8000/`.
To run the HTTPS secure server, instead use the command `python3 manage.py runserver_plus 0.0.0.0:8000 --cert-file cert.pem --key-file key.pem`

## Running tests
To manually run the iWEB test suite, navigate to `./iWEB/app-mysql/iWEB` or `./iWEB/app-sqlite/iWEB` and run the command:
`python manage.py test tests/`
This will tell the Django test runner to search in the directory `tests/` for test files, which it should find and automatically execute, reporting results back to the terminal.
There is also a set of Javascript tests for the Javascript contained in `index.html`. To run these, navigate to the `tests/` directory from either side of the app and run these commands:
`npm install jest`
`npm install jest-environment-jsdom`
`npm test`
This will run the Javascript test suite.
