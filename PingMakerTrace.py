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
import json
### "Global" list of targets removed, processes will periodically check to see if their target is in this list, if it is, they will end their processes.  ###
removedTargets = {}
removedTraceTargets = {}
### Function to compare old list of targets and new list of targets and return targets that have been added or removed. 
def compareTargets(oldTargets, newTargets):
  # take targets from each and compare the sets. We need to know what targets were added, which were removed, and which stayed the same.
  new_set = set(newTargets)
  old_set = set(oldTargets)
  # get added by subtracting old from new, get removed by subtracking new from old, get the same using & operator. We need the same so we can check if the delays have changed on any, since the set stuff doesnt check if the delay changed. Still need to work on a way of ending the ping processes per target manually instead of letting these processesd contantly check the removedtargets list
  added_set = new_set - old_set
  removed_set = old_set - new_set
  same_set = new_set & old_set
  addedDict = {}
  removedDict = {}
  # go back and using the new and old dictionarys, recreate the key value pairs of target and delay
  for item in added_set:
    addedDict[item] = newTargets[item]
  for item in removed_set:
    removedDict[item] = oldTargets[item]
  for item in same_set:
    if oldTargets[item] != newTargets[item]:
      removedDict[item] = oldTargets[item]
      addedDict[item] = newTargets[item]
  return addedDict, removedDict
  
### Function to turn cli output into an array, each line being an item in the array###
def getOutput(Command):
  output = subprocess.getoutput(Command)
  output = output.splitlines()
  return output

### Function to write errors to our error file 
def errWrite(Target, Message):
  client = pymongo.MongoClient(host="localhost", port=27017)
  db = client["database"]
  collection = db["errors"]
  # format data for DB insertion
  data = {
    "Target": Target,
    "Error": Message,
    "Time": time.strftime("%D:%H:%M:%S"),
    "createdAt": datetime.datetime.now(datetime.timezone.utc)
  }
  # insert data
  collection.insert_one(data)
  client.close()

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
      errWrite(Target, "Regex test failed. Validate target format. Not spawning thread for target.")
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
  ListOfTargets = {}
  # for every document in the target collection, grab the target and the Delay
  for document in targetDocuments:
    Target = document['Target']
    #Now, run Regex checks on every target in order to have a quick validation. This will not grab all of the bad ones, but it will do most. Later, we will have methods to kill processes if they end up being bad so that it doesnt waste cpu.
    if testTargetRegex(Target):
      Delay = int(document['Delay'])
      ListOfTargets[Target] = Delay
  return ListOfTargets
  
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
        errWrite(Target, "Name or service not known, validate target format. Ending thread for target")
        keepProcessRunning = False
      if errorCount == 400:
        errWrite(Target, "Excessive errors")
        errorCount = 0
    # check if its in the list of removed targets, if it is and the delay matches, set the keepprocessrunning flag to false and remove the target from that list
    if Target in removedTargets and removedTargets[Target] == Delay:
      keepProcessRunning = False
      del removedTargets[Target]
    # tell the program to wait the delay period. this is because a succesfull ping will generally happen pretty quick, and errors depending on which kind can show up immediatly. so this will limit the pings/errors to about one every one or two seconds. 
    time.sleep(Delay)

### Traceroute Portion
def AddressInNextHop(Node, Address):
  print("Address in next hop:")
  print("Node")
  print(Node)
  print("Address: "+Address)
  if Address in Node["nexthops"]:
      return True
  return False

def AddHop(Node, Address):
  print("Adding Hop")
  print("Node to be added to")
  print(Node)
  print(Node)
  print("Address: "+Address)
  Node["nexthops"][Address] = {"nexthops": {}}

def CheckAndAdd(Node, HopList, Target):
  # set up a boolean to trip if soemthing is found
  FoundNewRoute = False
  CurrentNode = Node
  print("Goign through hoplist")
  for Address in HopList:
    if AddressInNextHop(CurrentNode, Address):
      print("same node found, moving on to this node")
      CurrentNode = CurrentNode["nexthops"][Address]
    else:
      print("New hop found, adding it")
      AddHop(CurrentNode, Address)
      CurrentNode = CurrentNode["nexthops"][Address]
      FoundNewRoute = True
  if FoundNewRoute == True:
    client = pymongo.MongoClient(host="localhost", port=27017)
    db = client["database"]
    collection = db["tracemaps"]
    collection.update_one({'Target' : Target}, { '$set' : { 'Tree' : Node }})
    client.close()

