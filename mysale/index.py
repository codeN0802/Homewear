from flask import Flask,render_template,request,redirect,url_for,abort,Response,session,jsonify
from mysale import app,utils,login,mail
import math
import cloudinary.uploader
from flask_login import login_user,logout_user, login_required,current_user
from flask_mail import Mail, Message
@app.route("/")
def home():

    # cates = utils.read_categories()
    cate_id = request.args.get("category_id")
    kw = request.args.get("keyword")
    from_price = request.args.get("from_price")
    to_price = request.args.get("to_price")
    page = request.args.get("page",1)

    products = utils.read_prodcuts(cate_id=cate_id ,kw=kw,from_price=from_price,to_price=to_price, page=int(page))
    counter = utils.count_products()
    counter_cate = utils.count_products_cate(cate_id=cate_id)
    return render_template("index.html",
                            # categories = cates
                            products= products,pages= math.ceil(counter/app.config['PAGE_SIZE']),
                           pages_cate = math.ceil(counter_cate/app.config['PAGE_SIZE']))
@app.route("/register", methods=['get','post'])
def user_register():
    err_msg= ""
    if request.method.__eq__("POST"): #POST PHẢI IN HOA
        name = request.form.get("name")
        email = request.form.get('email')
        username = request.form.get("username")
        password = request.form.get("password")
        confirm = request.form.get("confirm")

        try:
            if password.strip().__eq__(confirm.strip()):
                avatar = request.files.get('avatar')
                if avatar:
                    res= cloudinary.uploader.upload(avatar)
                    avatar_path = res['secure_url']

                msg = Message('Vy Nguyễn Homewear', sender='nghinguyen08022000@gmail.com',
                              recipients=[email])
                msg.body = "Cám ơn bạn đã đăng ký tài khoản"
                mail.send(msg)
                utils.add_user(name=name, email=email, username=username, password=password, avatar=avatar_path)
                return redirect(url_for('user_login'))
            else:
                err_msg = "Mật khẩu không khớp"
        except :
                db.session.rollback() #sqlalchemy.exc.PendingRollbackError
                err_msg = "Username hoặc Email đã có trên hệ thống"
    if current_user.is_authenticated: # chặn đã đăng nhập không được vô login
        return redirect(url_for('home'))
    return render_template("register.html", err_msg=err_msg)

@app.route("/login", methods=['get','post'])
def user_login():
    err_msg = ""
    if request.method.__eq__('POST'):
        username = request.form.get("username")
        password = request.form.get("password")
        user = utils.check_login(username=username,password=password)
        if user:
            login_user(user=user) #ghi nnhaan trang thai da dang nhap

            next = request.args.get('next', 'home')
            return redirect(url_for(next))
        else:
            err_msg = "Vui lòng kiểm tra lại Username và Password"
    if current_user.is_authenticated: # chặn đã đăng nhập không được vô login
        return redirect(url_for('home'))
    return render_template("login.html",err_msg=err_msg)
@app.route("/logout")
def user_logout():
    logout_user()
    return redirect(url_for('user_login'))



@app.route("/admin-login", methods=['post'])
def admin_login():
    err_msg = ""
    if request.method.__eq__('POST'):
        username = request.form.get("username")
        password = request.form.get("password")
        user = utils.check_adminlogin(username=username,password=password)
        if user:
            login_user(user=user)  # ghi nnhaan trang thai da dang nhap
            return redirect('/admin')
        else:
            err_msg ="Vui lòng kiểm tra lại Username hoặc Password"
            return  abort(Response(err_msg))




@app.context_processor
def common_reponse():
    return {
        'categories': utils.read_categories(),
        'cart_stats':utils.count_cart(session.get('cart'))

    }
@login.user_loader
def user_load(user_id):
    return utils.get_user_by_id(user_id=user_id)

@app.route("/cart")
def cart():
    return render_template("cart.html",stats = utils.count_cart(session.get('cart'))) # nen dung get

@app.route('/api/add-to-cart', methods=['post'])
def add_to_cart():
    data = request.json
    id = str(data.get('id'))
    name = data.get('name')
    price = data.get('price')

    cart = session.get('cart')
    if not cart:
        cart = {}

    if id in cart:
        cart[id]['quantity'] = cart[id]['quantity'] + 1
    else:
        cart[id] = {
            'id': id,
            'name': name,
            'price': price,
            'quantity': 1
        }

    session['cart'] = cart

    return jsonify(utils.count_cart(cart))
@app.route('/api/pay', methods=['post'])
@login_required
def pay():


    try:
        utils.add_receipt(session.get('cart'))
        
        msg = Message('Vy Nguyễn Homewear', sender='nghinguyen08022000@gmail.com',
                      recipients=[current_user.email])
        msg.body = "Bạn đặt hàng thành công"
        mail.send(msg )
        del session['cart']
    except:
        return jsonify({'code':400})
    return jsonify({'code':200})

@app.route("/products")
def products_list():
    cates = utils.read_categories()
    cate_id = request.args.get("category_id")
    kw = request.args.get("keyword")
    from_price = request.args.get("from_price")
    to_price = request.args.get("to_price")
    products = utils.read_prodcuts(cate_id=cate_id, kw=kw, from_price=from_price,to_price=to_price)
    return render_template("products.html", products=products,categories = cates)


@app.route("/profile")
@login_required
def profile():
    return render_template("profile.html")
@app.route("/products/<int:product_id>")
def product_detail(product_id):
    product = utils.get_product_by_id(product_id)
    return render_template("product_detail.html", product=product)


if __name__== "__main__":
    from mysale.admin import *
    app.run(debug=True)