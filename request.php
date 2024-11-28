<!DOCTYPE html>
<html lang="en">
  <head>
    <title>PingMaker</title>
    <link rel="stylesheet" href="src/style.css">
    <ul>
      <li><a href="index.html">Home</a></li>
      <li><a href="request.php">Requests</a></li>
      <li><a href="targets.html">Targets</a></li>
    </ul>
  </head>
<body>
    <h1>Request Target Info</h1>
    <form id="runRequest" action="request.php" method="POST">
    Name: <input type="text" name="target"><br>
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
$Query = array('Target' => $Target);
$result = $collection->find($Query);
//Check if the target is null, if it is, dont do anything
if (!empty($Target)){
//Function
    //set up table
    echo "<div style='height:500px; width:600px; overflow: auto;'><br>";
    echo "<h1>$Target</h1><br>";
    echo "<table>";
    echo "<tr>";
    echo "<th>Time Of Ping</th>";
    echo "<th>Packet Loss</th>";
    echo "<th>Response Time</th>";
    echo "<th>Error Note</th>";
    echo "</tr>";
    //insert rows into table
    foreach ($result as $entry) {
        echo "<tr>";
        echo "<td>";
        echo json_encode($entry['timeOfPing']), PHP_EOL;
        echo "</td>";
        echo "<td>";
        echo json_encode($entry['packetLoss']), PHP_EOL;
        echo "</td>";
        echo "<td>";
        echo json_encode($entry['responseTime']), PHP_EOL;
        echo "</td>";
        echo "<td>";
        echo json_encode($entry['errorNote']), PHP_EOL;
        echo "</td>";
        echo "</tr>";
    }
    echo "</table>";
    echo "</div>";
}


?>
</body>
</html>
