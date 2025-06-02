###Imports###
import subprocess

####### SSL Setup #######
hostname = "pingmaker.local"
subprocess.run([f'hostname {hostname}'], shell=True)
subprocess.run(['a2enmod ssl'], shell=True)
subprocess.run(['systemctl restart apache2'], shell=True)
subprocess.run([f'openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /etc/ssl/private/apache-selfsigned.key -out /etc/ssl/certs/apache-selfsigned.crt -subj "/C=US/ST=None/L=None/O=None/OU=None/CN={hostname}"'], shell=True)
subprocess.run(['touch /etc/apache2/sites-available/ssl-selfsigned.conf'], shell=True)
ssl_conf = f"""
<VirtualHost *:443>
   ServerName {hostname}
   DocumentRoot /var/www/html

   SSLEngine on
   SSLCertificateFile /etc/ssl/certs/apache-selfsigned.crt
   SSLCertificateKeyFile /etc/ssl/private/apache-selfsigned.key
</VirtualHost>
<VirtualHost *:80>
	ServerName {hostname}
	Redirect / https://{hostname}/
</VirtualHost>
"""
with open("/etc/apache2/sites-available/ssl-selfsigned.conf", "a") as file:
    file.write(ssl_conf)
subprocess.run(['a2ensite ssl-selfsigned.conf'], shell=True)
subprocess.run(['shutdown -r now'], shell=True)



