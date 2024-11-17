<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <title>messing around</title>
</head>
<body>
    <h1>Add Target</h1>
    <form id="runRequest" action="targets.php" method="POST">
    Add Target: <input type="text" name="target"><br>
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

$collection->insertOne(['Target' => $Target,]);

$result = $collection->find();

foreach ($result as $entry) {
    echo json_encode($entry['Target']), PHP_EOL;
    echo "<br>";
}

?>
</body>
</html>
