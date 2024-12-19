<?php
session_start();
if (!isset($_SESSION['loggedin'])) {
	header('Location: index.html');
	exit;
}
?>

<!DOCTYPE html>
<html lang="en">
  <head>
    <title>PingMaker</title>
    <link rel="stylesheet" href="style.css">
    <ul>
      <li><a href="home.php">Home</a></li>
      <li><a href="request.php">Requests</a></li>
      <li><a href="targets.php">Targets</a></li>
      <li><a href="status.php">Status</a></li>
      <li><a href="users.php">Users</a></li>
      <li style='float: right;'><a href="logout.php">Logout</a></li>
    </ul>
  </head>
<body>
	
<?php
if ($_SESSION['role'] != "Admin") {
	echo "<h1 style='color:red;'>You need admin permissions in order to edit target database</h1><br>";
	exit;
} else {
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
	$Submit = $_POST["submit"];
	
	//Check if the target is null, if it is, dont do anything
	if (!empty($Target)){
	//Function to find if target is already in database, if it isnt, add it with the description
	    if ($Submit == "Add"){
	      $result = $collection->findOne(['Target' => $Target]);
	      if ($result['Target'] == $Target){
	          echo "<h1 style='color:red;'>Error: Target already in database</h1><br>";
	      }else {
	          $collection->insertOne(['Target' => $Target, 'Description' => $Description, 'Delay' => $Delay,]);
	          echo "<h1 style='color:green;'>Target added to database</h1><br>";
	      }
	    } else if ($Submit == "Remove"){
	      $result = $collection->findOne(['Target' => $Target]);
	      if ($result['Target'] == $Target){
	          $collection->deleteOne(['Target' => $Target,]);
	          echo "<h1 style='color:green;'>Target removed from database</h1><br>";
	      }else {
	          echo "<h1 style='color:red;'>Error: Target not found in database</h1><br>";
	      }
	    } else if ($Submit == "Update"){
	      $result = $collection->findOne(['Target' => $Target]);
	      if ($result['Target'] == $Target){
	          $collection->updateOne([ 'Target' => $Target ], [ '$set' => [ 'Description' => $Description ]]);
	          $collection->updateOne([ 'Target' => $Target ], [ '$set' => [ 'Delay' => $Delay ]]);
	          echo "<h1 style='color:green;'>Target updated</h1><br>";
	      }else {
	          echo "<h1 style='color:red;'>Error: Target not found in database</h1><br>";
	      }
	    }
	}
}
?>
    <h1>Database Functions</h1>
    <h2>Add Target</h2>
    <form id="runRequest" action="targets.php" method="POST">
    <input type="text" name="target" placeholder="IP or Hostname" required><br>
    <input type="text" name="description" placeholder="Description" required><br>
    <input type="number" name="delay" placeholder="Ping Delay In Seconds" min="1" required><br>
    <input type="submit" value="Add" name="submit"><br>
    </form>
    <h2>Removing Target</h2>
    <form id="runRequest" action="targets.php" method="POST">
    <select name="target" placeholder="IP or Hostname">
    <?php
	$result = $collection->find();
	foreach ($result as $entry) {
		$Value = $entry['Target'];
		echo "<option value='$Value'>$Value</option>";
		echo PHP_EOL;
	}
    ?>
    </select>
    <br>
    <input type="submit" value="Remove" name="submit">
    </form>
    <h2>Update Target</h2>
    <form id="runRequest" action="targets.php" method="POST">
    <select name="target" placeholder="IP or Hostname">
    <?php
	$result = $collection->find();
	foreach ($result as $entry) {
		$Value = $entry['Target'];
		echo "<option value='$Value'>$Value</option>";
		echo PHP_EOL;
	}
    ?>
    </select>
    <br>
    <input type="text" name="description" placeholder="Description" required><br>
    <input type="number" name="delay" placeholder="Ping Delay In Seconds" min="1" required><br>
    <input type="submit" value="Update" name="submit">
    </form>
<?php

// Get list of current targets and print
$result = $collection->find();
//set up table
GetTargetTable($result);

?>
</body>
</html>
