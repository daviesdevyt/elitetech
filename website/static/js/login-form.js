$(document).ready(function () {
    $("#checkbox").click(()=>{
        $("#ref").prop("hidden", $("#ref").is(":visible"))
    })
});