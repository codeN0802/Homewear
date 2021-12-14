from mysale import app, db,utils
from flask_admin import Admin,BaseView,expose, AdminIndexView
from mysale.models import *
from flask_admin.contrib.sqla import ModelView
from flask_login import logout_user,current_user
from flask import redirect,request
from datetime import datetime
admin = Admin(app=app, name='Quản trị bán hàng',template_mode='bootstrap4')

class AuthenticatedModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN

class ProductView(AuthenticatedModelView):
    column_display_pk = True
    can_view_details = True
    can_export = True
    column_searchable_list = ['name', 'description', 'price']
    column_filters = ['name', 'description', 'price']
    column_exclude_list = ['image', 'active']
    column_labels = {
        'name' : 'Tên sản phẩm',
        'description' : 'Mô tả',
        'price' : 'Gía',
        'created_date' : 'Ngày tạo'
    }
class CategoryView(AuthenticatedModelView):
    column_display_pk = True



class Logoutview(BaseView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect("/admin")

    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN
class StatsView(BaseView):
    @expose('/')
    def index(self):
        kw = request.args.get('keyword')
        from_date=request.args.get('from_date')
        to_date=request.args.get('to_date')
        year = request.args.get('year', datetime.now().year)
        stats = utils.product_count_by_cate()
        stats_product = utils.count_product_stats(kw=kw,from_date=from_date,to_date=to_date)
        doanhthu= utils.doanhthu(year=year)
        return self.render('admin/stats.html',stats=stats, stats_product=stats_product, doanhthu=doanhthu)
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN

admin.add_view(CategoryView(Category,db.session))
admin.add_view(ProductView(Product,db.session, name='Sản phẩm'))
admin.add_view(AuthenticatedModelView(User,db.session))
admin.add_view(AuthenticatedModelView(Receipt, db.session, name='Hóa đơn'))
admin.add_view(AuthenticatedModelView(ReceiptDetail, db.session, name='Chi tiết hóa đơn'))
admin.add_view(StatsView(name='Thống kê'))
admin.add_view(Logoutview(name='Đăng xuất'))