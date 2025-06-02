#### Setup ####
###Imports###
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
subprocess.run(['printf " " | pecl install mongodb'], shell=True)
print("Adding mongodb.so extensions to php file")
with open("/etc/php/8.3/cli/php.ini", "a") as file:
    file.write("\nextension=mongodb.so")
print("Installing libapache-php")
subprocess.run(['apt install -y libapache2-mod-php8.3'], shell=True)
print("Adding mongodb.so extensions to libapache-php file")
with open("/etc/php/8.3/apache2/php.ini", "a") as file:
    file.write("\nextension=mongodb.so")
print("Installing Composer")
subprocess.run(['apt install -y composer'], shell=True)


####### PingMaker Monitoring Script Installation #######
print("------ Setting up PingMaker Service ------")
print("Making directories")
subprocess.run(['mkdir /home/PingMaker'], shell=True)
print("Downloading Script and Service file")
subprocess.run(['wget https://raw.githubusercontent.com/DominicKavalary/PingMaker4/refs/heads/main/PingAndTrace.py -P /home/PingMaker'], shell=True)
subprocess.run(['wget https://raw.githubusercontent.com/DominicKavalary/PingMaker4/refs/heads/main/PingMaker.service -P /etc/systemd/system/'], shell=True)
print("Installing pymongo and traceroute")
subprocess.run(['apt install -y python3-pymongo'], shell=True)
print("Downloading and running database innitialization script")
subprocess.run(['wget https://raw.githubusercontent.com/DominicKavalary/PingMaker4/refs/heads/main/PingSetup2.py -P /home/PingMaker'], shell=True)
subprocess.run(['python3 /home/PingMaker/PingSetup2.py'], shell=True)
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
print("Downloading required web pages")
subprocess.run(['wget https://raw.githubusercontent.com/DominicKavalary/PingMaker4/refs/heads/main/index.html -P /var/www/html/'], shell=True)
subprocess.run(['wget https://raw.githubusercontent.com/DominicKavalary/PingMaker4/refs/heads/main/style.css -P /var/www/html/'], shell=True)
subprocess.run(['wget https://raw.githubusercontent.com/DominicKavalary/PingMaker4/refs/heads/main/users.php -P /var/www/html/'], shell=True)
subprocess.run(['wget https://raw.githubusercontent.com/DominicKavalary/PingMaker4/refs/heads/main/request.php -P /var/www/html/'], shell=True)
subprocess.run(['wget https://raw.githubusercontent.com/DominicKavalary/PingMaker4/refs/heads/main/targets.php -P /var/www/html/'], shell=True)
subprocess.run(['wget https://raw.githubusercontent.com/DominicKavalary/PingMaker4/refs/heads/main/status.php -P /var/www/html/'], shell=True)
subprocess.run(['wget https://raw.githubusercontent.com/DominicKavalary/PingMaker4/refs/heads/main/home.php -P /var/www/html/'], shell=True)
subprocess.run(['wget https://raw.githubusercontent.com/DominicKavalary/PingMaker4/refs/heads/main/login.php -P /var/www/html/'], shell=True)
subprocess.run(['wget https://raw.githubusercontent.com/DominicKavalary/PingMaker4/refs/heads/main/phpfunctions.php -P /var/www/html/'], shell=True)
subprocess.run(['wget https://raw.githubusercontent.com/DominicKavalary/PingMaker4/refs/heads/main/logout.php -P /var/www/html/'], shell=True)
print("Composer Require step")
subprocess.run(['cd /var/www/html/ && composer require mongodb/mongodb'], shell=True)
print("Downloading and running SSL config setup script")
subprocess.run(['wget https://raw.githubusercontent.com/DominicKavalary/PingMaker4/refs/heads/main/PingSetup3.py -P /home/PingMaker'], shell=True)
subprocess.run(['python3 /home/PingMaker/PingSetup3.py'], shell=True)

####### Done #######
print("------ Innitial Setup Complete ------")

