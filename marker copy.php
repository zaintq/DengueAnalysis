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
    
    error_reporting(E_ALL);

    $total_clusters = intval($_GET['c']);
    
    echo "var total_clusters = ".$total_clusters.";";
    echo "var hull_data = [];";
    echo "var coords_data = [];";
    
    $hull_data = array();
    $coords_data = array();
    
    for ($i = 0; $i < $total_clusters; $i++) {

      $hull_filename = 'convex_hull_cluster'.$i.'.csv';
      $coords_filename = 'cluster'.$i.'.csv';

      $hull_file = fopen($hull_filename, 'r');
      $coords_file = fopen($coords_filename, 'r');
      
      echo "var hull_lines = [];";
      
      while (($line = fgetcsv($hull_file)) !== FALSE) {
        echo "hull_lines.push({lat: ".floatval($line[0]).", lng: ".floatval($line[1])."});";
      }

      echo "hull_data[".$i."] = hull_lines;";

      echo "var coords_lines = [];";
      
      while (($line = fgetcsv($coords_file)) !== FALSE) {
        echo "coords_lines.push({lat: ".floatval($line[0]).", lng: ".floatval($line[1])."});";
      }
      
      echo "coords_data[".$i."] = coords_lines;";
      
      fclose($hull_file);
      fclose($coords_file);
    }

    ?>

    </script>
    
    <div id="map"></div>

    <script>

      function initMap() {

        var colors = [
          "#000000",
          "#0000FF",
          "#8A2BE2",
          "#A52A2A",
          "#5F9EA0",
          "#DC143C",
          "#D2691E",
          "#B8860B",
          "#006400",
          "#2F4F4F",
          "#DAA520",
          "#FF69B4",
          "#00FF00",
          "#FFA500",
          "#008080",
          "#FFFF00",
          "#9ACD32",
          "#66CDAA",
          "#87CEFA",
          "#F0E68C",
        ];

        // initiate map
        var map = new google.maps.Map(document.getElementById('map'), {
          zoom: 12,
          center: hull_data[0][0],
          mapTypeId: google.maps.MapTypeId.TERRAIN
        });

        for (var i = 0; i < total_clusters; i++) {

          // place the markers
          var markerCoords = coords_data[i];
          var markers = [];

          for (var j = 0; j <= markerCoords.length; j++){
            markers[j] = new google.maps.Marker({
              position: markerCoords[j],
              map: map,
            });
          }

          // create poly lines
          var flightPlanCoordinates = hull_data[i];
          var flightPath = new google.maps.Polyline({
            path: flightPlanCoordinates,
            geodesic: true,
            //strokeColor: '#0000FF',
            strokeColor: colors[i%20],
            strokeOpacity: 1.0,
            strokeWeight: 3
          });

          flightPath.setMap(map);
        }
        
      }
      

    </script>

    <script
        src="https://maps.googleapis.com/maps/api/js?signed_in=true&callback=initMap">
    </script>
  
  </body>
</html>