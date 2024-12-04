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

### "Global" list of targets removed, processes will periodically check to see if their target is in this list, if it is, they will end their processes.  ###
removedTargets = []

### Function to compare old list of targets and new list of targets and return targets that have been added or removed. Please for the love of god future dom, please do past dom a solid and make this more efficient than what you have come up with in your deranged state
def compareTargets(oldTargets, newTargets):
  # take targets from each and compare the sets
  new_list = []
  old_list = []
  for item in newTargets:
    new_list.append(item[0])
  for item in oldTargets:
    old_list.append(item[0])
  new_set = set(new_list)
  old_set = set(old_list)
  # Now get the TargetItems from their respective lists by getting the added fromt he new list and the removed from the old list
  added_list = new_set - old_set
  removed_list = old_set - new_set
  addedArray = []
  removedArray = []
  for item in newTargets:
    if item[0] in added_list:
      addedArray.append(item)
  for item in oldTargets:
    if item[0] in removed_list:
      removedArray.append(item)
  return addedArray, removedArray
  
### Function to turn cli output into an array, each line being an item in the array###
def getOutput(Command):
  output = subprocess.getoutput(Command)
  output = output.splitlines()
  return output

### Function to write errors to our error file 
def errWrite(Message):
  with open("/home/PingMaker/errors/Errors.txt", "a") as errfile:
    errfile.write("\n"+Message)

#### Function to do a quick address format validation on the targets in the target file. X.X.X.X and XXX.XXX(sorta) for ips and hostnames####
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
  
### Function to get targets from target file. then parse through them and remove bad ones. EVentually move the regex checking to the php file targets.php, eventually add a note variable to the target collection documents and add to that note if the regex failed or not so they can see it in the web table when i make that
def getTargets():
# Set up database connection to grab targets
  client = pymongo.MongoClient(host="localhost", port=27017)
  db = client["database"]
  collection = db["targets"]
  targetDocuments = collection.find({})
  client.close()
# create empty list of targets
  ListOfTargets = []
  # for every document in the target collection, grab the target and the Delay
  for document in targetDocuments:
    Target = document['Target']
    #Now, run Regex checks on every target in order to have a quick validation. This will not grab all of the bad ones, but it will do most. Later, we will have methods to kill processes if they end up being bad so that it doesnt waste cpu.
    if testTargetRegex(Target):
      Delay = int(document['Delay'])
      TargetItem = [Target, Delay]
      ListOfTargets.append(TargetItem)
  return ListOfTargets

### Function to create needed directories and error file for code to work
def makeDirectories():
  subprocess.run(["mkdir", "/home/PingMaker/errors"])
  subprocess.run(["touch", "/home/PingMaker/errors/Errors.txt"])

### Function to create and set up database
def databaseSetup():
  client = pymongo.MongoClient(host="localhost", port=27017)
  db = client["database"]
  collection = db["targets"]
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
def PingMaker(Target, Delay):
  # Error Count, this is to count total errors, if total errors of a certain kind happen often, it will close the thread because it will nto ever succede
  errorCount = 0
  # Setting up the while statement to always run and continuously try pinging, otherwise if the event happens it will break the loop#
  keepProcessRunning = True
  while keepProcessRunning:
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
      "createdAt": datetime.datetime.now(datetime.timezone.utc)
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
        keepProcessRunning = False
      if errorCount == 750:
        errWrite("Excessive errors for: " + Target)
        errorCount = 0
    # check if its in the list of removed targets, if it is, set the keepprocessrunning flag to false and remove the target from that list
    if Target in removedTargets:
      keepProcessRunning = False
      removedTargets.remove(Target)
    # tell the program to wait the delay period. this is because a succesfull ping will generally happen pretty quick, and errors depending on which kind can show up immediatly. so this will limit the pings/errors to about one every one or two seconds. 
    time.sleep(Delay)


########    ----   MAIN     ----    ####### MAYBE DO THE IF MAIN THING#
# sets up needed directories
makeDirectories()
# sets up mongodb database with required database name, collection names, and ttl to do record rotation
databaseSetup()
# Get list of targets
ListOfTargets = getTargets()
# Start a thread per target. Each thread will ping the target and log to their own files. spreads the starting of threads by waiting fractions of a second so that the pings dont all happen liek once like a firing squad and mess up the cpu
for TargetItem in ListOfTargets:
  PingThread = threading.Thread(target=PingMaker, args=(TargetItem[0],TargetItem[1],))
  PingThread.start()
  time.sleep(random.random()/3)

# now check forever every 5 minutes wether the target collection has changed or not. if it has, you know a target has been removed or added
while 1 == 1:
  time.sleep(300)
  newTargets = getTargets()
  if ListOfTargets != newTargets:
    added, removed = compareTargets(ListOfTargets, newTargets)
    # if length of added is 1 or more, start the process for everything in added
    if len(added) >=1:
      for TargetItem in added:
        if testTargetRegex(TargetItem[0]):
          PingThread = threading.Thread(target=PingMaker, args=(TargetItem[0],TargetItem[1],))
          PingThread.start()
          time.sleep(random.random()/3)
    # if length of removed is 1 or more, add the names to the removed targets list, which processes will periodically check to see fi they need to be shut down
    if len(removed) >=1:
      for TargetItem in removed:
        removedTargets.append(TargetItem[0])
    ListOfTargets = newTargets

