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
        let counter = document.getElementsByClassName("countCart");
        for (let i = 0 ; i < counter.length; i++)
            counter[i].innerText = data.total_quantity
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
function updateCart(id, obj){

    fetch('/api/update-cart' ,{
        method:'put',
        body:JSON.stringify({
            'id':id,
            'quantity': parseInt(obj.value)
        }),
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
    }).then(res => res.json()).then(data => {
        let counter = document.getElementsByClassName('countCart');
        for (let i = 0 ; i < counter.length; i++)
            counter[i].innerText = data.total_quantity
        let total_amount = document.getElementById("total_amount")
        total_amount.innerText=new Intl.NumberFormat().format(data.total_amount);
    })
}

function deleteCart(id) {
    if(confirm('Bạn có muốn thanh toán không') == true) {
        fetch('/api/delete-cart/' + id ,{
        method:'delete',
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
    }).then(res => res.json()).then(data => {
        let counter = document.getElementsByClassName('countCart');
        for (let i = 0 ; i < counter.length; i++)
            counter[i].innerText = data.total_quantity
        let total_amount = document.getElementById("total_amount")
        total_amount.innerText=new Intl.NumberFormat('en-US', {style: 'decimal'}).format(data.total_amount);
        let e = document.getElementById("product"+id)
        e.style.display = 'none'
    })
    }
}
function addComment(productId) {
    let content = document.getElementById("commentId")
    if (content.value.length > 0)
    {
        fetch('/api/add-comment', {
            method: 'POST',
            body: JSON.stringify({
                'product_id':productId,
                'content':content.value.trim()
            }),
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
    }).then(res => res.json()).then(data => {
        if(data.status == 201){
            let c = data.comment
            let commentA = document.getElementById("commentArea")
            commentA.innerHTML = `
                    <div class="row">
                        <div class="col-md-1 col-xs-4">
                            <img src="${c.user.avatar}" width="50px" height="50px" class="rounded-circle">
                        </div>

                          <div class="col-md-11 col-xs-8" style="border: 1px solid;border-radius: 20px;background-color: #E5eaea;">
                             <span style="font-weight:bold;">${c.user.name}  &ensp; </span><em>vài giây trước</em>
                            <br><br>
                            <h6>${c.content}</h6>
                        </div>
                   </div>
                   <br>
            ` + commentA.innerHTML
        }
        else if (data.staus == 404){
            alert(data.err_msg)
        }
    })
    }
    else
          alert("Nội dung bình luận đang trống")
}