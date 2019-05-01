var eventSource = new EventSource("/stream")

eventSource.onmessage = function(e) {
  var targetContainer = document.getElementById("target_div");
  targetContainer.innerHTML = e.data;
};