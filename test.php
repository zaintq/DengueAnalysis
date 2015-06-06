<?php
do{
	$blah = file('http://tracking.punjab.gov.pk/ajax/all_positive_larvae.json');
	var_dump($blah);
}while($blah == false);
?>