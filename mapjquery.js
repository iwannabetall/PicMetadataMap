// $(document).ready(function(){




// })


var metadata = metadata_gps;
var markers;
var locations = []
markerarray = []
// hard code list of locations to animate 
var locationList = ["I_eland", "China", "Australia", "Tahoe-SF", "Eclipse", "Borrego Springs", "Florida - Key Largo", "France", "London/Scotland", "Arizona"]

for (i=0; i < metadata.length; i++){
// var inListIndex = locationList.indexOf(metadata[i].location)
// if (inListIndex == -1) {
//   locationList.push(metadata[i].location)
// }
locations.push({lat:metadata[i].latitude, lng: metadata[i].longitude})
}




var map;

function initMap() {

console.log('wtf')
map = new google.maps.Map(document.getElementById('map'), {
  zoom: 3,
  center: {lat:21.289373, lng:-157.917480}
});

// Create an array of alphabetical characters used to label the markers.
var labels = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';

// Add some markers to the map.
// Note: The code uses the JavaScript Array.prototype.map() method to
// create an array of markers based on a given "locations" array.
// The map() method here has nothing to do with the Google Maps API.
markers = locations.map(function(location, i) {
  return new google.maps.Marker({
    position: location,
    label: labels[i % labels.length]
  });
});

// Add a marker clusterer to manage the markers.
var markerCluster = new MarkerClusterer(map, markers,
    {imagePath: 'https://developers.google.com/maps/documentation/javascript/examples/markerclusterer/m'});

var markerpoints = locations.map(function(location, i) {
  var markerpoint = new google.maps.Marker({
    position: location,             
    map: map
})
  markerarray.push(markerpoint)
})        
}

function ShowAll() {  
markerarray.forEach(function(marker) {
  marker.setMap(map);
});
}    

function HideAll() {
markerarray.forEach(function(marker) {
  marker.setMap(null);
});
}  

function ZoomOut() {  
//zoom out faster than scrolling repeatedly
var zoomlevel = map.getZoom()
// map.panTo(markerarray[visible].getPosition());
if (Math.floor(zoomlevel/2) < 3){
map.setZoom(3)
}
else{
map.setZoom(Math.floor(zoomlevel/2))
}
}