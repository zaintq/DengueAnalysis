<?php
	
	function get_data($url) {
		$ch = curl_init();
		$timeout = 5;
		curl_setopt($ch, CURLOPT_URL, $url);
		curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
		curl_setopt($ch, CURLOPT_CONNECTTIMEOUT, $timeout);
		$data = curl_exec($ch);
		curl_close($ch);
		return $data;
	}

	echo "start \n";
	ini_set('max_execution_time', 3600); //3600 seconds
	do{
		// $lines = file("http://tracking.punjab.gov.pk/ajax/all_positive_larvae.json?year=2015");
		$lines = get_data("http://tracking.punjab.gov.pk/ajax/all_positive_larvae.json?year=2015");
		if($lines == false)
			sleep(300); //300 seconds	
	}while($lines == false);
	echo "\n \n outta loop! \n \n";
	var_dump($lines);
	echo "\n \n dpme \n";
	die();
	$jsonIterator = new RecursiveIteratorIterator(
    new RecursiveArrayIterator(json_decode($lines[0], TRUE)),
    RecursiveIteratorIterator::SELF_FIRST);
    
    $cases = fopen('dengue_larvae.cas', 'w');
    $geof = fopen('geo_larvae.csv', 'w');
    
	$date = '';
	$location = '';
	$row = 1;
	
	foreach ($jsonIterator as $key => $val) 
	{
	
		if(is_array($val)) 
		{
		    //echo "$key:<br/>";
			$date = '';
			$location = '';
		} 
		else 
		{
			if($key == 'created_at')
		    	$date = "$val";
			if($key == 'location')
		    	$location = "$val";
		}
		if($date != '' && $location != '' )
		{
			$date = explode('T',$date);
			$temp = explode('-',$date[0]);
			$newdate = "$temp[1]/$temp[2]/$temp[0]";
			$geo = explode(',',$location);
			
			fwrite($cases, "$row 1 $newdate\n");
			fwrite($geof, "$row $geo[0] $geo[1]\n");
			
			$date = '';
			$location = '';
			$row++;
		}
	}
?>
