# PingMaker4
pingmaker3 but attempted to add database stuff and maybe web stuff

## Time set up
### Ubuntu Server (Tested on Noble)
- timedatectl set-timezone ENTERTIMEZONEHERE

## Installaton
### Ubuntu Server (Tested on Noble)
- Obtain Setup File
```
wget https://raw.githubusercontent.com/DominicKavalary/PingMaker4/refs/heads/main/PingSetup.py
```
- Run the file as root/with sudo
```
python3 PingSetup.py
```
## If youd like extra security on the webpage with php session stuff modify the php ini file options like below
- nano /etc/php/8.3/apache2/php.ini
```
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
```

  
## Now to enable our server to use SSH with a self signed cert
- sudo a2enmod ssl
- sudo systemctl restart apache2
- sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /etc/ssl/private/apache-selfsigned.key -out /etc/ssl/certs/apache-selfsigned.crt
- When you are prompted to, make the "Common Name" the IP or hostname of the server, the rest isnt that important
- sudo nano /etc/apache2/sites-available/192.168.1.1.conf
- 	Make the site-available file the hostname or ip of your server, and paste this in after editing the IP
```
<VirtualHost *:443>
   ServerName 192.168.1.1
   DocumentRoot /var/www/html

   SSLEngine on
   SSLCertificateFile /etc/ssl/certs/apache-selfsigned.crt
   SSLCertificateKeyFile /etc/ssl/private/apache-selfsigned.key
</VirtualHost>
<VirtualHost *:80>
	ServerName 192.168.1.1
	Redirect / https://192.168.1.1/
</VirtualHost>
```
- sudo a2ensite 192.168.1.1.conf
- sudo systemctl reload apache2


# Things of note
- Depending on the amount of targets, and how long you want to keep data for, you want you may need to increase:
-   Disk Size
-   Memory
-   CPU


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


### Possibly i dunno yet well see, there is a potential issue of the maximum oamoutn of files open at the same time, i think these can help
go to /etc/security/limits.conf and add:
mongodb soft nofile 64000
mongodb hard nofile 64000

set to 100000

sudo nano /etc/sysctl.conf
fs.file-max = 2097152
sudo sysctl -p

sudo nano /etc/pam.d/common-session
session required pam_limits.so
