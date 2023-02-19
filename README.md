# iWEB
Repo for ECM2434 Group Software Engineering Project.

## Getting Started
### Starting the Django server
The Django server needs to have the SQL database running in the background.
To do this, SQL data is included in the repository in `/main/SQL_DATA/`. [These files can be reloaded into SQL](https://dev.mysql.com/doc/refman/5.7/en/reloading-sql-format-dumps.html)locally with a command such as `mysql < dump.sql`, run in the SQL_DATA directory.
This will run the SQL server in the backend, picking up the data from the dump file.
Run 'python manage.py runserver'

### Installing mySQL
If you are developing the server, you will need to have a local mySQL installation to pick up the backend of the web app. Instructions for installing mySQL can be found [here](https://dev.mysql.com/doc/mysql-installation-excerpt/5.7/en/installing.html), at the mySQL developer documentation. This wiki covers installation on all major operating systems.

The project is built on mySQL v8.0.32 Community Edition, x86.

#### mySQL Python integration
Django needs a Python-SQL interface to operate the database. This is provided by [mysqlclient](https://pypi.org/project/mysqlclient/), which can be installed with simple `pip` commands as detailed on the linked site.

## SQL maintenance
In order to update the SQL datadumps (**REQUIRED** before committing after any database change), you can run `mysqldump -u root -p IWEB > newdump.sql`, replacing `newdump` with the name of your dump file.
Note that this command must be run as `root` for your local SQL installation; user `iweb_dev` lacks the `PROCESS` privileges to dump the database in this way.
When you alter the database, ensure that a new dump file is created when you commit for groupmembers to be able to pick up the most recent version of the database.
