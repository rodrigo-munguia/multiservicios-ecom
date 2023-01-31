from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from .models import Item, OrderItem, Order, ShippingAddress, Payment, Category
from django.views.generic import ListView, DetailView, View
from django.utils import timezone
from datetime import datetime
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from .forms import CheckoutForm
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from .mail import Send_mail_to_client, Send_mail_to_seller 
import stripe
import json
#stripe.api_key = settings.STRIPE_SECRET_KEY
#stripe.api.key = settings.STRIPE_PUBLIC_KEY
stripe.api_key = settings.STRIPE_SECRET_KEY
endpoint_secret = settings.STRIPE_WEBHOOK_KEY

# Create your views here.

def item_list(request):
    context = {
        'items': Item.objects.all()
    }
    return render(request,"home-page.html",context)

def products(request):
    context = {
        'items':Item.objects.all()
    }
    return render(request,"product.html",context)

class CheckoutView(View):
       
    def get(self,*args,**kwargs):
        try:
            form = CheckoutForm()
            order = Order.objects.get(user=self.request.user,ordered = False)
            order_items = OrderItem.objects.filter(order = order)
            context = {
                'form': form,
                'order': order,
                'order_items': order_items
            }        
            return render(self.request,"checkout.html",context)
        except:
            messages.info(self.request,"You dont have products in your cart.")
            return redirect("core:home")
            
    
    def post(self,*args,**kwargs):
        form = CheckoutForm(self.request.POST or Node)
        try:
            order = Order.objects.get(user=self.request.user,ordered = False)
            
            delivery_option = form.data.get('delivery_option')
            
            payment_type = 'S' #set default payment type to stripe 
                
            
            if delivery_option == 'P': 
                # if the choice is pick up then the folowing fields are no longer required
                form.fields['street_address'].required = False
                form.fields['apartment_address'].required = False
                form.fields['zip'].required = False
                form.fields['state'].required = False
                form.fields['municipality'].required = False
                payment_type = 'C' #set payment type to cash
            
            if form.is_valid():
                print(form.cleaned_data)
                print("The form is valid")                     
                                
                name = form.cleaned_data.get('name')
                mobile_phone = form.cleaned_data.get('mobile_phone')
                email = form.cleaned_data.get('email')
                delivery_option = form.cleaned_data.get('delivery_option')
                
                street_address = form.cleaned_data.get('street_address')
                apartment_address = form.cleaned_data.get('apartment_address')                
                state = form.cleaned_data.get('state')
                municipality = form.cleaned_data.get('municipality')
                zip = form.cleaned_data.get('zip')
                # TODO: add functionality
                #same_billing_address = form.cleaned_data.get('same_billing_address')
                #save_info = form.cleaned_data.get('save_info')
                payment_option = form.cleaned_data.get('payment_option')
                
                # TODO: add functionality for creating shipping_address only if there is not exist one for the particular order number
                shipping_address = ShippingAddress(
                    user = self.request.user,
                    order_number = order.order_number,
                    name = name,
                    delivery_option = delivery_option,
                    street_address = street_address,
                    apartment_address = apartment_address,
                    mobile_phone = mobile_phone,
                    email = email,
                    state = state,
                    municipality=municipality,
                    zip = zip               
                )
                shipping_address.save()
                
                payment = Payment(
                    user = self.request.user,
                    order_number = order.order_number,
                    payment_type = payment_type,
                    amount = order.get_total()
                )
                payment.save()
                
                
                #order.order_number = new_order_number
                order.ordered_date = datetime.now()
                order.delivery_option = delivery_option
                order.ShippingAddress = shipping_address
                order.payment = payment                            
                order.save()
                
                order_items = OrderItem.objects.filter(order = order)
                for item in order_items:
                    item.ordered =  True
                    item.save()                
                    
                if delivery_option == 'P':
                    #messages.warning(self.request, "Order: " + order.order_number )
                    order.ordered = True
                    order.save()
                   # self.request.session["mail"] = email   
                    self.request.session["order_number"] = order.order_number
                   # self.request.session["name"] = name
                   # self.request.session["order_items"] = order_items
                    return redirect('core:Order-pick-up-success-View')
                
                if delivery_option == 'S':
                    return redirect('core:create-payment-intent')
        
            # the form is not valid
            for e in form.errors.values():
                print(e)
                messages.warning(self.request, e)
            
            messages.warning(self.request, "Failed checkout")
            return redirect('core:checkout')           
        
        except ObjectDoesNotExist:
            messages.error(self.request,"You do not have an active order")
            return redirect("core:order-summary")
        
     
