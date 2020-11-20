# https://stackoverflow.com/questions/49741986/django-migration-to-multiple-databases
class DBRouter:
    """
    A router to control all database operations on models in the
    app application.
    """

    route_app_labels = {"data"}

    def db_for_read(self, model, **hints):
        """
        Attempts to read data models go to data_db.
        """
        if model._meta.app_label in self.route_app_labels:
            return "data_db"
        return "default"

    def db_for_write(self, model, **hints):
        """
        Attempts to write data models go to data_db.
        """
        if model._meta.app_label in self.route_app_labels:
            return "data_db"
        return "default"

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the data apps is
        involved.
        """
        if obj1._meta.app_label in self.route_app_labels or obj2._meta.app_label in self.route_app_labels:
            return True

        if obj1._meta.app_label not in self.route_app_labels and obj2._meta.app_label not in self.route_app_labels:
            return True

        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure the data apps only appear in the
        'data_db' database.
        """
        if app_label in self.route_app_labels:
            return db == "data_db"

        if db == "data_db":
            return False

        return None
