<!DOCTYPE html>
<html lang="en">
  <head>
    <title>PingMaker</title>
    <link rel="stylesheet" href="src/style.css">
    <ul>
      <li><a href="index.html">Home</a></li>
      <li><a href="request.html">Requests</a></li>
      <li><a href="targets.html">Targets</a></li>
    </ul>
  </head>
<body>
    <h1>Database Functions</h1>
    <h2>Add Target</h2>
    <form id="runRequest" action="addtargets.php" method="POST">
    Add Target: <input type="text" name="target"><br>
    <input type="submit">
    </form>
    <h2>Removing Target</h2>
    <form id="runRequest" action="remtargets.php" method="POST">
    Add Target: <input type="text" name="target"><br>
    <input type="submit">
    </form>
    <h2>Update Target Description</h2>
    <form id="runRequest" action="updatetargets.php" method="POST">
    Add Target: <input type="text" name="target"><br>
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
$Description = $_POST["description"];
//Check if the target is null, if it is, dont do anything
if (!empty($Target)){
//Function to find if target is already in database, if it isnt, add it with the description
    $result = $collection->find();
    $found = False;
    foreach ($result as $entry){
        if ($entry['Target'] == $Target){
            $found = True;
        }
    }
    if ($found == False) {
	$collection->insertOne(['Target' => $Target, 'Description' => $Description,]);
    }else {
	echo "<p>Target already in database</p><br>";
    }
}

// Get list of current targets and print
$result = $collection->find();
echo "<br>";
echo "<h1>Current Targets</h1>";
foreach ($result as $entry) {
    echo json_encode($entry['Target']), PHP_EOL;
    echo ": ";
    echo json_encode($entry['Description']), PHP_EOL;
    echo "<br>";
}

?>
</body>
</html>
