# Prerequisites
sudo apt install traceroute -y
make a traceroutes collection and a tracemaps collection in mongodb

# Create the TraceObject object. this will be the core of our TraceTree
class TraceObject:
  #  define the object, it has two variables, address and nexthops. nexthops will be an array that holds traceobjects. address will be the hop address
  def __init__(self, Address):
    self.address = Address
    self.nexthops = []
    # if the address inputed into the object matches a next hop it has, return true
  def ifHopMatches(self, Address):
    if self.nexthops:
      for hop in self.nexthops:
        if hop.address == Address:
          return True
      return False
    else:
      return False
      # add a traceobject to the array of next hops
  def addHop(self, Hop):
    self.nexthops.append(Hop)

#TraceMaker frunction to get the route to your targets from the server
def TraceMaker(Target, Delay):
  # check if the tree has started being built. if not, keep the flag false to start to build it, if it has, dont keep checking
  TreeBuilt = False
  client = pymongo.MongoClient(host="localhost", port=27017)
  db = client["database"]
  collection = db["tracemaps"]
  if collection.find_one({'Target': Target}):
    TreeBuilt = True
  client.close()

  # Set up the loop to keep doing traceroutes
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

    # Building the tree

   def buildTree(HopArray):
     # Hop array depth tracker
     HopTracker = 0
     # the first node in the tree is the machine itself
     Node=TraceObject("Self")
     #Now you need to check to see if the next node exists and matches the next recorded hop
     Node.

    if TreeBuilt == False:
      # build innitial tree
      for item in HopArray:
        TreeNode = TraceObject(item)




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
