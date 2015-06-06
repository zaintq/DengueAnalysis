<?php

require_once('parser2new.php');
$data = extract_data_of_file('result_larvae.txt');
$start_date = strtotime("-1 month");
$end_date = strtotime("now");



$jsn = file_get_contents('http://tracking.punjab.gov.pk/ajax/weather_data.json'); 
$weather = json_decode($jsn);
$lahore_weather = array();

for ($i = 0; $i < count($weather); $i++){
	if ($weather[$i]->district == 'Lahore'){
		$lahore_weather[] = $weather[$i];
	}
}

$weather = $lahore_weather;

function getRainPastFortNigt($date_as_string,$decodedData,$last_n_days){
    $cur_date=new DateTime($date_as_string);
    $total_rain=0.00;
    foreach ($decodedData as $dataElement){//replaced the enntire for loop
        $dataDate=new DateTime($dataElement->date);
        $dataDateString=$dataDate->format('Y-m-d');
        $dataDate=new DateTime($dataDateString);
        $dateInterval=$dataDate->diff($cur_date);
            if($dateInterval->days<= $last_n_days && $dateInterval->invert==0){//this line.
                $total_rain=$total_rain+$dataElement->min_rain_fall;
            }
        }
    return $total_rain;
}


function getTempPastFortNigt($date_as_string,$decodedData,$last_n_days){
    $cur_date=new DateTime($date_as_string);
    $total_rain=0.00;
    foreach ($decodedData as $dataElement){//replaced the enntire for loop
        $dataDate=new DateTime($dataElement->date);
        $dataDateString=$dataDate->format('Y-m-d');
        $dataDate=new DateTime($dataDateString);
        $dateInterval=$dataDate->diff($cur_date);
            if($dateInterval->days<= $last_n_days && $dateInterval->invert==0){//this line.
                $total_rain=$total_rain+$dataElement->max_temperature;
            }
        }
    return $total_rain;
}




function getProb($rain,$mxtemp){
    
    $proba= 1/ ( 1 + exp(   -1*(-23.4372570261433 + 0.00597102025913475*$rain -0.000110941078266593*$mxtemp*$mxtemp +0.102469735126995*$mxtemp)   ) );
    
    return $proba;
}














$SECONDS_IN_DAY=86400;


