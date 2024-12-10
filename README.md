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
- 	do all default options when they appear by just clicking enter
- locate your php ini file using the command "php --ini" it is labeled as loaded configuration file
	- - edit that file and add the line "extension=mongodb.so"
- sudo apt install libapache2-mod-php8.3
- nano /etc/php/8.3/apache2/php.ini
- 	edit that file and add the line "extension=mongodb.so"
- sudo apt install composer
- MORE PHP STUFF
- session.use_strict_mode = 1

## PingMaker Monitoring Script Setup
### Ubuntu Server (Tested on Noble)
- sudo su
- mkdir /home/PingMaker
- cd /home/PingMaker
- wget https://raw.githubusercontent.com/DominicKavalary/PingMaker4/refs/heads/main/PingMaker.py
- wget https://raw.githubusercontent.com/DominicKavalary/PingMaker4/refs/heads/main/PingSetup.py
- nano /etc/systemd/system/PingMaker.service
- - Copy paste the contents of the PingMaker.service file in the repository
- apt install python3-pymongo
- python3 PingSetup.py
- 	Will ask you to input a username and password for the admin account
- systemctl enable PingMaker.service
- systemctl daemon-reload
- systemctl start PingMaker.service

## Apache2 Install And Front End Setup
### Ubuntu Server (Tested on Noble)
- sudo apt update
- sudo apt install apache2
- 	Test if you can rach apache server with address of ubuntu server
- rm /var/www/html/index.html
- cd /var/www/html/
- wget https://raw.githubusercontent.com/DominicKavalary/PingMaker4/refs/heads/main/index.html
- wget https://raw.githubusercontent.com/DominicKavalary/PingMaker4/refs/heads/main/style.css
- wget https://raw.githubusercontent.com/DominicKavalary/PingMaker4/refs/heads/main/users.php
- wget https://raw.githubusercontent.com/DominicKavalary/PingMaker4/refs/heads/main/request.php
- wget https://raw.githubusercontent.com/DominicKavalary/PingMaker4/refs/heads/main/targets.php
- wget https://raw.githubusercontent.com/DominicKavalary/PingMaker4/refs/heads/main/status.php
- wget https://raw.githubusercontent.com/DominicKavalary/PingMaker4/refs/heads/main/home.php
- wget https://raw.githubusercontent.com/DominicKavalary/PingMaker4/refs/heads/main/login.php
- wget https://raw.githubusercontent.com/DominicKavalary/PingMaker4/refs/heads/main/phpfunctions.php
- composer require mongodb/mongodb
#### Now to enable our server to use SSH with a self signed cert
- sudo a2enmod ssl
- sudo systemctl restart apache2
- sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /etc/ssl/private/apache-selfsigned.key -out /etc/ssl/certs/apache-selfsigned.crt
- 	When you are prompted to, make the "Common Name" the IP or hostname of the server, the rest isnt that important
- sudo nano /etc/apache2/sites-available/192.168.150.134.conf
- 	Make the site-available file the hostname or ip of your server, and paste this in
'''
<VirtualHost *:443>
   ServerName 192.168.150.134
   DocumentRoot /var/www/html

   SSLEngine on
   SSLCertificateFile /etc/ssl/certs/apache-selfsigned.crt
   SSLCertificateKeyFile /etc/ssl/private/apache-selfsigned.key
</VirtualHost>
<VirtualHost *:80>
	ServerName 192.168.150.134
	Redirect / https://192.168.150.134/
</VirtualHost>
'''
- sudo a2ensite 192.168.150.134.conf
- sudo systemctl reload apache2
### Uknown if needed
- sudo ufw allow "Apache Full"





## Things of note
- Depending on the amount of targets, and how long you want to keep data for, you want you may need to increase:
-   Disk Size
-   Memory
-   CPU
You can change the retention time in the python script when it innitialized some database stuff. The time is in seconds I beleive. You can also change hwo quickly this software pings by also changing the value in the python script. EXCEPT NOT FOR LONG I JUST HAD A GREAT IDEA. Gonna make it so when you add targets you also select the delay of pings in seconds and then the python script can get that information when the target pinging process is created.

Generally, 10 targets being pinged every 5 seconds for a day will take up
- UNKNOWN AMOUNT OF CPU at any time
- UNKNOWN GB MEMORY at any time
- UNKNOWN GB STORAGE at the end of the day

Use these semi accurate kinda metrics to calculate your needs. If you ping every second multiply by roughly 5 i think




# Todo:
- database user created for database interactions
- css
- validate user input on forms, possibly keep doing it in the python script like do delay tests to see if delay is valid
- - stress test
- move target and user actions to the phpfucntions somehow? i dont like the idea of you submitting your own page over and over again. eh who knows though
- add a php thing that grabs all your targets and makes select options for the requests page
- HAVE NOT TESTED MOST RECENT PINGMAKER CODE when i added the dictionary updates
- Make it so you cant remove the last admin user in the delete user function