def printTree(Node, Count):
  for Address in Node["nexthops"]:
    print(('-' * Count) + Address)
    printTree(Node["nexthops"][Address], Count+1)


#TraceMaker frunction to get the route to your targets from the server
def TraceMaker(Target, Delay):
  # check if the tree has started being built. if not, built root node. regardless, set the Tracemap variable to be the current or new map
  client = pymongo.MongoClient(host="localhost", port=27017)
  db = client["database"]
  collection = db["tracemaps"]
  Tracemap = collection.find_one({'Target': Target})
  if not Tracemap:
    roottraceobject = {"nexthops": {}}
    data = {
      "Target": Target,
      "Tree": roottraceobject
    }
    print(data)
  # insert data
    collection.insert_one(data)
    Tracemap = data
  client.close()
  # Set up the loop to keep doing traceroutes
  keepProcessRunning = True
  while keepProcessRunning:
  # setting up array for hops to go in
    HopArray = []
    TimeOfTrace = time.strftime("%D:%H:%M:%S")
    output = getOutput("sudo traceroute -nI "+Target)
    for line in output:
      if "* * *" in line and HopArray[-1] != "Fail":
        HopArray.append("Fail")
      elif "ms" in line:
        print("Hop Array BULL -----"+line)
        print("Hop array adding"+line.split("  ")[1])
        HopArray.append(line.split("  ")[1].replace("*", "").replace(" ",""))

  # establish connection with DB
    client = pymongo.MongoClient(host="localhost", port=27017)
    db = client["database"]
    collection = db["traceroutes"]
    # format data for DB insertion
    data = {
        "Target": Target,
        "TimeOfTrace": TimeOfTrace,
        "HopArray": HopArray,
        "createdAt": datetime.datetime.now(datetime.timezone.utc)
    }
    # insert data and close connection
    collection.insert_one(data)
    client.close()
    # call the check and add function on the hop array so it can add hops to the tree
    print("Checking and adding Map") 
    print(Tracemap)
    CheckAndAdd(Tracemap["Tree"], HopArray, Target)
    # sleep for delay timer
    printTree(Tracemap["Tree"],0)
    time.sleep(Delay)
    if Target in removedTraceTargets and removedTraceTargets[Target] == Delay:
      keepProcessRunning = False
      del removedTraceTargets[Target]

########    ----   MAIN     ----    ####### MAYBE DO THE IF MAIN THING#
# Get list of targets
ListOfTargets = getTargets()
# Start a thread per target. Each thread will ping the target and log to their own files. spreads the starting of threads by waiting fractions of a second so that the pings dont all happen liek once like a firing squad and mess up the cpu
for TargetItem in ListOfTargets.items():
  PingThread = threading.Thread(target=PingMaker, args=(TargetItem[0],TargetItem[1],))
  PingThread.start()
  time.sleep(random.random()/3)
  TraceThread = threading.Thread(target=TraceMaker(TargetItem[0],TargetItem[1]))

  TraceThread.start()

  time.sleep(random.random()/3)
# now check forever every 5 minutes wether the target collection has changed or not. if it has, you know a target has been removed or added
while 1 == 1:
  time.sleep(300)
  newTargets = getTargets()
  if ListOfTargets != newTargets:
    added, removed = compareTargets(ListOfTargets, newTargets)
    # if length of added is 1 or more, start the process for everything in added
    if len(added) >=1:
      for TargetItem in added.items():
        if testTargetRegex(TargetItem[0]):
          PingThread = threading.Thread(target=PingMaker, args=(TargetItem[0],TargetItem[1],))
          PingThread.start()
          time.sleep(random.random()/3)
          TraceThread = threading.Thread(target=TraceMaker(TargetItem[0],TargetItem[1]))

          TraceThread.start() 

          time.sleep(random.random()/3)
    # if length of removed is 1 or more, add the names to the removed targets list, which processes will periodically check to see fi they need to be shut down
    if len(removed) >=1:
      for TargetItem in removed.items():
        removedTargets[TargetItem[0]] = TargetItem[1]
        removedTraceTargets[TargetItem[0]] = TargetItem[1]
    ListOfTargets = newTargets

