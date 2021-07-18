var server_address = "http://34.78.224.246:5000/"

var start_date = ""
var end_date = ""
var isFilterOn = false


var get_measurements = function() {
    $.get(server_address+"dso/measurements/", function(data) {
	    var json = JSON.parse(data)
        fetchMeasurementsTable()

        for(var i = 0; i < data.length; i++)
            appendMeasurement(json[i].timestamp,  json[i].temperature, json[i].humidity);
    });
}

var get_devices = function() {
    $.get(server_address+"dso/devices/", function(data) {
	    var json = JSON.parse(data)
        fetchDevicesTable()

        for(var i = 0; i < data.length; i++)
            appendDevice(json[i].device_id, json[i].device_location, json[i].device_state, json[i].device_timestamp, i);
    });
}


var measurements_regular_interval = setInterval(get_measurements, 2000);
var measurements_filtered_interval = ""
var devices_interval = setInterval(get_devices, 2000);


function showHome() {
    document.getElementById('home').style.display = "block";
    document.getElementById('Raspberry').style.display = "none";

    isFilterOn = false;

    toggleMeasurementsInvervals();
}

function showMeasures(button_id) {
    document.getElementById('home').style.display = "none";
    document.getElementById('Raspberry').style.display = "block";

    setDeviceDescription(button_id);
}

function setDeviceDescription(button_id) {
    var device_id = document.getElementById("device_id_col").childNodes[button_id+1].textContent;
    var device_state = document.getElementById("device_state_col").childNodes[button_id+1].textContent;
    var device_location = document.getElementById("device_location_col").childNodes[button_id+1].textContent;
    var device_timestamp = document.getElementById("device_timestamp_col").childNodes[button_id+1].textContent;

    document.getElementById("description_id").textContent = device_id;
    document.getElementById("description_state").textContent = device_state;
    document.getElementById("description_location").textContent = device_location;
    document.getElementById("description_timestamp").textContent = device_timestamp;
}

function removeAllChildNodes(parent) {
    while (parent.firstChild) {
        parent.removeChild(parent.firstChild);
    }
}

function get_measurements_on_interval() {
    request_params = {"start_date": String(start_date), "end_date": String(end_date)};
    $.get(server_address+"dso/measurements_interval", request_params,function(data) {
	    var json = JSON.parse(data)
        fetchMeasurementsTable()

        for(var i = 0; i < data.length; i++)
            appendMeasurement(json[i].timestamp,  json[i].temperature, json[i].humidity);
    });
}

function filterMeasurements () {
    start_date = document.getElementById("start_date").value + " 00:00:00";
    end_date = document.getElementById("end_date").value + " 00:00:00";

    isFilterOn = true;

    toggleMeasurementsInvervals();
}

function toggleMeasurementsInvervals(){
    if(isFilterOn) {
        measurements_filtered_interval = setInterval(get_measurements_on_interval, 2000);
        clearInterval(measurements_regular_interval);
    }

    else {
        measurements_regular_interval = setInterval(get_measurements, 2000);
        clearInterval(measurements_filtered_interval);
    }
}


function fetchMeasurementsTable() {
    removeAllChildNodes(document.getElementById("measurements"));

    var measurements_labels = document.createElement('TR');
    measurements_labels.id = "measurements_labels";

    var time_label = document.createElement('TH');
    time_label.textContent = "Time";
    var temperature_label = document.createElement('TH');
    temperature_label.textContent = "Temperature";
    var humidity_label = document.createElement('TH');
    humidity_label.textContent = "Humidity";

    measurements_labels.appendChild(time_label);
    measurements_labels.appendChild(temperature_label);
    measurements_labels.appendChild(humidity_label);

    document.getElementById("measurements").appendChild(measurements_labels);
}

function fetchDevicesTable() {
    removeAllChildNodes(document.getElementById("device_id_col"));
    removeAllChildNodes(document.getElementById("device_state_col"));
    removeAllChildNodes(document.getElementById("device_location_col"));
    removeAllChildNodes(document.getElementById("device_timestamp_col"));
    removeAllChildNodes(document.getElementById("buttons"));

    var devices = document.createElement('DIV');
    devices.classList += "devices_col";
    devices.textContent = "Devices";

    var state = document.createElement('DIV');
    state.classList += "devices_col";
    state.textContent = "State";

    var location = document.createElement('DIV');
    location.classList += "devices_col";
    location.textContent = "Location";

    var time = document.createElement('DIV');
    time.classList += "devices_col";
    time.textContent = "Time";

    document.getElementById("device_id_col").append(devices);
    document.getElementById("device_state_col").append(state);
    document.getElementById("device_location_col").append(location);
    document.getElementById("device_timestamp_col").append(time);
}


function appendMeasurement(time, temperature, humidity){
    var measurement_instance = document.createElement('TR');
    measurement_instance.classList += "measurement_instance";

    var time_cell = document.createElement('TD');
    time_cell.textContent = time;
    var temperature_cell = document.createElement('TD');
    temperature_cell.textContent = temperature + " C";
    var humidity_cell = document.createElement('TD');
    humidity_cell.textContent = humidity + " %";

    measurement_instance.appendChild(time_cell);
    measurement_instance.appendChild(temperature_cell);
    measurement_instance.appendChild(humidity_cell);

    document.getElementById("measurements").appendChild(measurement_instance);
}

function appendDevice(id, location, state, timestamp, button_id) {
    var devices_columns = [];
    for (var i = 0; i < 4; i++) {
        var devices_col = document.createElement('DIV');
        devices_col.classList += "devices_col";
        devices_columns.push(devices_col);
    }

    var devices_values = [];

    var newId = document.createElement('DIV');
    newId.classList += "id";
    newId.textContent = id;
    devices_values.push(newId);

    var newState = document.createElement('DIV');
    newState.classList += "state";
    newState.textContent = state;
    devices_values.push(newState);

    var newLocation = document.createElement('DIV');
    newLocation.classList += "location";
    newLocation.textContent = location;
    devices_values.push(newLocation);

    var newTimestamp = document.createElement('DIV');
    newTimestamp.classList += "timestamp";
    newTimestamp.textContent = timestamp;
    devices_values.push(newTimestamp);

    var newButton = document.createElement('BUTTON');
    newButton.classList += "device_button";
    newButton.setAttribute("onclick", "showMeasures(" + button_id + ")");
    newButton.textContent = "Measurements";
    newButton.id = button_id;
    devices_values.push(newButton);

    for(var i = 0; i < devices_columns.length; i++)
        devices_columns[i].appendChild(devices_values[i]);

    document.getElementById("device_id_col").append(devices_columns[0]);
    document.getElementById("device_state_col").append(devices_columns[1]);
    document.getElementById("device_location_col").append(devices_columns[2]);
    document.getElementById("device_timestamp_col").append(devices_columns[3]);
    document.getElementById("buttons").append(devices_values[4]);
}



