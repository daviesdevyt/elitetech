var socket = io("http://" + document.domain + ":" + location.port + "/game");
var connection_status = document.getElementById('connection_status');
socket.on("connect", function () {
	connection_status.innerHTML = "Connected";
})
socket.on("disconnect", function () {
    alert("You are disconnected. Your score wont count if you are offline")
	connection_status.innerHTML = "Connecting ...";	
})
socket.on("getBalance", function (balance) {
	document.getElementById('balance').innerHTML = (balance).toFixed(5);})
socket.on("earningLimit", function () {
	alert("You have rached your earning limit for today. You no longer be earning tokens from your points until your next mining cycle")})