?>
<!DOCTYPE html>
<html>
  <head>
  	<script type="text/javascript" src="http://www.google.com/jsapi"></script>
	<script type="text/javascript" src="js/jquery-1.3.2.min.js"></script>
  	<script type="text/javascript" src="js/jquery-ui-1.7.1.custom.min.js"></script>
    <script type="text/javascript" src="js/selectToUISlider.jQuery.js"></script>
    <link rel="stylesheet" href="css/redmond/jquery-ui-1.7.1.custom.css" type="text/css" />
    <link rel="Stylesheet" href="css/ui.slider.extras.css" type="text/css" />
    <link rel="Stylesheet" href="css/bootstrap/css/bootstrap.min.css" type="text/css" />
    <link rel="Stylesheet" href="css/master.css" type="text/css" />
  
	<script type="text/javascript">
		
	var all_circles = {}; // the array containing all the circles!!


	Date.prototype.getWeek = function() {
		var determinedate = new Date();
		determinedate.setFullYear(this.getFullYear(), this.getMonth(), this.getDate());
		var D = determinedate.getDay();
		if(D == 0) D = 7;
		determinedate.setDate(determinedate.getDate() + (4 - D));
		var YN = determinedate.getFullYear();
		var ZBDoCY = Math.floor((determinedate.getTime() - new Date(YN, 0, 1, -6)) / 86400000);
		var WN = 1 + Math.floor(ZBDoCY / 7);
		return WN;
	}

	var all_weeks=new Array();
	var wIndex=0;

	<?php
		$temp=$start_date;
		$i=0;
		while($temp<=$end_date){
		    
		    echo "all_weeks[wIndex]=\"".date("Y/m/d",$temp)."\";";
		    echo "wIndex+=1;";
		    
		    $temp+=1*$SECONDS_IN_DAY;
		}	
	?>							
	</script>
	<script type="text/javascript">	

	var outbreak_data = <?php echo json_encode($data); ?>

  	var opacity = 0;
  	var town_color = new Array();
  	<?php
        $temp=$start_date;
        $i=0;
        while($temp<=$end_date)
		{          
            echo "town_color[".date("Y/m/d",$temp)."] = 0;";
            $temp+=1*$SECONDS_IN_DAY;
        }
        echo "town_color[".$start_date."] = 0.3;";
    ?>

	function existsInInterval(date, range)
	{
		range = range.split(">");
		var start = range[0];
		var end = range[1];
		start = start.split("/");
		end = end.split("/");
		date = date.split("/");

		start[0] = parseInt(start[0],10);
		start[1] = parseInt(start[1],10);
		start[2] = parseInt(start[2],10);
		
		end[0] = parseInt(end[0],10);
		end[1] = parseInt(end[1],10);
		end[2] = parseInt(end[2],10);

		date[0] = parseInt(date[0],10);
		date[1] = parseInt(date[1],10);
		date[2] = parseInt(date[2],10);
		startDate = new Date(start[0],start[1],start[2]);
		endDate = new Date(end[0],end[1],end[2]);
		checkDate = new Date(date[0],date[1],date[2]);

		if(checkDate>=startDate && checkDate<=endDate)
			return true;
		else 
			return false;
	}
	function first_reshow_outbreaks()
	{
		c = 1;
			
		//$("#valueAA").val(all_weeks[ui.value]);
		<?php
			echo "var first = '".date("Y/m/d",$start_date)."';";
		?>
		for(var iter in all_circles)
		{
			if(!existsInInterval(first, iter))
				all_circles[iter].setVisible(false);
			else
			{
				var id = iter.substring(iter.lastIndexOf(">")+1);
				var ucs = outbreak_data[id]['ucs'];
				if(ucs == null)
				{	
					continue;
				}
				ucs = ucs.split(",");
				for(i=0; i<ucs.length; i++)
					ucs[i] = ucs[i].split("-");
				
				row = document.createElement("tr");
				$(row).addClass('circle-row').attr('lat',all_circles[iter].center.lat()).attr('long',all_circles[iter].center.lng());
				
				ob_id = document.createElement('td');
				ob_id.innerHTML = c;
				
				uc_num = document.createElement('td');
				for(i=0; i<ucs.length; i++)
				{
					uc_num.innerHTML += ucs[i][0];
					uc_num.innerHTML += ', ';
				}
				
				uc_names = document.createElement('td');
				for(i=0; i<ucs.length; i++)
				{
					uc_names.innerHTML += ucs[i][1];
					uc_names.innerHTML += ', ';
				}
				
				uc_cases = document.createElement('td');
				uc_cases.innerHTML = Math.ceil(outbreak_data[id]['expected']);
				
				row.appendChild(ob_id);
				row.appendChild(uc_num);
				row.appendChild(uc_names);
				row.appendChild(uc_cases);
				
				document.getElementById("outbreak-table").appendChild(row);
				
				c++;
			}
		}
		
		$('.circle-row').bind('click', function() {
			var tempLat = $(this).attr('lat');
			var tempLong = $(this).attr('long');
		
			map.setCenter(new google.maps.LatLng(tempLat, tempLong), map.zoom);
		});
	}
    function reshow_outbreaks(e,ui)
	{
		c = 1;
		
		document.getElementById("outbreak-table").innerHTML = '';
			
		$("#valueAA").val(all_weeks[ui.value]);
		$(".ttContent").text(all_weeks[ui.value]);
		for(var iter in all_circles)
		{
			if(!existsInInterval(all_weeks[ui.value], iter))
				all_circles[iter].setVisible(false);
			else
			{	
				var id = iter.substring(iter.lastIndexOf(">")+1);
				var ucs = outbreak_data[id]['ucs'];
				if(ucs == null)
					continue;
				ucs = ucs.split(",");
				for(i=0; i<ucs.length; i++)
					ucs[i] = ucs[i].split("-");
				
				all_circles[iter].setVisible(true);
				row = document.createElement("tr");
				$(row).addClass('circle-row').attr('lat',all_circles[iter].center.lat()).attr('long',all_circles[iter].center.lng());
				
				ob_id = document.createElement('td');
				ob_id.innerHTML = c;
				
				uc_num = document.createElement('td');
				for(i=0; i<ucs.length; i++)
				{
					uc_num.innerHTML += ucs[i][0];
					uc_num.innerHTML += ', ';
				}
				
				uc_names = document.createElement('td');
				for(i=0; i<ucs.length; i++)
				{
					uc_names.innerHTML += ucs[i][1];
					uc_names.innerHTML += ', ';
				}
				
				uc_cases = document.createElement('td');
				uc_cases.innerHTML = Math.ceil(outbreak_data[id]['expected']);
				
				row.appendChild(ob_id);
				row.appendChild(uc_num);
				row.appendChild(uc_names);
				row.appendChild(uc_cases);
				
				document.getElementById("outbreak-table").appendChild(row);
				
				c++;
			}
		}
		
		$('.circle-row').bind('click', function() {
			var tempLat = $(this).attr('lat');
			var tempLong = $(this).attr('long');
		
			map.setCenter(new google.maps.LatLng(tempLat, tempLong), map.zoom);
		});

	}
		
    $(function(){    
        $('select#valueAA').selectToUISlider({labels:6,sliderOptions: {slide: function(e,ui) {
                    //console.log(e);
                    reshow_outbreaks(e,ui);
                    return true;
                }}});

        fixToolTipColor();
    });
	
    //purely for theme-switching demo... ignore this unless you're using a theme switcher
    //quick function for tooltip color match
    function fixToolTipColor(){
            //grab the bg color from the tooltip content - set top border of pointer to same
            $('.ui-tooltip-pointer-down-inner').each(function(){
                    var bWidth = $('.ui-tooltip-pointer-down-inner').css('borderTopWidth');
                    var bColor = $(this).parents('.ui-slider-tooltip').css('backgroundColor')
                    $(this).css('border-top', bWidth+' solid '+bColor);
            });	
    }
    function pageisLoaded(){
      
        
        ui={value:document.getElementById("valueAA").selectedIndex};
		//alert(ui.value);
		//alert(all_weeks[ui.value]);
        reshow_outbreaks(null,ui);               
	}                       
	</script>

    <meta name="viewport" content="initial-scale=1.0, user-scalable=no">
    <meta charset="utf-8">
    <title>Dengue Epidemic Prediction System</title>
    <link href="default.css" rel="stylesheet">
    <script src="https://maps.googleapis.com/maps/api/js?key=AIzaSyD1FztqCQBvCsou7sQOSk-31HfPw63wnZI"></script>
	<link href="default.css" rel="stylesheet">    
	
	<script>
      var map;
      var infoWindow;

      function initialize() {
		//  var myLatLng = new google.maps.LatLng(31.465279, 74.322);
		var town = "";
		
		var myLatLng = new google.maps.LatLng(31.465279, 74.322);
		var z = 10;
		  
        var mapOptions = {zoom: z, center: myLatLng, mapTypeId: google.maps.MapTypeId.ROADMAP };
		 map = new google.maps.Map(document.getElementById('map-canvas'),
            mapOptions);
		
		 if(town != "")
		 {
			infowindow = new google.maps.InfoWindow(); 
			var contentString = '<b>'+town+'</b><br>';
        
       	 	infowindow.setContent(contentString);
        	infowindow.setPosition(myLatLng);
        	infowindow.open(map);
		 }
		 
        var bermudaTriangle = new Array();
		var triangleCoords = new Array();
		var ctaLayer = new google.maps.KmlLayer({
    url: 'https://dl.dropboxusercontent.com/u/95635872/file.kml',
    map: map,
    preserveViewport: true
  });
  ctaLayer.setMap(map);
		
		<?php
		$towns = array();
		$mysongs = simplexml_load_file('Lahore_UC_ver2.KML');
		$i = 0;
		foreach ($mysongs->Document->Folder->Placemark as $eee)
		{
			$towns[$i] = $eee->description;
			
			
		$coordinates = $eee->Polygon->outerBoundaryIs->LinearRing->coordinates;
		$coordinates = preg_replace('!\s+!', ' ', $coordinates);
		$coordinates = explode(' ',$coordinates);?>
		triangleCoords[<?php echo $i; ?>] = [
		<?php
		for($iterator = 0; $iterator < sizeof($coordinates) ;$iterator++)
		{
					$seperate = explode(",",$coordinates[$iterator]);
					if($seperate[0] == NULL)
						continue;
					echo "new google.maps.LatLng(".$seperate[1].", ".$seperate[0].")";
					if($iterator != (sizeof($coordinates) - 2))
						echo ",";
		}?>
		];
		  bermudaTriangle[<?php echo $i; ?>] = new google.maps.Polygon({
          paths: triangleCoords[<?php echo $i ?>],
          strokeColor: '#000000',
          strokeOpacity: 0.6,
          strokeWeight: 1,
          fillColor: '#000000',
          fillOpacity: 0.00
		 // bounds: map.getBounds()
        });
			bermudaTriangle[<?php echo $i ?>].setMap(map);
		//	google.maps.event.addListener(bermudaTriangle[<?php //echo $i ?>], 'click', showArrays<?php //echo $i ?>);
		<?php
		$i++;
		}
		?>
		var circles = {};
		var ucs = {};
		
		<?php
		
		for($i = 0; $i < sizeof($data); $i++)
		{
			if($data[$i]['radius'] <0.01)
				$data[$i]['radius'] = 0.01;
		
			echo "circles['".$data[$i]['time_frame']['start'].">".$data[$i]['time_frame']['end'].">".$i."'] = { center: new google.maps.LatLng(".$data[$i]['coord']['x'].", ". $data[$i]['coord']['y']."), radius: ".$data[$i]['radius']." };";
			echo "ucs['".$data[$i]['time_frame']['start'].">".$data[$i]['time_frame']['end'].">".$i."'] = '".$data[$i]['ucs']."';";

			//echo "var string".$i." = '".$data[$i]['ucs']."';";
		} 
		?>
		
		var circleOptions;
		
		<?php 
		
    	// Construct the circle for each value in citymap. We scale population by 20.
		for($i = 0; $i < sizeof($data); $i++)
		{	
			
 			$raiin=getRainPastFortNigt($data[$i]['time_frame']['start'],$weather,59);
            $temperat=getTempPastFortNigt($data[$i]['time_frame']['start'],$weather,13);
            $probablity=getProb($raiin,$temperat);
	     $prob2=ceil($probablity*100);

			echo "circleOptions = {";
      			echo "strokeColor: '#FF0000',";
      			echo "strokeOpacity: 0.8,";
      			echo "strokeWeight: 2,";
			
			if($probablity<0.4 || $data[$i]['pvalue']>0.001)
				echo "fillColor: '#FFFFFF',";
      			else
      				echo "fillColor: '#F28816',";
      			echo "fillOpacity: 0.5,";
      			echo "map: map,";
      			echo "center: circles['".$data[$i]['time_frame']['start'].">".$data[$i]['time_frame']['end'].">".$i."'].center,";
      			echo "radius: circles['".$data[$i]['time_frame']['start'].">".$data[$i]['time_frame']['end'].">".$i."'].radius * 1000";
    			echo "};";
		
    		echo "all_circles['".$data[$i]['time_frame']['start'].">".$data[$i]['time_frame']['end'].">".$i."'] = new google.maps.Circle(circleOptions);";
		
		echo "var infoWindow".$i." = new google.maps.InfoWindow({
    				content:'<div style=\"width:200px; height:100px\">".
    				"radius: ".$data[$i]['radius']." km</br>".
    				"lat :".$data[$i]['coord']['x']." , </br>".
    				"lon :".$data[$i]['coord']['y']." </br>".
                    "Weather support :".$prob2." % ".
    				"</div>'
    			});";
			
    		echo "google.maps.event.addListener(all_circles['".$data[$i]['time_frame']['start'].">".$data[$i]['time_frame']['end'].">".$i."'], 'mouseover', function(ev){
    				infoWindow".$i.".setPosition(ev.latLng);
    				infoWindow".$i.".open(map);
    			});";
                
             echo "google.maps.event.addListener(all_circles['".$data[$i]['time_frame']['start'].">".$data[$i]['time_frame']['end'].">".$i."'], 'mouseout', function(ev) {
             infoWindow".$i.".close();
             });";
                



