from flask import redirect, url_for, request
from flask_admin import Admin as FlaskAdmin, AdminIndexView, expose, BaseView
from flask_admin.contrib.sqla import ModelView as FlaskModelView
import flask_login as login


class Admin(FlaskAdmin):
    def add_model_view(self, model, db):
        self.add_view(ModelView(model, db.session))

    def add_model_views(self, models, db):
        for model in models:
            self.add_model_view(model, db)

class ModelView(FlaskModelView):
    def is_accessible(self):
        return login.current_user.is_administrator()

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('auth.login', next=request.url_rule))


class SecuredHomeView(AdminIndexView):
    @expose('/')
    def index(self):
        if self.admin._menu[0].name == 'Home':
            del self.admin._menu[0]
        return self.render('/admin/index.html')

    def is_accessible(self):
        return login.current_user.is_administrator()

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('auth.login', next=request.url_rule))
