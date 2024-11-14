#### Setup ####
###Imports###
import time
import threading
import subprocess
import ipaddress
import re
import os
import random
import pymongo
import datetime

#### Function to turn cli output into an array, each line being an item in the array###
def getOutput(Command):
  output = subprocess.getoutput(Command)
  output = output.splitlines()
  return output

### Function to write errors to our error file 
def errWrite(Message):
  with open("/home/PingMaker/errors/Errors.txt", "a") as errfile:
    errfile.write("\n"+Message)

#### Function to do a quick address format validation on the targets in the target file. X.X.X.X and XXX.XXX(sorta) for ips and hostnames###
def testTargetRegex(Target):
  regex = r"^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$"
  if re.search(regex, Target):
    return True
  else:
    regex = "[a-zA-Z0-9@:%._\\+~#?&//=]{2,256}\\.[a-z]" + "{2,6}\\b([-a-zA-Z0-9@:%._\\+~#?&//=]*)"
    if re.search(regex,Target):
      return True
    else:
      errWrite("Regex test failed for: " + Target)
      return False
  
### Function to get targets from target file. then parse through them and remove bad ones
def getTargets():
# Create empty list of targets, then go through the target file to find them
  ListOfTargets = []
  with open("/home/PingMaker/PingTargets.txt", "r") as targetFile:
    for line in targetFile:
      # If there is a /, it means there is a cidr address range. Get the addresses and add them all
      if "/" in line:
        usableSubnet = [str(ip) for ip in ipaddress.IPv4Network(line.replace("\n",""))]
        for ip in usableSubnet[1:-1]:
          ListOfTargets.append(str(ip))
      # Otherwise, if there is no /, it means it is either an IP or a hostname.
      else:
        ListOfTargets.append(line.replace("\n",""))
  #Now, run Regex checks on every target in order to have a quick validation. This will not grab all of the bad ones, but it will do most. Later, we will have methods to kill processes if they end up being bad so that it doesnt waste cpu.
  ListOfBadTargets = []
  for Target in ListOfTargets:
    # if they pass the initial tests, create their directories
    if not testTargetRegex(Target):
      ListOfBadTargets.append(Target)
  # now remove every bad target from our list
  for Target in ListOfBadTargets:
    ListOfTargets.remove(Target)
  ## Return the list of targets
  return ListOfTargets

### Function to create needed directories and error file for code to work
def makeDirectories():
  subprocess.run(["mkdir", "/home/PingMaker/errors"])
  subprocess.run(["touch", "/home/PingMaker/errors/Errors.txt"])

### Function to create and set up database
def databaseSetup():
  client = pymongo.MongoClient(host="localhost", port=27017)
  db = client["database"]
  collection = db["collection"]
  collection.create_index([("createdAt", 1)], expireAfterSeconds=604800)
  client.close()
  
### Function to do a ping command, and return the output as an array of values. The array is: the time of ping, the packet loss, the response time, and any note outputted by the command#
def getPingArray(Target):
  # set up of variables and grabbing the result of the ping
  timeOfPing = time.strftime("%D:%H:%M:%S")
  packetLoss = "NA"
  responseTime = "NA"
  errorNote= "NA"
  output = getOutput("ping -c 1 " + Target)
  #parsing through results of ping to grab data. It will grab packet loss, response time, and any error it finds. It will then return the output
  for line in output:
    if "% packet loss" in line and "errors" not in line:
      packetLoss = line.split(', ')[2].split(" ")[0]
    elif "errors" in line:
      packetLoss = line.split(', ')[3].split(" ")[0]
    elif "Host Unreachable" in line or "Temporary failure" in line or "Name or service" in line or "Network is unreachable" in line:
      errorNote = line
    elif "bytes from" in line:
      responseTime = line[line.find("time=")+5:]
  return [timeOfPing,packetLoss,responseTime,errorNote]

### Function to be threaded. This function handles the main process of pinging and storing file data
def PingMaker(Target):
  # Error Count, this is to count total errors, if total errors of a certain kind happen often, it will close the thread because it will nto ever succede
  errorCount = 0
  # Setting up the while statement to always run and continuously try pinging, otherwise if the event happens it will break the loop#
  knownService = True
  while knownService:
    # Grab the info from a the ping output function
    pingArray = getPingArray(Target)
    # establish connection with DB
    client = pymongo.MongoClient(host="localhost", port=27017)
    db = client["database"]
    collection = db["collection"]
    # format data for DB insertion
    data = {
      "Target": Target,
      "timeOfPing": pingArray[0],
      "packetLoss": pingArray[1],
      "responseTime": pingArray[2],
      "errorNote": pingArray[3],
      "createdAt": datetime.datetime.now(timezone.utc)
    }
    # insert data
    collection.insert_one(data)
    # close connection so theres not a million files open
    client.close()
    # if there was an error note created, add to the count. , if a large amount has happened, make a note of it. if the name or service isnt known, assume its bad input and close the process so it doesnt take up cpu
    if "NA" not in pingArray[3]:
      errorCount += 1
      if "Name or service not known" in pingArray[3]:
        errWrite("Name or service not known for target: "+Target+", validate target format\nEnding thread for target "+Target+" under the assumption of an improper target")
        knownService = False
      if errorCount == 750:
        errWrite("Excessive errors for: " + Target)
        errorCount = 0
    #tell the program to wait a second. this is because a succesfull ping will generally happen pretty quick, and errors depending on which kind can show up immediatly. so this will limit the pings/errors to about one every one or two seconds. 
    time.sleep(1)

########    ----   MAIN     ----    ####### MAYBE DO THE IF MAIN THING#
# sets up needed directories
makeDirectories()
# Get list of targets
ListOfTargets = getTargets()
# sets up mongodb database with required database name, collection name, and ttl to do record rotation
databaseSetup()
# Start a thread per target. Each thread will ping the target and log to their own files. spreads the starting of threads by waiting fractions of a second so that the pings dont all happen liek once like a firing squad and mess up the cpu
for Target in ListOfTargets:
  PingThread = threading.Thread(target=PingMaker, args=(Target,))
  PingThread.start()
  time.sleep(random.random()/3)