/*		echo "google.maps.event.addListener(all_circles['".$data[$i]['time_frame']['start'].">".$data[$i]['time_frame']['end'].">".$i."'], 'mousedown', function() {";
				echo "document.getElementById('uc').value = '".$data[$i]['ucs']."';";
				echo "});";
		echo "google.maps.event.addListener(all_circles['".$data[$i]['time_frame']['start'].">".$data[$i]['time_frame']['end'].">".$i."'], 'mouseout', function() {";
				echo "document.getElementById('uc').value = '';"; 
				echo "});"; */
		}
  		?>
		first_reshow_outbreaks();
		//all_circles[date].setVisible(false);
		var overlay = new google.maps.OverlayView();
		overlay.draw = function() {};
		overlay.setMap(map);
      }


    </script>
  </head>

  <body onLoad="initialize()">	
    
    	<center class="header-text">
    		<p style="font-size:16px">
				<b>Alerts based on Statistical Analysis</b><br/>
                <span style="font-size:11px; position: relative; bottom: 1px;">
                	(Select day from menu below to see the alerts)
                </span>                        
			</p>
			
			<div id="links" style="width:800px; color: #414141; font: normal 13px Tahoma,Geneva,sans-serif; position:relative; top: 3px;" >
				Current Data Set:  <b>Positive Larvae Reports</b>, change to:  
				<a href="http://103.226.216.147/pitb/new/pitb_map.php"> 
					Confirmed Dengue Patients 
				</a>
			</div>
			<br/>
	    </center>    
    
    <div id="map-canvas" style="width: 800px; height: 600px;"></div>
	
	<center>
		<br />
		<p><font size="2"><b>Trend: &nbsp;&nbsp;</b></font>
			<span style="background-color:#ffcc77; border:#999999 1px solid;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span> Potential Threat&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
			<span style="background-color:#ffffff; border:#999999 1px solid;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span> Cause of Concern</p>
	

    	<div style="width:900px;font-size: 80%;">
			<font size="2"><b style="position: relative; bottom: 8px;">Day: &nbsp;</b></font>
			<select style="width:130px;margin-bottom: 20px;" name="valueAA" id="valueAA" onchange="pageisLoaded();">
                <?php
                $temp=$start_date;
                $i=0;
                while($temp<=$end_date){
                    
                    echo "<option value=\"".date("Y/m/d",$temp)."\"";
                    
                    if($i==0){
                        echo " selected=\"selected\" ";
                        $i+=1;
                    }
                            
                    echo ">".date("Y/m/d",$temp)."</option>";
                    $temp+=1*$SECONDS_IN_DAY;
                }
                
                ?>
			</select>	

            <br/><br/>
                        
		</div>
		
		<table class="table table-bordered table-striped" style="width: 1276px; margin-top: 10px">
			<thead>
				<tr>
					<th style="width:200px;text-align: center;">ID</th>
					<th style="text-align: center;">UC Numbers</th>
					<th style="text-align: center;">UC Names</th>
					<th style="width:200px;text-align: center;">Expected Cases</th>
				</tr>
			</thead>
			<tbody id="outbreak-table">
			</tbody>
		</table>
		
	</center>
	
	<br/><br/>
	
  </body>
</html>
