from django import template
from core.models import Order,OrderItem

register = template.Library()


@register.filter
def cart_item_count(user):
    if user.is_authenticated:
        qs = Order.objects.filter(user=user, ordered=False)
        
        if qs.exists():
            #return qs[0].items.count()
            order_items = OrderItem.objects.filter(order = qs[0])
            return order_items.count()
    return 0
