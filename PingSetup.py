#### Setup ####
###Imports###
import pymongo
import hashlib
import subprocess


####### MongoDB Setup #######
print("------ Installing MongoDB-org ------")
subprocess.run(['apt-get install -y gnupg curl'], shell=True)
subprocess.run(['curl -fsSL https://www.mongodb.org/static/pgp/server-8.0.asc | sudo gpg -o /usr/share/keyrings/mongodb-server-8.0.gpg  --dearmor'], shell=True)
subprocess.run(['echo "deb [ arch=amd64,arm64 signed-by=/usr/share/keyrings/mongodb-server-8.0.gpg ] https://repo.mongodb.org/apt/ubuntu noble/mongodb-org/8.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-8.0.list'], shell=True)
subprocess.run(['apt-get update'], shell=True)
subprocess.run(['apt-get install -y mongodb-org'], shell=True)
print("Enabling and starting mongod")
subprocess.run(['systemctl enable mongod'], shell=True)
subprocess.run(['systemctl start mongod'], shell=True)


####### MongoDB PHP Installation #######
print("------ Installing PHP and Pecl Installing Mongodb ------")
subprocess.run(['apt install -y php-dev'], shell=True)
subprocess.run(['pecl install -y mongodb'], shell=True)
print("Adding mongodb.so extensions to php file")
with open("example.txt", "a") as file:
    file.write("\nextension=mongodb.so")
print("Installing libapache-php")
subprocess.run(['apt install libapache2-mod-php8.3'], shell=True)
print("Adding mongodb.so extensions to libapache-php file")
with open("/etc/php/8.3/apache2/php.ini", "a") as file:
    file.write("\nextension=mongodb.so")
print("Installing Composer")
subprocess.run(['apt install composer'], shell=True)


####### PingMaker Monitoring Script Installation #######
print("------ Setting up PingMaker Service ------")
print("Making directories")
subprocess.run(['mkdir /home/PingMaker'], shell=True)
subprocess.run(['cd /home/PingMaker'], shell=True)
print("Downloading Script and Service file")
subprocess.run(['wget https://raw.githubusercontent.com/DominicKavalary/PingMaker4/refs/heads/main/PingAndTrace.py'], shell=True)
subprocess.run(['wget https://raw.githubusercontent.com/DominicKavalary/PingMaker4/refs/heads/main/PingMaker.service -P /etc/systemd/system/'], shell=True)
print("Installing pymongo and traceroute")
subprocess.run(['apt install -y python3-pymongo'], shell=True)
subprocess.run(['apt install -y traceroute'], shell=True)
print("Enbaling service and reloading daemon")
subprocess.run(['systemctl enable PingMaker.service'], shell=True)
subprocess.run(['systemctl daemon-reload'], shell=True)
subprocess.run(['systemctl start PingMaker.service'], shell=True)


####### Apache2 Install and Setup #######
print("------ Apache2 install and Front end Setup ------")
print("Installing Apache2")
subprocess.run(['apt update'], shell=True)
subprocess.run(['apt install apache2'], shell=True)
subprocess.run(['rm /var/www/html/index.html'], shell=True)
subprocess.run(['cd /var/www/html/'], shell=True)
print("Downloading required web pages")
subprocess.run(['wget https://raw.githubusercontent.com/DominicKavalary/PingMaker4/refs/heads/main/index.html'], shell=True)
subprocess.run(['wget https://raw.githubusercontent.com/DominicKavalary/PingMaker4/refs/heads/main/style.css'], shell=True)
subprocess.run(['wget https://raw.githubusercontent.com/DominicKavalary/PingMaker4/refs/heads/main/users.php'], shell=True)
subprocess.run(['wget https://raw.githubusercontent.com/DominicKavalary/PingMaker4/refs/heads/main/request.php'], shell=True)
subprocess.run(['wget https://raw.githubusercontent.com/DominicKavalary/PingMaker4/refs/heads/main/targets.php'], shell=True)
subprocess.run(['wget https://raw.githubusercontent.com/DominicKavalary/PingMaker4/refs/heads/main/status.php'], shell=True)
subprocess.run(['https://raw.githubusercontent.com/DominicKavalary/PingMaker4/refs/heads/main/home.php'], shell=True)
subprocess.run(['https://raw.githubusercontent.com/DominicKavalary/PingMaker4/refs/heads/main/login.php'], shell=True)
subprocess.run(['https://raw.githubusercontent.com/DominicKavalary/PingMaker4/refs/heads/main/phpfunctions.php'], shell=True)
subprocess.run(['https://raw.githubusercontent.com/DominicKavalary/PingMaker4/refs/heads/main/logout.php'], shell=True)
print("Composer Require step")
subprocess.run(['composer require mongodb/mongodb'], shell=True)


####### Innitializing Database and Adding Default Admin User #######
print("------ Creating default admin user and innitializing database tables ------")
Username = "admin"
Password = "admin"
Password = hashlib.sha256(Password.encode('utf-8')).hexdigest()
AdminUser = { "Username": Username, "Password": Password, "Role": "Admin" }
client = pymongo.MongoClient(host="localhost", port=27017)
db = client["database"]
collection = db["targets"]
collection = db["errors"]
collection.create_index([("createdAt", 1)], expireAfterSeconds=604800)
collection = db["collection"]
collection.create_index([("createdAt", 1)], expireAfterSeconds=604800)
collection = db["users"]
collection.insert_one(AdminUser)
collection = db["traceroutes"]
collection.create_index([("createdAt", 1)], expireAfterSeconds=604800)
collection = db["tracemaps"]
client.close()
print("------ Innitial Setup Complete ------")
