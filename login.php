<?php
session_start();

$Username = $_POST["username"];
$Password = $_POST["password"];
$Login = $_POST["login"];

require 'vendor/autoload.php';

$client = new MongoDB\Client("mongodb://localhost:27017");
$database = $client->database;
$collection = $database->users;

if (!empty($Username)){
    if ($Login == "login"){
      $result = $collection->findOne(['Username' => $Username]);
      if ($result['Password'] == hash('sha256', $Password)){
	            session_regenerate_id();
		    $_SESSION['loggedin'] = TRUE;
		    $_SESSION['name'] = $_POST['username'];
        header('Location: home.php');
      }else {
          echo 'Incorrect username and/or password!';
      }
    }
}
