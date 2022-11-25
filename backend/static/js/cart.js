var updateBtns = document.getElementsByClassName('update-cart')

for (i = 0; i < updateBtns.length; i++) {
	updateBtns[i].addEventListener('click', function(){
		var productId = this.dataset.product
		var quotationId = this.dataset.quotation
		var action = this.dataset.action
		console.log('productId:', productId, 'QuotationId:', quotationId, 'Action:', action)
		console.log('USER:', user)

		if (user == 'AnonymousUser'){
			addCookieItem(productId, quotationId, action)
		}else{
			updateUserOrder(productId, quotationId, action)
		}
	})
}

function updateUserOrder(productId, quotationId, action){
	console.log('User is authenticated, sending data...')

		var url = '/update-quotation/'

		fetch(url, {
			method:'POST',
			headers:{
				'Content-Type':'application/json',
				'X-CSRFToken':csrftoken,
			}, 
			body:JSON.stringify({'productId':productId, 'quotationId':quotationId, 'action':action})
		})
		.then((response) => {
		   return response.json();
		})
		.then((data) => {
		    console.log('data:', data)
		});
}