class Order_pick_up_success_View(View):
    def get(self, *args, **kwargs):        
        order_number =  self.request.session["order_number"] 
        order = Order.objects.get(order_number = order_number)
        #mail = order.ShippingAddress.email
        name = order.ShippingAddress.name
        order_items = OrderItem.objects.filter(order = order)
        
        context = {           
                'order_number': order_number,
                'name' : name            
            }
        
        Send_mail_to_client(order,'P',order_items)
        Send_mail_to_seller(order,'P',order_items)         
        return render(self.request, "order_pickup_success.html",context)           
        
           


class HomeView(ListView):
    #model = Item
    paginate_by = 10
    #template_name = "home.html"
    #context_object_name = 'items'   
    def get(self, *args, **kwargs):       
        #template_name = "home.html"
        #items = Item.objects.get(user=self.request.user,ordered = False)
        items = Item.objects.all()
        categories = Category.objects.all()
        context = {
            'items': items,
            'categories':categories
        }
        return render(self.request, "home.html",context)
    
class HomeSearchView(ListView):   
    paginate_by = 10       
    def get(self, *args, **kwargs):    
        search = self.request.GET.get('search')
        try:
            items = Item.objects.filter(
                Q(title__icontains=search) | Q(category__title__icontains=search) | Q(description__icontains=search)
                )
            
            categories = Category.objects.all()
            context = {
                'items': items,
                'categories':categories
            }
            return render(self.request, "home.html",context)
        except: # if search fails then return all
            items = Item.objects.all()
            categories = Category.objects.all()
            context = {
                'items': items,
                'categories':categories
            }
            return render(self.request, "home.html",context)
            
    
class HomeCategorySearchView(ListView):
    template_name = "home.html"
    model = Item
    context_object_name = 'items'    
    def get_context_data(self, **kwargs):        
        context = super().get_context_data(**kwargs)
        search = self.kwargs.get('pk')
        context["items"] = Item.objects.filter(category__id=search)
        context["categories"] = Category.objects.all()
        return context
    
    """
    def get_queryset(self):       
        queryset = super().get_queryset()
        search = self.kwargs.get('pk')
        
        if search:
            items = Item.objects.filter(category__id=search)
            
            return items
        else:
            return items.none() 
    """
    
    
    
       
    

class OrderSummaryView(LoginRequiredMixin,View):
    def get(self,*args,**kwargs):
        try:
            order = Order.objects.get(user=self.request.user,ordered = False)
            order_items = OrderItem.objects.filter(order = order)
            context = {
                'order': order,
                'order_items': order_items
            }
            return render(self.request,'order_summary.html',context)
        except ObjectDoesNotExist:
            messages.error(self.request,"You do not have an active order")
            return redirect("/")
            
   
    

class ItemDetailView(DetailView):
    model = Item
    template_name = "product.html"
    

def create_ref_code():
        now = timezone.now()        
        # get number of orders created today
        count = Order.objects.filter(ordered_date__date=timezone.now()).count()         
        code = now.strftime("%y%m%d%H%M%S")
        digit = str(count).zfill(3)
        my_code = (code, digit)
        return ''.join(my_code)

@login_required    
def add_to_cart(request, slug):
    item = get_object_or_404(Item,slug=slug)
    
    if item.stock < 1:  #if there is not stock then cancel add to cart
        messages.info(request,"There is not stock of this product.")
        return redirect("core:product", slug =slug)
    
    item.stock -= 1 # decrement stock
    item.save() # save changes
    
    #check for an open order
    order_qs = Order.objects.filter(user=request.user, ordered = False)
    
    if not order_qs.exists():
        # if order does not exist then create new order
        #ordered_date = timezone.now()
        #order = Order.objects.create(user=request.user,ordered_date= ordered_date)
        #start_date = timezone.now()
        #order = Order.objects.create(user=request.user,start_date=start_date)
        order = Order.objects.create(user=request.user)
        order.order_number = create_ref_code()   # get new order number     
        order.save()
    else:
        # if an open order exist (ordered = True), then use this order 
        order = order_qs[0]
        
    
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False,
        order = order
        )
     
        
    # check if the order item is in the order
    if not created:
    #if order.items.filter(item__slug=item.slug).exists():            
        order_item.quantity += 1
        order_item.save()
        messages.info(request,"This item quantity was updated.")
        return redirect("core:order-summary")
    else:
        messages.info(request,"This item was added to your cart.")
        #order.items.add(order_item)
        order.save()
        return redirect("core:order-summary") 
          
    
    return redirect("core:order-summary")

