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
    <h1>request.php</h1>
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
$collection = $database->collection;
$Target = $_POST["target"];
$Query = array('Target' => $Target);
$result = $collection->find($Query);

foreach ($result as $entry) {
    echo json_encode($entry), PHP_EOL;
}

?>
</body>
</html>
