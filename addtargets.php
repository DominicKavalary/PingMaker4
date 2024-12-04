<!DOCTYPE html>
<html lang="en">
  <head>
    <title>PingMaker</title>
    <link rel="stylesheet" href="style.css">
    <ul>
      <li><a href="index.html">Home</a></li>
      <li><a href="request.html">Requests</a></li>
      <li><a href="targets.html">Targets</a></li>
      <li><a href="status.php">Status</a></li>
    </ul>
  </head>
<body>
    <h1>Database Functions</h1>
    <h2>Add Target</h2>
    <form id="runRequest" action="addtargets.php" method="POST">
    <input type="text" name="target" placeholder="IP or Hostname" required><br>
    <input type="text" name="description" placeholder="Description" required><br>
    <input type="text" name="delay" placeholder="Ping Delay In Seconds" required><br>
    <input type="submit" value="Add" name="submit">
    </form>
    <h2>Removing Target</h2>
    <form id="runRequest" action="remtargets.php" method="POST">
    <input type="text" name="target" placeholder="IP or Hostname" required><br>
    <input type="submit" value="Remove" name="submit">
    </form>
    <h2>Update Target</h2>
    <form id="runRequest" action="updatetargets.php" method="POST">
    <input type="text" name="target" placeholder="IP or Hostname" required><br>
    <input type="text" name="description" placeholder="Description" required><br>
    <input type="text" name="delay" placeholder="Ping Delay In Seconds" required><br>
    <input type="submit" value="Update" name="submit">
    </form>
<?php

// Include Composer autoload (make sure it's included to load the MongoDB library)
require 'vendor/autoload.php'; // Path to Composer's autoload file
require 'phpfunctions.php';
// Create a new MongoDB client to connect to the MongoDB server
$client = new MongoDB\Client("mongodb://localhost:27017"); // Change if your MongoDB is hosted elsewhere
$database = $client->database;
$collection = $database->targets;

// Get variables, some may have Target some may have description, remove only has target
$Target = $_POST["target"];
$Description = $_POST["description"];
$Delay = $_POST["delay"];
$Submit = $_POST["submit"]
//Check if the target is null, if it is, dont do anything
if (!empty($Target)){
//Function to find if target is already in database, if it isnt, add it with the description
    $result = $collection->findOne(['Target' => $Target]);
    if ($result['Target'] == $Target){
        echo "<h1 style='color:red;'>Error: Target already in database</h1><br>";
    }else {
        $collection->insertOne(['Target' => $Target, 'Description' => $Description, 'Delay' => $Delay,]);
    }
}

// Get list of current targets and print
$result = $collection->find();
//set up table
GetTargetTable($result);

?>
</body>
</html>
