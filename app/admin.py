
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView


class _Admin(Admin):
    def add_model_view(self, model, db):
        self.add_view(ModelView(model, db.session))

    def add_model_views(self, models, db):
        for model in models:
            self.add_model_view(model, db)
