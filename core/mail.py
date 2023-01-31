from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string



def Send_mail_to_client(order,order_type,order_items):
    
    # send mail to client
    merge_data = {
    'order': order, 'order_items':order_items
    }
    
    mail = order.ShippingAddress.email
    
    #subject = render_to_string("message_subject.txt", merge_data).strip()
    subject = 'Order ' + order.order_number + ' confirmation'
    #text_body = render_to_string("message_body.txt", merge_data)
    text_body = ""
    html_body = render_to_string("mail_order_conf.html", merge_data)

    msg = EmailMultiAlternatives(subject=subject, from_email= 'Multiservicios-ecom <settings.EMAIL_HOST_USER>',                                 
                                to=[mail], body=text_body)
    msg.attach_alternative(html_body, "text/html")
    msg.send()
    
    # auto send mail
    
def Send_mail_to_seller(order,order_type,order_items):    
    
    msg = ('The order: ' + order.order_number + ' has been received' 
          )
    if order.delivery_option == "P":
        msg = msg + " for pick up"
    if order.delivery_option == "S":
        msg = msg + " for shipping"
    
    msg = msg + '\n\nItems in order: \n' 
    
    for o_item in order_items:
        msg = msg + str(o_item.quantity) + " of " + o_item.item.title + '\n'
    
    subject = 'The order ' + order.order_number + ' has been received'
    
    if order.delivery_option == "P":
        subject = subject + " for pick up"
    if order.delivery_option == "S":
        subject = subject + " for shipping"
        
    
    send_mail(
            subject= subject,            
            message= msg,           
            from_email = settings.EMAIL_HOST_USER,
            recipient_list=[settings.EMAIL_HOST_USER]
            ) 
    
    

def Send_remainder_mail_to_client(order,order_type,order_items):
     # send mail to client
    merge_data = {
    'order': order, 'order_items':order_items
    }
    
    mail = order.ShippingAddress.email
    
    #subject = render_to_string("message_subject.txt", merge_data).strip()
    subject = 'Remainder for Order ' + order.order_number 
    #text_body = render_to_string("message_body.txt", merge_data)
    text_body = ""
    html_body = render_to_string("mail_order_remainder.html", merge_data)

    msg = EmailMultiAlternatives(subject=subject, from_email= 'Multiservicios-ecom <settings.EMAIL_HOST_USER>',                                 
                                to=[mail], body=text_body)
    msg.attach_alternative(html_body, "text/html")
    msg.send() 
    

def Send_cancel_mail_to_client(order,order_type,order_items):
     # send mail to client
    merge_data = {
    'order': order, 'order_items':order_items
    }
    
    mail = order.ShippingAddress.email
    
    #subject = render_to_string("message_subject.txt", merge_data).strip()
    subject = 'Your Order ' + order.order_number + 'has been canceled'
    #text_body = render_to_string("message_body.txt", merge_data)
    text_body = ""
    html_body = render_to_string("mail_order_cancel.html", merge_data)

    msg = EmailMultiAlternatives(subject=subject, from_email= 'Multiservicios-ecom <settings.EMAIL_HOST_USER>',                                 
                                to=[mail], body=text_body)
    msg.attach_alternative(html_body, "text/html")
    msg.send()       