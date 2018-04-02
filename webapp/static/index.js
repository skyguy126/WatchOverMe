// This example creates circles on the map, representing populations in North
// America.

var circles = new Array;
var infoWindowLocation;
var firstStateCheck = true;
var showAlert = true;

var prevState = [false, false, false, false, false];
var curState = [false, false, false, false, false];

$(document).ready(function () {
    $("#alert-overlay").click(hideAlertOverlay);
    $("#alert-overlay-box").click(hideAlertOverlay);
    getData();
    setInterval(getData, 1500);
});

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

function getData() {
    $.ajax({
        url : 'http://73.223.184.186:25565/status',
        type: 'GET',
        crossDomain: true,
        success : function (body) {
            for (var x in body) {

                curState[body[x].index] = body[x].state;
                var stateChanged = isStateChanged();

                if (body[x].state) {
                    circles[body[x].index].setOptions({
                        fillColor: '#FF0000', // Red
                        strokeColor: '#FF0000'
                    });

                    if (stateChanged && !firstStateCheck)
                        showAlertOverlay();

                } else {
                    circles[body[x].index].setOptions({
                        fillColor: '#1c73ff', // Blue
                        strokeColor: '#1c73ff'
                    });
                }
            }

            firstStateCheck = false;
        },
        error : function (err) {
            console.log(err);
        }
    })
}

function isStateChanged() {
    var isSame = true;
    for (var i = 0; i < curState.length; i++) {
        if (curState[i] != prevState[i])
            isSame = false;
    }

    prevState = curState.slice();
    return !isSame;
}

function showAlertOverlay() {
    if (showAlert) {
        showAlert = false;
        $("#alert-overlay").addClass("fadein-visibility");
        $("#alert-overlay-box").addClass("fadein-visibility");
        $("#alert-overlay").addClass("fadein-overlay");
        $("#alert-overlay-box").addClass("fadein-overlay-box");
    }
}

function hideAlertOverlay() {
    $("#alert-overlay").removeClass("fadein-overlay");
    $("#alert-overlay-box").removeClass("fadein-overlay-box");
    sleep(400);
    $("#alert-overlay").removeClass("fadein-visibility");
    $("#alert-overlay-box").removeClass("fadein-visibility");
    setTimeout(resetAlertOverlay, 10000);
}

function resetAlertOverlay() {
    console.log("reseting alert overlay params...");
    showAlert = true;
}

// First, create an object containing LatLng and population for each city.
var citymap = {
    c1: {
        center: {lat: 34.065816, lng: -118.446825},
        population: 1,
        location: "Ronald Reagan UCLA Medical Center"
    },
    c2: {
        center: {lat: 34.066208, lng: -118.443284},
        population: 1,
        location: "UCLA School of Public Health"
    },
    c3: {
        center: {lat: 34.067822, lng: -118.444637},
        population: 1,
        location: "UCLA Parking Structure 9"
    },
    c4: {
        center: {lat: 34.069583, lng: -118.442405},
        population: 1,
        location: "Mathematical Sciences Building"
    },
    c5: {
        center: {lat: 34.070804, lng: -118.447448},
        population: 1,
        location: "Pauley Pavilion"
    },
};



function initMap() {
    // Create the map.
    var map = new google.maps.Map(document.getElementById('map'), {
        zoom: 16,
        center: {lat: 34.067859, lng: -118.444559},
        mapTypeId: 'roadmap' //'terrain'
    });

    infoWindowLocation = new google.maps.InfoWindow;
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function(position) {
            var pos = {
                lat: position.coords.latitude,
                lng: position.coords.longitude
            };

            infoWindowLocation.setPosition(pos);
            infoWindowLocation.setContent('Your location.');
            infoWindowLocation.open(map);
            map.setCenter(map.center);

        }, function() {
            console.log("couldnt get location 1");
        });
    } else {
        console.log("couldnt get location 2");
    }

    // Construct the circle for each value in citymap.
    // Note: We scale the area of the circle based on the population.
    for (var city in citymap) {
      var infowindow = new google.maps.InfoWindow;
        // Add the circle for this city to the map.
        var cityCircle = new google.maps.Circle({
            strokeColor: '#1c73ff',
            strokeOpacity: 0.8,
            strokeWeight: 2,
            fillColor: '#1c73ff',
            fillOpacity: 0.35,
            map: map,
            center: citymap[city].center,
            radius: Math.sqrt(citymap[city].population) * 85,
            clickable: true
        });

        google.maps.event.addListener(cityCircle, 'click', (function(cityCircle, city){
          return function() {
            infowindow.setContent(citymap[city].location);
            infowindow.setPosition(cityCircle.getCenter());
            infowindow.open(map);
          }
        }) (cityCircle, city));

        circles.push(cityCircle);
    }
}
