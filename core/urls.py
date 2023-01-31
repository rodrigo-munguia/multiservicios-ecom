from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .views import (
        HomeView,
        ItemDetailView,
        CheckoutView,
        add_to_cart,
        remove_from_cart,
        remove_single_item_from_cart,
        OrderSummaryView,
        StripeIntentView,
        StripeSuccessView,
        Stripe_webhook,
        Order_pick_up_success_View,
        HomeCategorySearchView,
        HomeSearchView
        #PaymentView
    ) 

app_name = 'core'

urlpatterns = [
    path('',HomeView.as_view(),name='home'),
    path('categories/<int:pk>', HomeCategorySearchView.as_view(), name='category_search'),
    path('search/', HomeSearchView.as_view(), name='home_search'),
    path('checkout/',CheckoutView.as_view(),name = 'checkout'),
    path('product/<slug>',ItemDetailView.as_view(),name = 'product'),
    path('add-to-cart/<slug>', add_to_cart, name = 'add-to-cart'),
    path('remove-from-cart/<slug>', remove_from_cart, name = 'remove-from-cart'),
    path('remove-single-item-from-cart/<slug>', remove_single_item_from_cart, name = 'remove-single-item-from-cart'),
    path('order-summary/', OrderSummaryView.as_view(), name= 'order-summary'),
    #path('payment/<payment_option>/',PaymentView.as_view(), name = 'payment' ),
    path('create-payment-intent/',StripeIntentView.as_view(), name = 'create-payment-intent' ),
    path('create-payment-success/',StripeSuccessView.as_view(), name = 'create-payment-success'),
    path('webhooks/stripe/',Stripe_webhook,name = 'Stripe-webhook'  ),
    path('Order_pick_up_success_View',Order_pick_up_success_View.as_view(), name = 'Order-pick-up-success-View')
    
] 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
