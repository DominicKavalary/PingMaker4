<?php
function GetTargetTable($result){
  echo "<h1>Target List</h1>", PHP_EOL;  
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
?>
