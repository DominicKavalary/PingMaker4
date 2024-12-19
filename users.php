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
	echo "<h1 style='color:red;'>You need admin permissions in order to edit User database</h1><br>";
	exit;
} else{
	// Include Composer autoload (make sure it's included to load the MongoDB library)
	require 'vendor/autoload.php'; // Path to Composer's autoload file
	require 'phpfunctions.php';
	// Create a new MongoDB client to connect to the MongoDB server
	$client = new MongoDB\Client("mongodb://localhost:27017"); // Change if your MongoDB is hosted elsewhere
	$database = $client->database;
	$collection = $database->users;
	
	// Get variables, some may have Target some may have description, remove only has target
	$Username = $_POST["username"];
	$Password = $_POST["password"];
	$Role = $_POST["role"];
	$Submit = $_POST["submit"];
	
	//Check if the target is null, if it is, dont do anything
	if (!empty($Username)){
	//Function to find if target is already in database, if it isnt, add it with the description
	    if ($Submit == "Add"){
	      $result = $collection->findOne(['Username' => $Username]);
	      if ($result['Username'] == $Username){
	          echo "<h1 style='color:red;'>Error: User already in database</h1><br>";
	      }else {
	          $collection->insertOne(['Username' => $Username, 'Password' => hash('sha256',$Password), 'Role' => $Role,]);
	          echo "<h1 style='color:green;'>User added to database</h1><br>";
	      }
	    } else if ($Submit == "Remove"){
	      $result = $collection->findOne(['Username' => $Username]);
	      if ($result['Username'] == $Username){
	          if ($result['Role'] == 'Guest'){
		  	$collection->deleteOne(['Username' => $Username,]);
	          	echo "<h1 style='color:green;'>User removed from database</h1><br>";
		  } else if ($collection->count(['Role' => 'Admin']) > 1){
			$collection->deleteOne(['Username' => $Username,]);
	         	echo "<h1 style='color:green;'>User removed from database</h1><br>";  
		  } else{
			 echo "<h1 style='color:red;'>Cannot remove last Admin user from database</h1><br>";
		  }
	      }else {
	          echo "<h1 style='color:red;'>Error: User not found in database</h1><br>";
	      }
	    } else if ($Submit == "Update"){
	      $result = $collection->findOne(['Username' => $Username]);
	      if ($result['Username'] == $Username){
	          $collection->updateOne([ 'Username' => $Username ], [ '$set' => [ 'Password' => hash('sha256',$Password)]]);
	          $collection->updateOne([ 'Username' => $Username ], [ '$set' => [ 'Role' => $Role ]]);
	          echo "<h1 style='color:green;'>User updated</h1><br>";
	      }else {
	          echo "<h1 style='color:red;'>Error: User not found in database</h1><br>";
	      }
	    }
	}
}
?>
    <h1>Database Functions</h1>
    <h2>Add user</h2>
    <form id="runRequest" action="users.php" method="POST">
    <input type="text" name="username" placeholder="Username" required><br>
    <input type="password" name="password" placeholder="Password" required><br>
    <select name="role">
    <option value="Guest">Guest</option>
    <option value="Admin">Admin</option>
    </select>
    <br>
    <input type="submit" value="Add" name="submit">
    </form>
    <h2>Remove user</h2>
  <form id="runRequest" action="users.php" method="POST">
    <select name="username" placeholder="Username">
<?php
	$result = $collection->find();
	foreach ($result as $entry) {
		$Value = $entry['Username'];
		echo "<option value='$Value'>$Value</option>";
		echo PHP_EOL;
	}
?>
    </select><br>
    <input type="checkbox" class="selectoptions" id="areyousure" required>
    <label for="areyousure">Are you sure?</label><br>
    <input type="submit" value="Remove" name="submit">
    </form>
    <h2>Update User</h2>
  <form id="runRequest" action="users.php" method="POST">
    <select name="username" placeholder="Username">
<?php
	$result = $collection->find();
	foreach ($result as $entry) {
		$Value = $entry['Username'];
		echo "<option value='$Value'>$Value</option>";
		echo PHP_EOL;
	}
?>
    </select><br>
    <input type="password" name="password" placeholder="Password" required><br>
    <select name="role">
    <option value="Guest">Guest</option>
    <option value="Admin">Admin</option>
    </select>
    <br>
    <input type="submit" value="Update" name="submit">
    </form>
<?php
// Get list of current targets and print
$result = $collection->find();
//set up table
GetUserTable($result);

?>
</body>
</html>
