<?php

function DBConn($db = "jokeline", $servername = "127.0.0.1", $username = "root", $password = ""){
	$conn = new mysqli($servername, $username, $password, $db);
	if ($conn->connect_error) return false;
	return $conn;
}

ini_set('memory_limit', '-1');

// MySQL table's name
$tableName = 'positive_larvae';

// Get JSON file and decode contents into PHP arrays/values
$jsonFile = 'all_positive_larvae2014.json';
$jsonData = json_decode(file_get_contents($jsonFile), true);

$db = DBConn("containment");

// Iterate through JSON and build INSERT statements
foreach ($jsonData as $id=>$row) {
    $insertPairs = array();
    foreach ($row as $key=>$val) {
        $insertPairs[addslashes($key)] = addslashes($val);
    }
    $insertKeys = '`' . implode('`,`', array_keys($insertPairs)) . '`';
    $insertVals = '"' . implode('","', array_values($insertPairs)) . '"';

    $sql = "INSERT INTO `{$tableName}` ({$insertKeys}) VALUES ({$insertVals});";
	
	if ($db->query($sql) === TRUE) {
	    echo "New record created successfully: $id <br>";
	} else {
	    echo "Error: " . $sql . "<br>" . $conn->error. " <br>";
	}
}
?>