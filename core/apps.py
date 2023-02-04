from django.apps import AppConfig
#from . import schedule
import os


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'
    
    def ready(self):
        from . import scheduler
        if os.environ.get('RUN_MAIN'):
            #scheduler.start()
            pass
    
    

    
    
