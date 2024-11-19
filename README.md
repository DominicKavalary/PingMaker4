# PingMaker4
pingmaker3 but attempted to add database stuff and maybe web stuff


## PingMaker Monitoring Script Setup
# Ubuntu Server (Tested on Noble)
- sudo su
- mkdir /home/PingMaker
- cd /home/PingMaker
- wget https://raw.githubusercontent.com/DominicKavalary/PingMaker4/refs/heads/main/PingMaker.py
- nano /etc/systemd/system/PingMaker.service
  Copy paste the contents of the PingMaker.service file in the repository
- systemctl enable PingMaker.service
- systemctl daemon-reload

## MongoDB Installation For Monitoring Database
# Ubuntu Server (Tested on Noble)




# TODO
- css
- security
- update target info
- - uniform web design
  - maybe use javascript and node js instread of php
