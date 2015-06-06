<!DOCTYPE html>
<html>
  <head>
    <meta name="viewport" content="initial-scale=1.0, user-scalable=no">
    <meta charset="utf-8">
    <title>Simple markers</title>
    <style>
      html, body {
        height: 100%;
        margin: 0;
        padding: 0;
      }
      #map {
        height: 100%;
      }
    </style>
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js"></script>

  </head>
  <body>

    <script type="text/javascript">
    <?php
	    echo "var coords_data = [];";
    	
	    $coords_data = array();
		
		if(isset($_GET["year"])){
			$coords_filename = 'irs_patients_'.$_GET["year"].'.csv';
		}else{
			$coords_filename = 'irs_patients_all.csv';
		}

	    $coords_file = fopen($coords_filename, 'r');

	    echo "var coords_data = [];";
		echo "var total_clusters = 1;";
  	  	
		$first_line = true;
	    while (($line = fgetcsv($coords_file)) !== FALSE) {
			if(!$first_line)
				echo "coords_data.push({lat: ".floatval($line[2]).", lng: ".floatval($line[3])."});";
			$first_line = false;
	    }
		
	    fclose($coords_file);
    ?>
	console.log("cooords", coords_data);
    </script>
    
    <div id="map"></div>

    <script>

    function initMap() {
      var markerCoords = coords_data;

      var map = new google.maps.Map(document.getElementById('map'), {
        zoom: 11,
        center: markerCoords[0]
      });

      var markers = [];
      for (var i = 0; i <= markerCoords.length; i++){
        markers[i] = new google.maps.Marker({
          position: markerCoords[i],
          map: map,
        });
      }
    }

    </script>

    <script
        src="https://maps.googleapis.com/maps/api/js?&key=AIzaSyAq2lxSeMQ_zPr-52sYgG-MwUlvKBYmMeU&signed_in=true&callback=initMap">
    </script>
  
  </body>
</html>