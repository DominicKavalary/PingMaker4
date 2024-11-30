<!DOCTYPE html>
<html lang="en">
  <head>
    <title>PingMaker</title>
    <link rel="stylesheet" href="style.css">
    <ul>
      <li><a href="index.html">Home</a></li>
      <li><a href="request.html">Requests</a></li>
      <li><a href="targets.html">Targets</a></li>
    </ul>
  </head>
<body>
    <h1>Request Target Info</h1>
    <form id="runRequest" action="request.php" method="POST">
    Name: <input type="text" name="target"><br>
    <input type="submit">
    </form>

<button type="button" onclick="tableToCSV()">
            download CSV
</button>
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

// Include Composer autoload (make sure it's included to load the MongoDB library)
require 'vendor/autoload.php'; // Path to Composer's autoload file

// Create a new MongoDB client to connect to the MongoDB server
$client = new MongoDB\Client("mongodb://localhost:27017"); // Change if your MongoDB is hosted elsewhere
$database = $client->database;
$collection = $database->collection;

// Get variables, some may have Target some may have description, remove only has target
$Target = $_POST["target"];
$Query = array('Target' => $Target);
$result = $collection->find($Query);
//Check if the target is null, if it is, dont do anything
if (!empty($Target)){
//Function
    //set up table
    echo "<h1>$Target</h1>";  
    echo "<div style='height:500px; width:600px; overflow: auto;'>";
    echo "<table>";
    echo "<tr>";
    echo "<th>Time Of Ping</th>";
    echo "<th>Packet Loss</th>";
    echo "<th>Response Time</th>";
    echo "<th>Error Note</th>";
    echo "</tr>";
    //insert rows into table
    foreach ($result as $entry) {
        echo "<tr>";
        echo "<td>";
        echo json_encode($entry['timeOfPing']);
        echo "</td>";
        echo "<td>";
        echo json_encode($entry['packetLoss']);
        echo "</td>";
        echo "<td>";
        echo json_encode($entry['responseTime']);
        echo "</td>";
        echo "<td>";
        echo json_encode($entry['errorNote']);
        echo "</td>";
        echo "</tr>";
        echo PHP_EOL;
    }
    echo "</table>";
    echo "</div>";
}


?>
</body>
</html>
