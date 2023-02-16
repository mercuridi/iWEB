# Database choice
*File for exploring justifications of which database system to use*
### General notes
- Each thread maintains its own connection. Therefore, the database must support at least as many simultaneous connections as you have worker threads.
	- Assume we have 100000 users, with a maximum concurrency of 1000.
- A worker thread is a model that pulls or uses the database in some way.
- Databases must conform to UTF-8 encoding to avoid errors in passing data between the database and Django.
## Options
Django officially supported databases:
- PostgreSQL
- MariaDB
- MySQL
- Oracle
- SQLite

### Default: SQLite
- Very fast as compared to full-fat SQL
- Embedded in application; no network capabilities!
- "Excellent development alternative for applications that are predominanty read-only or require a smaller installation footprint"
	- Note our application is *not* predominanty read only and also has no requirement for a small installation footprint.
	- SQLite does **not** support a "real decimal internal type"; decimal values are internally converted to the `REAL` data type, so they do not support correctly-rounded decimal floating point arithmetics 
		- We want to perform floating point arithmetics for our location handling. SQLite is likely not the best option.
- Designed to be lightweight; does not support high levels of concurrency
	- Huge problem for scalability
- Threads often claim exclusive locks across the entire database.
	- SQLite quickly becomes "too lite" for many real-world applications
	- We should switch backend before this becomes an issue
- Does not natively support JSON; must activate `JSON1` extension from the Python `sqlite3` library.

### MySQL
- Supports SSL out-of-box; 
- Extremely common for web apps that only require a data transactional database
- Supports the `POINT` datatype
- Scalable
- InnoDB framework; fast
- Concurrent
- Does not support Python out-of-box
- Free for personal use; commercial use requires paid license from Oracle

### MariaDB
- Extension of MySQL

### PostgreSQL
- Extremely robust
- Very fast
- Supports Python directly
- Common for enterprise-level databases
- Open source, strong community
- Object-relational; more restrictive in database construction

# Conclusion
- Migrate from SQLite to MySQL Community Edition
- Keep PostgreSQL as backup plan
- If possible, create a fork running PostgreSQL for proof-of concept (late stage)
