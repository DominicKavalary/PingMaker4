# PingMaker4
pingmaker3 but attempted to add database stuff and maybe web stuff

## Time set up
### Ubuntu Server (Tested on Noble)
- timedatectl set-timezone ENTERTIMEZONEHERE

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
#### If youd like extra security on the webpage with php session stuff do the below
-- nano /etc/php/8.3/apache2/php.ini
-- session.use_strict_mode = 1
-- file_uploads = Off
-- disable_functions = system, shell_exec, passthru, phpinfo, show_source, highlight_file, popen, proc_open, fopen_with_path, dbmopen, dbase_open, putenv, move_uploaded_file, chdir, mkdir, rmdir, chmod, rename, filepro, filepro_rowcount, filepro_retrieve, posix_mkfifo
-- session.sid_length = 150
-- session.name = PingMakerPHPSESSID
-- session.cookie_lifetime = 600
-- session.cookie_httponly = 1
-- session.cookie_samesite = Strict
-- session.cookie_secure = 1
-- session.sid_bits_per_character = 6

## PingMaker Monitoring Script Setup
### Ubuntu Server (Tested on Noble)
- sudo su
- mkdir /home/PingMaker
- cd /home/PingMaker
- wget https://raw.githubusercontent.com/DominicKavalary/PingMaker4/refs/heads/main/PingAndTrace.py
- wget https://raw.githubusercontent.com/DominicKavalary/PingMaker4/refs/heads/main/PingSetup.py
- nano /etc/systemd/system/PingMaker.service
- - Copy paste the contents of the PingMaker.service file in the repository
- apt install python3-pymongo
- apt install traceroute -y
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
- wget https://raw.githubusercontent.com/DominicKavalary/PingMaker4/refs/heads/main/logout.php
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


## Things of note
- Depending on the amount of targets, and how long you want to keep data for, you want you may need to increase:
-   Disk Size
-   Memory
-   CPU

# 135.5 mongo 136.6
# 30.9 PingMaker
### Generally, a targets being pinged every second for a day will take up
- UNKNOWN AMOUNT OF CPU at any time
- Memory: 180 + 
- UNKNOWN GB STORAGE at the end of the day

Use these semi accurate kinda metrics to calculate your needs. If you ping every second multiply by roughly 5 i think




# Todo:
- database user created for database interactions
- css
- 	- onclick button effects
- validate user input on forms, possibly keep doing it in the python script like do delay tests to see if delay is valid
- - stress test
- move target and user actions to the phpfucntions somehow? i dont like the idea of you submitting your own page over and over again. eh who knows though
- Just learned that the mongodb connection made by php probably dont close. they maybe persist accross sessions so maybe i just need to make one on succesfull login
- add more duration between when new targets are spun up in that ending while loop
- also maybe add additional security by not just checking if the session is logged in, but also if the IP has changed or anything like that to try and further prevent session stealing
- DO if name == main for better stuff?
- possibly also make a main file, and make a pingmaker file and a tracemaker file and import the two into main and just have if main in the main
- figure out how to do batch processing for less database connections, and look into data streaming with mongodb so you dont have to check every 5 minutes, you wait on target database update to do the new and remove targets stuff
- learn docker and make a docker container for db, for scripts, and for web. autoscaling resources?
