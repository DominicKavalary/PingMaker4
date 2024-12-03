<!DOCTYPE html>
<html lang="en">
  <head>
    <title>PingMaker</title>
    <link rel="stylesheet" href="style.css">
    <ul>
      <li><a href="index.html">Home</a></li>
      <li><a href="request.html">Requests</a></li>
      <li><a href="targets.index">Targets</a></li>
      <li><a href="status.php">Status</a></li>
    </ul>
  </head>
<body>

<?php
// Include Composer autoload (make sure it's included to load the MongoDB library)
require 'vendor/autoload.php'; // Path to Composer's autoload file

//MongoDB PHP Connection Test
echo "<h1>MongoDB Connection</h1>";
try {
	// Create a new MongoDB client to connect to the MongoDB server
  $client = new MongoDB\Client("mongodb://localhost:27017"); // Change if your MongoDB is hosted elsewhere
  echo "Connection to database using PHP succesfull";
} catch (Exception $ex) {
  echo "Could not make connection to database with PHP";
  echo PHP_EOL;
}

//Mongodb Service Test
echo "<h1>Mongodb Service</h1>";
try {
	// Create a new MongoDB client to connect to the MongoDB server
  $output=null;
  $retval=null;
  exec('systemctl status mongod', $output, $retval);
  echo "Returned with status $retval and output:\n";
  foreach ($output as $line) {
    echo "<br>$line";
    if (str_contains($line,'CGroup',)) {
      break;
    }
  }
} catch (Exception $ex) {
	echo "Error running systemctl status mongod using PHP";
  echo PHP_EOL;
}

//Python Script Service Test
echo "<h1>PingMaker Service</h1>";
try {
	// Create a new MongoDB client to connect to the MongoDB server
  $output=null;
  $retval=null;
  exec('systemctl status PingMaker', $output, $retval);
  echo "Returned with status $retval and output:\n";
  foreach ($output as $line) {
    echo "<br>$line";
    if (str_contains($line,'CGroup',)) {
      break;
    }
  }
} catch (Exception $ex) {
	echo "Error running systemctl status PingMaker using PHP";
  echo PHP_EOL;
}


?>
</body>
</html>
