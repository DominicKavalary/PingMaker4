<?php

require __DIR__ . '/../vendor/autoload.php';
//make connection and allow insecure connections because i dont understand certificates
$client = new MongoDB\Client('mongodb://127.0.0.1:27017',['tls' => true, 'tlsInsecure' => true],);
//select database
$database = $client->database;
$collection = $database->collection;
//get results, might need =>
$results = $collection->find(['Target' == "8.8.8.8"]);
foreach ($results as $doc) {
    echo json_encode($doc), PHP_EOL;
}
//get number of records
$result = $collection->countDocuments(['Target' == "8.8.8.8"]);
echo 'Number of results: ', $result;

?>
