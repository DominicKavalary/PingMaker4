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
    <input type="submit">
    </form>
    <h2>Removing Target</h2>
    <form id="runRequest" action="remtargets.php" method="POST">
    <input type="text" name="target" placeholder="IP or Hostname" required><br>
    <input type="submit">
    </form>
    <h2>Update Target</h2>
    <form id="runRequest" action="updatetargets.php" method="POST">
    <input type="text" name="target" placeholder="IP or Hostname" required><br>
    <input type="text" name="description" placeholder="Description" required><br>
    <input type="text" name="delay" placeholder="Ping Delay In Seconds" required><br>
    <input type="submit">
    </form>
<?php

// Include Composer autoload (make sure it's included to load the MongoDB library)
require 'vendor/autoload.php'; // Path to Composer's autoload file

// Create a new MongoDB client to connect to the MongoDB server
$client = new MongoDB\Client("mongodb://localhost:27017"); // Change if your MongoDB is hosted elsewhere
$database = $client->database;
$collection = $database->targets;

// Get variables, some may have Target some may have description, remove only has target
$Target = $_POST["target"];

//Check if the target is null, if it is, dont do anything
if (!empty($Target)){
//Function
    $collection->deleteOne(['Target' => $Target,]);
    }

// Get list of current targets and print
$result = $collection->find();
echo "<br>";
echo "<h1>Current Targets</h1>";
foreach ($result as $entry) {
    echo json_encode($entry['Target']), PHP_EOL;
    echo "<br>";
}

?>
</body>
</html>

