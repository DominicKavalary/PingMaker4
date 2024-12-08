<?php
function GetTargetTable($result){
  echo "<h1>Target Table</h1>", PHP_EOL;  
  echo "<div style='height:500px; width:600px; overflow: auto;'>", PHP_EOL;
  echo "<table>", PHP_EOL;
  echo "<tr><th>Target</th><th>Description</th><th>Delay</th></tr>";
  //insert rows into table
  foreach ($result as $entry) {
    echo "<tr><td>";
    echo json_encode($entry['Target']);
    echo "</td><td>";
    echo json_encode($entry['Description']);
    echo "</td><td>";
    echo json_encode($entry['Delay']);
    echo "</td></tr>";
    echo PHP_EOL;
  }
  echo "</table></div>";
}
function GetRequestTable($result){
  echo "<h1>Ping Table</h1>", PHP_EOL;
  echo "<div style='height:500px; width:600px; overflow: auto;'>", PHP_EOL;
  echo "<table>", PHP_EOL;
  echo "<tr><th>Time Of Ping</th><th>Packet Loss</th><th>Response Time</th><th>Error Note</th></tr>";
  //insert rows into table
  foreach ($result as $entry) {
    echo "<tr><td>";
    echo json_encode($entry['timeOfPing']);
    echo "</td><td>";
    echo json_encode($entry['packetLoss']);
    echo "</td><td>";
    echo json_encode($entry['responseTime']);
    echo "</td><td>";
    echo json_encode($entry['errorNote']);
    echo "</td></tr>";
    echo PHP_EOL;
  }
  echo "</table></div>";
}
function GetUserTable($result){
  echo "<h1>User Table</h1>", PHP_EOL;
  echo "<div style='height:500px; width:600px; overflow: auto;'>", PHP_EOL;
  echo "<table>", PHP_EOL;
  echo "<tr><th>User</th><th>Role</th></tr>";
  //insert rows into table
  foreach ($result as $entry) {
    echo "<tr><td>";
    echo json_encode($entry['Username']);
    echo "</td><td>";
    echo json_encode($entry['Role']);
    echo "</td></tr>";
    echo PHP_EOL;
  }
  echo "</table></div>";
}
function GetErrorTable($result){
  echo "<h1>Error Table</h1>", PHP_EOL;
  echo "<div style='height:500px; width:600px; overflow: auto;'>", PHP_EOL;
  echo "<table>", PHP_EOL;
  echo "<tr><th>Target</th><th>Error</th><th>Time</th></tr>";
  //insert rows into table
  foreach ($result as $entry) {
    echo "<tr><td>";
    echo json_encode($entry['Target']);
    echo "</td><td>";
    echo json_encode($entry['Error']);
    echo "</td><td>";
    echo json_encode($entry['Time']);
    echo "</td></tr>";
    echo PHP_EOL;
  }
  echo "</table></div>";
}
?>
