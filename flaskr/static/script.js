var eventSource = new EventSource("/stream")

eventSource.onmessage = function(event) {
  var targetContainer = document.getElementById("target_div");
  var data = JSON.parse(event.data);
  targetContainer.innerHTML = data.time;
};