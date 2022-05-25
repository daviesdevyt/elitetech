
// function sell(){
// 	tokenAmount = $('#input').val().toString();
// 	tokenAmount = web3.utils.toWei(tokenAmount, 'Ether')
// 	token.methods.approve(swapAddress, tokenAmount).send({ from: account }).on('transactionHash', (hash) => {
// 		console.log("Approved !!");
// 		swap.methods.sellTokens(tokenAmount).send({ from: account }).on('transactionHash', (hash) => {
// 			console.log("Tokens sold")
// 		})
// 	})
// }