function addToCart(id, name, price) {
    event.preventDefault()
    // promise
    fetch('/api/add-to-cart', {
        method: 'POST',
        body: JSON.stringify({
            'id': id,
            'name': name,
            'price': price
        }),
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
    }).then(function(res) {
        console.info(res)
        return res.json()
    }).then(function(data) {
        console.info(data)
        let counter = document.getElementById("countCart");
        counter.innerText = data.total_quantity
    }).catch(function(err) {
        console.info(err)
    })
}

function pay() {
    if(confirm('Bạn có muốn thanh toán không') == true){
         fetch('/api/pay', {
            method: 'POST'
         }).then(function(res) {
            console.info(res)
            return res.json()
         }).then(function(data) {
            console.info(data)
            if (data.code == 200){

                 location.reload()
                 alert("Đặt hàng thành công")


            }
        }).catch(function(err) {
            console.info(err)
        })
    }
}