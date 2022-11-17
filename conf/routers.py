class ApplicationRouter:
    
    route_app_label = ["account", "cfe"]
    
    
    def db_for_read(self, model, **hints):
        """
        If the model is from account, it suggests querying the account database. 
        If the model is from app2, then app2
       """
        if model._meta.app_label in self.route_app_label:
            return model._meta.app_label
        return None
    
    def db_for_write(self, model, **hints):
        """
        If the model is from account, it suggest querying account app database
        """
        if model._meta.app_label in self.route_app_label:
            return model._meta.app_label
        return None
    
    def allow_for_relation(self, obj1, obj2, **hints):
        if(obj1._meta.app_label in self.route_app_label or obj2._meta.app_label in self.route_app_label):
            return True
        return None
    
    
    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """Ensure that account only appear in the account database"""
        if app_label in self.route_app_label:
            return db == app_label
        return None
    
    
    
            