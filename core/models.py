from django.db import models
from django.conf import settings
from django.shortcuts import reverse
from autoslug import AutoSlugField
import os.path
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile

#from django_q.models import Schedule


#Schedule.objects.create(
#    func='core.tasks.test_task',
#    minutes=1,  # run every 5 minutes
#    repeats=-1  # keep repeating, repeat forever
#)

# Create your models here.

CATEGORY_CHOICES = (
    ('HM','Hornos'),
    ('O','otros')
)

LABEL_CHOICES = (
    ('P','primary'),
    ('S','secondary'),
    ('T','third')
)

PAYMENT_CHOICES = (
    ('C','cash'),
    ('S','stripe')    
)

PAYMENT_STATUS = (
    ('F','fulfilled'),
    ('P','pending')    
)

DELIVERY_CHOICES = (
    ('P','pickup'),
    ('S','shipping')    
)

class Category(models.Model):
    title = models.CharField(max_length=100,default='Otros')
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'



class Item(models.Model):
    title = models.CharField(max_length=100)
    price = models.FloatField()
    discount_price = models.FloatField(blank=True,null=True)
    shipping_cost = models.FloatField(default=0)
    #category = models.CharField(choices=CATEGORY_CHOICES,max_length=2,default='O')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default= None)
    label = models.CharField(choices=LABEL_CHOICES,max_length=1,default='P')
    #slug = models.SlugField(default = 'test-product')
    slug = AutoSlugField(populate_from='title',unique=True)
    description = models.TextField(default = 'test description')
    stock = models.IntegerField(default=1)
    id_item = models.CharField(max_length=20,default='0')
    image = models.ImageField(upload_to='work_image', verbose_name=('imagen'),null=True)
    thumbnail = models.ImageField(editable=False, upload_to='work_thumbnail',null=True)
    image2 = models.ImageField(upload_to='work_image', verbose_name=('imagen2'),null=True,blank=True)
    image3 = models.ImageField(upload_to='work_image', verbose_name=('imagen3'),null=True,blank=True)
    
     # Class string added to store original name of photo
    original_image_name = None 
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("core:product", kwargs={"slug": self.slug})
    
    def get_add_to_cart_url(self):
        return reverse("core:add-to-cart", kwargs={"slug": self.slug})
    
    def get_remove_from_cart_url(self):
        return reverse("core:remove-from-cart", kwargs={"slug": self.slug})
    
      # When the form is initialized save the original photo name
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.original_photo_name = self.title
    
        
    def save(self, *args, **kwargs):
        # This checks if the photo was updated or not before saving a thumbnail
        if self.original_image_name != self.title: 
            if not self.make_thumbnail():
                # set to a default thumbnail
                raise Exception('Could not create thumbnail - is the file type valid?')

        super(Item, self).save(*args, **kwargs)
    
    def make_thumbnail(self):

        image = Image.open(self.image)
        image.thumbnail(settings.THUMB_SIZE, Image.ANTIALIAS)

        thumb_name, thumb_extension = os.path.splitext(self.image.name)
        thumb_extension = thumb_extension.lower()

        thumb_filename = thumb_name + '_thumb' + thumb_extension

        if thumb_extension in ['.jpg', '.jpeg']:
            FTYPE = 'JPEG'
        elif thumb_extension == '.gif':
            FTYPE = 'GIF'
        elif thumb_extension == '.png':
            FTYPE = 'PNG'
        elif thumb_extension == '.webp':
            FTYPE = 'WEBP'
        else:
            return False    # Unrecognized file type

        # Save thumbnail to in-memory file as StringIO
        temp_thumb = BytesIO()
        image.save(temp_thumb, FTYPE)
        temp_thumb.seek(0)

        # set save=False, otherwise it will run in an infinite loop
        self.thumbnail.save(thumb_filename, ContentFile(temp_thumb.read()), save=False)
        temp_thumb.close()

        return True
    
        
