var eventSource = new EventSource("/stream")

eventSource.onmessage = function(event) {
  var targetContainer = document.getElementById("calender_div");
  var data = JSON.parse(event.data);
  targetContainer.innerHTML = data.calendarEvents;
};

function showMap(map) {
  var targetContainer = document.getElementById("calender_div");
  targetContainer.innerHTML = '<img src=static/images/' + map + '.jpg height="380"></img>';
};
