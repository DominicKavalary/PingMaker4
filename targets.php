<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>messing around</title>
    <a href="request.html">requests</a>
    <a href="targets.html">targets</a>
</head>
<body>
    
    <h1>Add Target</h1>
    <form id="runRequest" action="targets.php" method="POST">
    Target: <input type="text" name="target"><br>
    Description: <input type="text" name="description"><br>
    <input type="submit">
    </form>
    <h1>Removing Target</h1>
    <form id="runRequest" action="remtargets.php" method="POST">
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
$Target = $_POST["target"];
$Description = $_POST["description"];
$collection->insertOne(['Target' => $Target, 'Description' => $Description,]);

$result = $collection->find();

foreach ($result as $entry) {
    echo json_encode($entry['Target']), PHP_EOL;
    echo ": ";
    echo json_encode($entry['Description']), PHP_EOL;
    echo "<br>";
}

?>
</body>
</html>
