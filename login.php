<?php
session_start();

$Username = $_POST["username"];
$Password = $_POST["password"];
$Login = $_POST["login"];

$client = new MongoDB\Client("mongodb://localhost:27017");
$database = $client->database;
$collection = $database->users;

if (!empty($Username)){
    if ($Submit == "Login"){
      $result = $collection->findOne(['Username' => $Target]);
      if ($result['Password'] == md5($Password)){
		    $_SESSION['loggedin'] = TRUE;
		    $_SESSION['name'] = $_POST['username'];
        header('Location: home.php');
      }else {
          echo 'Incorrect username and/or password!';
      }
    }
}
