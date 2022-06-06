var socket = io("http://" + document.domain + ":" + location.port + "/account");

function fmt(t){
  if (t < 10) return "0"+t.toString();
  return t.toString()
}
function format_time(h, m, s){
  h = fmt(h)
  m = fmt(m)
  s = fmt(s)
  return `${h}:${m}:${s}`
}
socket.on("miningStatus", function (data) {
    if (!data.mining) return;
    $("#mine").prop('disabled', true);
    var countDownDate = new Date(data.next).getTime();
    var now = new Date(data.current_time).getTime();
    var x = setInterval(function() {
      now += 1000;
      var distance = countDownDate - now;
      var hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
      var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
      var seconds = Math.floor((distance % (1000 * 60)) / 1000);

    $("#mine").html(`<i class='fa fa-clock-o'></i>  ${format_time(hours, minutes, seconds)}`);
    //   }
    }, 1000);
})

$(document).ready(function () {
  $("#mine").click((e) => {
      socket.emit("startMine");
      $("#mine").html('Loading ...');
      $("#mine").prop('disabled', true);
    }
  )})

socket.on("getBalance", function (balance) {
  document.getElementById('mined').innerHTML = (balance).toFixed(5);})