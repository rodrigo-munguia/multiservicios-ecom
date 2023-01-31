from django.conf import settings
from .models import Order, OrderItem, Item
from datetime import datetime
from django.utils import timezone
import pytz
from .mail import Send_remainder_mail_to_client, Send_cancel_mail_to_client


def convert_to_localtime(utctime):
    fmt = '%d/%m/%Y %H:%M'
    utc = utctime.replace(tzinfo=pytz.UTC)
    localtz = utc.astimezone(timezone.get_current_timezone())
    return localtz.strftime(fmt)

def test_task():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("Current Time =", current_time)
    

#-----------------------------------------------
# function for deleting orders (and put their items to stock back) if orders have been
# in kart for more than X minutes
def polling_kart_orders():    
    print("polling kart orders..")
    now = datetime.now(timezone.utc)
    # get orders in kart
    orders_in_kart = Order.objects.filter(ordered = False)
    
        
    for order_k in orders_in_kart:          
        delta_t = now - order_k.start_date
        elapsed_minutes = delta_t.seconds/60
               
        if elapsed_minutes > settings.MINUTES_IN_KART: # if the order in kart has been active more than X minutes
            print(delta_t) 
            print("kart time expired for order")
            print(order_k.order_number)
            order_items = OrderItem.objects.filter(order = order_k)
            # remove from kart and get back to stock
            for order_it in order_items:
                item_i = order_it.item
                quantity = order_it.quantity
                #print(item_i)
                #print(quantity)                
                item = Item.objects.get(slug = item_i.slug)
                item.stock += quantity
                item.save()
                order_it.delete()
            order_k.delete()
             
              

    
#-----------------------------------------------
# function for deleting pick_up orders (and put their items to stock back) if the order has been not
# complete (payed) in more than X hours.
# After deleting/canceling the order, send a remainder emil to the customer in Y hours 
def polling_pick_up_orders():
    print("polling pick up orders..")    
    now = datetime.now(timezone.utc)        
    # get pickup        
    pu_orders = Order.objects.filter(delivery_option='P',complete = False)
    
    for order in pu_orders:
        delta_t = now - order.ordered_date
        elapsed_hours = delta_t.seconds/3600
        
        if elapsed_hours > settings.HOURS_TO_REMAINDER_FOR_PICKUP_ORDERS and order.reminder == False:
            print(delta_t) 
            print("Reminder for order")
            print(order.order_number)
            order_items = OrderItem.objects.filter(order = order)
            Send_remainder_mail_to_client(order, 'P', order_items)
            order.reminder = True
            order.save()
        
        if elapsed_hours > settings.HOURS_TO_CANCEL_PICKUP_ORDERS:
            print(delta_t) 
            print("Cancel for order")
            print(order.order_number)
            order_items = OrderItem.objects.filter(order = order)
            Send_cancel_mail_to_client(order, 'P', order_items)
            for order_it in order_items:
                item_i = order_it.item
                quantity = order_it.quantity
                #print(item_i)
                #print(quantity)                
                item = Item.objects.get(slug = item_i.slug)
                item.stock += quantity
                item.save()
                order_it.delete()
            order.delete()
            
#----------------------------------------------------------------
            
            
            
        
    
         
    
    
    
