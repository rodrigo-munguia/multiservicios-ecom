from apscheduler.schedulers.background import BackgroundScheduler
from .tasks import test_task, polling_pick_up_orders, polling_kart_orders

#https://apscheduler.readthedocs.io/en/latest/modules/triggers/cron.html

def start():
    scheduler = BackgroundScheduler()
    
    # for testing
    #scheduler.add_job(polling_kart_orders, 'interval', seconds=10)
    #scheduler.add_job(polling_pick_up_orders, 'interval', seconds=10)
    
    scheduler.add_job(polling_pick_up_orders, "cron", hour='0,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22')
    scheduler.add_job(polling_kart_orders, 'interval', minutes=15)
    
    scheduler.start()
    
    