@login_required
def remove_from_cart(request,slug):
    item = get_object_or_404(Item,slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered = False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        
        #for i in order.items.all():
        #    print(i.item.title)
        
        #if order.items.filter(item__slug=item.slug).exists(): 
        if OrderItem.objects.filter(order = order).exists():    
       
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                order=order,
                ordered=False
            )[0]
            
            item.stock += order_item.quantity # get back to stock
            item.save()
                            
            #order.items.remove(order_item)
            order_item.delete()
            messages.info(request,"This item was remove from your cart.")
            return redirect("core:order-summary")
           
        else:
             # add a message saying the user doesnt have an order
            messages.info(request,"This item was not in your cart.")
            return redirect("core:product", slug =slug)
             
    else:
        # add a message saying the user doesnt have an order
        messages.info(request,"You do not have an active order.")
        return redirect("core:product", slug =slug)          
    
    return redirect("core:product", slug =slug)

@login_required
def remove_single_item_from_cart(request,slug):
    item = get_object_or_404(Item,slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered = False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        
        #for i in order.items.all():
        #    print(i.item.title)
        
        #if order.items.filter(item__slug=item.slug).exists():
        if OrderItem.objects.filter(order = order).exists():  
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            
            item.stock += 1 # add to inventary
            item.save()
            
            if order_item.quantity > 1:      
                order_item.quantity -= 1
                order_item.save()
            else:
                #order.items.remove(order_item)
                order_item.delete()
            
            messages.info(request,"This item quantity was updated.")
            return redirect("core:order-summary")
        else:
             # add a message saying the user doesnt have an order
            messages.info(request,"This item was not in your cart.")
            return redirect("core:product", slug =slug)
             
    else:
        # add a message saying the user doesnt have an order
        messages.info(request,"You do not have an active order.")
        return redirect("core:product", slug =slug)          
    
    return redirect("core:product", slug =slug)


#--------------------------------------------------------------------------------
#   Stripe views
#--------------------------------------------------------------------------------       
"""   
class PaymentView(View):
    def get(self, *args, **kwargs):
        return render(self.request, "payment.html")
    
    def post(self,*args,**kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        token = self.request.POST.get('stripeToken')
        amount = order.get_total()#cents
        
        try:
            charge = stripe.Charge.create(
                amount= amount, 
                currency="mxn",
                source=token, # obtained with Stripe.js
                description = "Charge for fulanito@example.com",
                automatic_payment_methods={"enabled": True},
            )
            #create the payment
            payment = Payment()
            payment.stripe_charge_id = charge['id']
            payment.user = self.request.user
            payment.amount = amount
            payment.save()
            
            #assign the payment to the order
            order.ordered = True
            order.payment = payment
            order.save()
            
            messages.success(self.request, "Your order was successful!")
            return redirect("/")
            
        except stripe.error.CardError as e:
                body = e.json_body
                err = body.get('error', {})
                messages.warning(self.request, f"{err.get('message')}")
                return redirect("/")

        except stripe.error.RateLimitError as e:
                # Too many requests made to the API too quickly
                messages.warning(self.request, "Rate limit error")
                return redirect("/")

        except stripe.error.InvalidRequestError as e:
                # Invalid parameters were supplied to Stripe's API
                print(e)
                messages.warning(self.request, "Invalid parameters")
                return redirect("/")

        except stripe.error.AuthenticationError as e:
                # Authentication with Stripe's API failed
                # (maybe you changed API keys recently)
                messages.warning(self.request, "Not authenticated")
                return redirect("/")

        except stripe.error.APIConnectionError as e:
                # Network communication with Stripe failed
                messages.warning(self.request, "Network error")
                return redirect("/")

        except stripe.error.StripeError as e:
                # Display a very generic error to the user, and maybe send
                # yourself an email
                messages.warning(
                    self.request, "Something went wrong. You were not charged. Please try again.")
                return redirect("/")

        except Exception as e:
                # send an email to ourselves
                messages.warning(
                    self.request, "A serious error occurred. We have been notifed.")
                return redirect("/")
"""

class StripeIntentView(View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user,ordered = False)
            order_items = OrderItem.objects.filter(order = order)
            context = {           
                'order': order,
                'order_items': order_items
            }   
            return render(self.request, "payment.html",context)
        except:
            messages.info(self.request,"Your order has been already placed.")
            return redirect("core:home")
    
    def post(self, *args, **kwargs):         
        try:
            #print(Order)
            order = Order.objects.get(user=self.request.user, ordered=False)          
            amount = int(order.get_total()*100)#cents            
            #print (amount)
            
            # Create a PaymentIntent with the order amount and currency
            intent = stripe.PaymentIntent.create(
                amount=amount,
                currency='mxn',
                automatic_payment_methods={
                    'enabled': True,
                },
                # TODO  add order number
                metadata={
                    "user": order.user,
                    "order_number": order.order_number 
                    },
            )            
            
            payment = Payment.objects.get(order_number=order.order_number) 
            payment.stripe_payment_id = intent['id']
            payment.save()
            
            #print(intent['id'])
            #print("/n")
            
            return JsonResponse({
                'clientSecret': intent['client_secret']
            })
            
        except Exception as e:
            print(e)
            return JsonResponse( {'error': str(e)})       
        
        
class StripeSuccessView(View):
    def get(self, *args, **kwargs):
        
        try:
            order = Order.objects.get(user=self.request.user,ordered = False)        
        
            context = {           
                'order': order,            
            }
            # set order to ordered
            order.ordered = True
            order.save() 
            
            order_items = OrderItem.objects.filter(order = order)
        
            Send_mail_to_client(order,'S',order_items)
            Send_mail_to_seller(order,'S',order_items) 
                      
            return render(self.request, "payment_success.html",context)
        except:
            messages.info(self.request,"Your order has been already placed.")
            return redirect("core:home")
       
@csrf_exempt
def Stripe_webhook(request):
    event = None
    #print(request)
    payload = request.body

    try:
        event = json.loads(payload)
    except:
        print('⚠️  Webhook error while parsing basic request.' + str(e))
        #return jsonify(success=False)
        #return JsonResponse(succes=False)
        return HttpResponse(status = 400)
    if endpoint_secret:
        # Only verify the event if there is an endpoint secret defined
        # Otherwise use the basic event deserialized with json
        sig_header = request.headers.get('stripe-signature')
        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, endpoint_secret
            )
        except stripe.error.SignatureVerificationError as e:
            print('⚠️  Webhook signature verification failed.' + str(e))
            #return jsonify(success=False)
            #return JsonResponse(succes=False)
            return HttpResponse(status = 400)
    
    
    
    # Handle the event
    if event and event['type'] == 'payment_intent.succeeded':
        payment_intent = event['data']['object']  # contains a stripe.PaymentIntent
        print('Payment for {} succeeded'.format(payment_intent['amount']))
        # Then define and call a method to handle the successful payment intent.
        # handle_payment_intent_succeeded(payment_intent)
        user = payment_intent['metadata']['user']  # get user from metadata
        print(user)
        
    elif event['type'] == 'payment_method.attached':
        payment_method = event['data']['object']  # contains a stripe.PaymentMethod
        # Then define and call a method to handle the successful attachment of a PaymentMethod.
        # handle_payment_method_attached(payment_method)
    elif event['type'] == 'charge.succeeded':
        payment_charge = event['data']['object'] 
        user = payment_charge['metadata']['user']  # get user from metadata
        order_number = payment_charge['metadata']['order_number']  # get user from metadata
        
        payment = Payment.objects.get(order_number=order_number) 
        stripe_charge_id = payment_charge['id']
        payment.stripe_charge_id = stripe_charge_id
        payment.status = 'F' # set payment to fulfilled
        payment.save()
        print('charge accepted')
    else:
        # Unexpected event type
        print('Unhandled event type {}'.format(event['type']))

    #return jsonify(success=True)
    #return JsonResponse(succes=False)          
    return HttpResponse(status = 200)

# https://stripe.com/docs/webhooks/quickstart
# for testing stripe webhook: stripe listen --forward-to 127.0.0.1:9000/webhooks/stripe/
        
#-------------------------------------------------------------------------------------------   
    
    
        
            
    





