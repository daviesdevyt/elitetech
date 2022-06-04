function calc(){
    amt = $("#amount").val();
    amt_in_bnb = amt*0.0001;
    let dec = Math.pow(10, 18)
    amt_in_bnb = Math.round(amt_in_bnb*dec)/dec
    amt_in_bnb = Math.min(amt_in_bnb, 999999999999999999)
    return amt_in_bnb
}
async function getTransactionReceipt(hash) {
    console.log("Transaction sent!", hash);
    const interval = setInterval(function() {
        console.log("Attempting to get transaction receipt...");
        web3.eth.getTransactionReceipt(hash, function(err, rec) {
            if (rec) {
                console.log(rec);
                $("#buy_btn").html("Purchase MCR")
                $("#buy_btn").prop("disabled", false)
                loadToken()
                clearInterval(interval);
            }
    });
}, 1000)}

    
function buy(amt){
	etherAmount = amt.toString();
    etherAmount = web3.utils.toWei(etherAmount, 'Ether');
	swap.methods.buyTokens().send({ value: etherAmount, from: account }).on('transactionHash', (transactionHash) => {
    $("#buy_btn").prop("disabled", true)
    $("#buy_btn").html("Processing...")
    getTransactionReceipt(transactionHash)
})
}
$(document).keyup(function(e) {    
    $("#price").html(calc());
});

$(document).ready(function () {
    $("#buy_btn").click(() => {
        buy(calc())
    })
});
