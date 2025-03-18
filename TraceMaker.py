# Prerequisites
sudo apt install traceroute -y
make a traceroutes collection and a tracemaps collection in mongodb



#TraceMaker frunction to get the route to your targets from the server
def TraceMaker(Target, Delay):
  while 1==1:
  # setting up array for hops to go in
    HopArray = []
    TimeOfTrace = time.strftime("%D:%H:%M:%S")
    output = getOutput("traceroute "+Target)
    for line in output:
      if "* * *" in line:
        HopArray.append("Fail")
      elif "ms" in line:
        HopArray.append(line=line.split("  ")[1])
  ######################################## THINGS I NEED###############################
  - Summary of failures
        if it goes 192.16.1.1 then fail fail fail 192.168.2.1 i need it to report 192.168.1.1 3 fails 192.168.2.1
  
  - also currently the new target list will always make regex fail messages every 5 minutes because we aren't removing the bad target from the database, we are expcluding it form current list of targets. SO every 5 minutes when it gets the list of targets it will grab the bad one and do the regex test again
  ##############################################################################
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
    # insert data
    collection.insert_one(data)







    # close connection so theres not a million files open
    client.close()
    time.sleep(Delay)







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
    # if length of removed is 1 or more, add the names to the removed targets list, which processes will periodically check to see fi they need to be shut down
    if len(removed) >=1:
      for TargetItem in removed.items():
        removedTargets[TargetItem[0]] = TargetItem[1]
    ListOfTargets = newTargets
    # Now also start the threads for the traceroute portion of device tracking
    for Target in ListOfTargets:
      TraceThread = threading.Thread(target=TraceMaker, args=(Target[0],TargetItem[1],))
          TraceThread.start()
          time.sleep(random.random()/3)