class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,default=1)
    #order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, related_name='items') 
    order = models.ForeignKey('Order', on_delete=models.CASCADE, null=True, blank=True)
    ordered = models.BooleanField(default=False) 
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return  self.order.__str__() + ": " + f"{self.quantity} of {self.item.title}"
    
    def get_total_item_price(self):
        return self.quantity * self.item.price
    
    def get_total_discount_item_price(self):
        return self.quantity * self.item.discount_price
    
    def get_total_shipping_cost(self):
        print(self.quantity * self.item.shipping_cost)
        return self.quantity * self.item.shipping_cost
    
    def get_amount_saved(self):
        return self.quantity * self.item.price - self.quantity * self.item.discount_price
    
    def get_final_price(self):
        if self.item.discount_price:
            return self.get_total_discount_item_price() + self.get_total_shipping_cost()
        return self.get_total_item_price()  + self.get_total_shipping_cost()          

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    order_number = models.CharField(max_length=20,blank=True,default="")    
    #items = models.ManyToManyField(OrderItem, related_name='ordered_items')    
    start_date = models.DateTimeField(auto_now_add=True)
    #start_date = models.DateTimeField()
    ordered_date = models.DateTimeField(null=True)
    ordered = models.BooleanField(default=False)
    
    #delivery_option = models.CharField(max_length=20,blank=True, null= True)
    
    delivery_option  = models.CharField(choices=DELIVERY_CHOICES,max_length=1,blank=True, null=True)
    
    ShippingAddress = models.ForeignKey(
        'ShippingAddress', on_delete=models.SET_NULL, blank=True, null= True)
    payment = models.ForeignKey(
        'Payment', on_delete=models.SET_NULL, blank=True, null= True)
    
    reminder = models.BooleanField(default=False)
    
    complete = models.BooleanField(default=False)
    
    def __str__(self):
        #return self.user.username + " " + self.order_number.__str__()
        if self.ordered == False:
            return  self.order_number.__str__() + "/OnCart "           
        else:
            if self.complete == False:
                return  (self.order_number.__str__() + "/Ordered" + "/" 
                        + self.get_delivery_option_display() + "/" 
                        + self.payment.get_status_display()
                )
            else:
                return  (self.order_number.__str__() + "/Ordered" + "/" 
                        + self.get_delivery_option_display() + "/" 
                        + self.payment.get_status_display() + "/complete"
                )
                
    def get_total(self):
        order_items = OrderItem.objects.filter(order = self)
        total = 0
        
        for order_item in order_items:
            total += order_item.get_final_price()
        #for order_item in self.items.all():
        #    total += order_item.get_final_price()
        return total


    
class ShippingAddress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    order_number = models.CharField(max_length=20,blank=True,null=True)
    
    name = models.CharField(max_length = 100, default="")
    email = models.CharField(max_length=50)
    mobile_phone = models.CharField(max_length=10)
    delivery_option = models.CharField(max_length=20, default="")
    # if delivery_option = 'S' : 'envio a domicilio'
    street_address = models.CharField(max_length = 100)
    apartment_address = models.CharField(max_length = 100)   
    state = models.CharField(max_length=20)
    municipality = models.CharField(max_length=20)
    zip = models.CharField(max_length=5)
    
    def __str__(self):
        return self.user.username 
    
    
class Payment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, blank=True, null=True)
    
    order_number = models.CharField(max_length=20,blank=True,null=True) 
    
    payment_type = models.CharField(choices=PAYMENT_CHOICES,max_length=1,blank=True, null=True)
    
    amount = models.FloatField()
    
    status = models.CharField(choices=PAYMENT_STATUS,max_length=1,default='P')
    
    timestamp = models.DateTimeField(auto_now_add=True)
    
    stripe_payment_id = models.CharField(max_length=50,blank=True,null=True)
    stripe_charge_id = models.CharField(max_length=50,blank=True,null=True)
    
          
    def __str__(self):
        return self.order_number.__str__() + "/" + self.get_payment_type_display() + "/" + self.get_status_display()
        
    

    
    
       
    
            
            
        
        


