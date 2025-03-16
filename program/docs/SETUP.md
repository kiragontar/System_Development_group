# Setup process

## Database Setup:
1. Install Newest Mysql and Mysql Workbench Versions avaiable at [Mysql_Installation](https://dev.mysql.com/downloads/file/?id=536788) 
    - Once you install from this link, and when you are prompted select the "Full" installation version, this will automatically install workbench as well.
2. Open Workbench, Open the local instance with the username "root" 
    1. Head to User and Privallages on the left column.
    2. "Add account" --> Username: MickelUWE, Password--> g<bI1Z11iC]c --> apply.
    3. Leave User and Privallages and run the following Queries to give permission to the new user.
        ```sql
        GRANT ALL PRIVILEGES ON *.* TO 'MickelUWE'@'%';
        FLUSH PRIVILEGES;
        ```
    4. Exit back to main by clicking the house icon on the top left.
3. Create a new MYsql connection by clicking on the + icon.
    - Give the name of Connection Name to "Cinema"
    - Username should be MickelUWE
    - Password should be stored in vault and its the password g<bI1Z11iC]c
    - Test connection then select ok if all works.
4. Enter that connection, and run the following queries to create the database:
    - create database Cinema;
    - create database testdb;
5. That should be all for the database setup, if you encountered any issues please let me know.

## Installing Neccessary Imports:
Run the following on your terminal:
```bash
pip install bcrypt
pip install pytest
pip install mysql-connector-python
pip install sqlalchemy
pip install pillow
pip install pymysql
```
There may be more that you need to install so follow the errors if you get any.

## Verify:
To verify if everything is working well, head to app.py and run it, the result should be "✅ Successfully connected to the database!"
If that has worked, on your terminal head to the program directory
```bash
cd program
```
run the following command to check if the pytest is working well which in turn checks if the whole program is working well.
```bash
pytest .\tests
```