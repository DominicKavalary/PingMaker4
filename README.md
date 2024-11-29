# PingMaker4
pingmaker3 but attempted to add database stuff and maybe web stuff



## MongoDB Installation For Monitoring Database
### Ubuntu Server (Tested on Noble)
- sudo apt-get install gnupg curl
- curl -fsSL https://www.mongodb.org/static/pgp/server-8.0.asc | sudo gpg -o /usr/share/keyrings/mongodb-server-8.0.gpg  --dearmor
- echo "deb [ arch=amd64,arm64 signed-by=/usr/share/keyrings/mongodb-server-8.0.gpg ] https://repo.mongodb.org/apt/ubuntu noble/mongodb-org/8.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-8.0.list
- sudo apt-get update
- sudo apt-get install -y mongodb-org
- sudo systemctl enable mongod
- sudo systemctl start mongod

####Possibly i dunno yet well see
go to /etc/security/limits.conf and add:
mongodb soft nofile 64000
mongodb hard nofile 64000

set to 100000

sudo nano /etc/sysctl.conf
fs.file-max = 2097152
sudo sysctl -p

sudo nano /etc/pam.d/common-session
session required pam_limits.so

## MongoDB PHP Setup
### Ubuntu Server (Tested on Noble)
- sudo apt install php-dev
- sudo pecl install mongodb
-  - do all default options when they appear by just clicking enter
- locate your php ini file using the command "php --ini" it is labeled as loaded configuration file
- edit that file and add the line "extension=mongodb.so"

## PingMaker Monitoring Script Setup
### Ubuntu Server (Tested on Noble)
- sudo su
- mkdir /home/PingMaker
- cd /home/PingMaker
- wget https://raw.githubusercontent.com/DominicKavalary/PingMaker4/refs/heads/main/PingMaker4.py
- nano /etc/systemd/system/PingMaker.service
- - Copy paste the contents of the PingMaker.service file in the repository
- apt install python3-pymongo
- systemctl enable PingMaker.service
- systemctl daemon-reload
- systemctl start PingMaker.service

## Apache2 Install And Front End Setup
### Ubuntu Server (Tested on Noble)
- sudo apt update
- sudo apt install apache2
Test if you can rach apache server with address of ubuntu server
- rm /var/www/html/index.html
- wget https://raw.githubusercontent.com/DominicKavalary/PingMaker4/refs/heads/main/index.html -P /var/www/html/
- wget https://raw.githubusercontent.com/DominicKavalary/PingMaker4/refs/heads/main/targets.html -P /var/www/html/
- wget https://raw.githubusercontent.com/DominicKavalary/PingMaker4/refs/heads/main/request.html -P /var/www/html/
- wget https://raw.githubusercontent.com/DominicKavalary/PingMaker4/refs/heads/main/style.css -P /var/www/html/
- wget https://raw.githubusercontent.com/DominicKavalary/PingMaker4/refs/heads/main/request.php -P /var/www/html/
- wget https://raw.githubusercontent.com/DominicKavalary/PingMaker4/refs/heads/main/remtargets.php -P /var/www/html/
- wget https://raw.githubusercontent.com/DominicKavalary/PingMaker4/refs/heads/main/addtargets.php -P /var/www/html/








# Todo:
security logins
css
javascript?
check if target exists before attempting to delete
make targets.html php and just list targets at end with no functions
