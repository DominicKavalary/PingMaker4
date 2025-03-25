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
    <h1>Request Target Info</h1>
    <form id="runRequest" action="request.php" method="POST">
    <select name="target" placeholder="IP or Hostname">
<?php
        require 'vendor/autoload.php';
	require 'phpfunctions.php';
	$Target = $_POST["target"];
	$client = new MongoDB\Client("mongodb://localhost:27017"); // Change if your MongoDB is hosted elsewhere
	$database = $client->database;
	$collection = $database->targets;
	$result = $collection->find();
	foreach ($result as $entry) {
		$Value = $entry['Target'];
		echo "<option value='$Value'>$Value</option>";
		echo PHP_EOL;
	}
?>
    </select>
    <input type="submit" value="Get Target Data" name="submit">
    </form>

<script type="text/javascript">
        function tableToCSV() {
            // Variable to store the final csv data
            let csv_data = [];
            // Get each row data
            let rows = document.getElementsByTagName('tr');
            for (let i = 0; i < rows.length; i++) {
                // Get each column data
                let cols = rows[i].querySelectorAll('td,th');
                // Stores each csv row data
                let csvrow = [];
                for (let j = 0; j < cols.length; j++) {
                    // Get the text data of each cell
                    // of a row and push it to csvrow
                    csvrow.push(cols[j].innerHTML);
                }
                // Combine each column value with comma
                csv_data.push(csvrow.join(","));
            }
            // Combine each row data with new line character
            csv_data = csv_data.join('\n');
            // Call this function to download csv file  
            downloadCSVFile(csv_data);
        }
        function downloadCSVFile(csv_data) {
            // Create CSV file object and feed
            // our csv_data into it
            CSVFile = new Blob([csv_data], {
                type: "text/csv"
            });
            // Create to temporary link to initiate
            // download process
            let temp_link = document.createElement('a');
            // Download csv file
            temp_link.download = "PingMakertarget.csv";
            let url = window.URL.createObjectURL(CSVFile);
            temp_link.href = url;
            // This link should not be displayed
            temp_link.style.display = "none";
            document.body.appendChild(temp_link);
            // Automatically click the link to
            // trigger download
            temp_link.click();
            document.body.removeChild(temp_link);
        }
    </script>
  
<?php

//Check if the target is null, if it is, dont do anything
if (!empty($Target)){
	$collection = $database->collection;
	$result = $collection->find(['Target' => $Target]);
	GetRequestTable($result);
  	echo "<button type='button' onclick='tableToCSV()'>Download CSV</button>";
	$collection = $database->traceroutes;
	$result = $collection->find(['Target' => $Target]);
	GetTraceTable($result);
	$collection = $database->tracemaps;
	$result = $collection->find(['Target' => $Target]);
	print_nested($result['Tree'])
  	
}

?>
</body>
</html>
