var targetContainer = document.getElementById("target_div");
var eventSource = new EventSource("/stream")
  eventSource.onmessage = function(e) {
  targetContainer.innerHTML = e.data;
};