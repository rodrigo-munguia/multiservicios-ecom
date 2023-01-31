from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

#from django_countries.fields import CountryField

PAYMENT_CHOICES = (
    ('S','Stripe'),
    ('P','PayPal')
)

#DELIVERY_CHOICES = (
#  ('S','Shipping'),
#  ('P','Pick up')
#)

DELIVERY_CHOICES = (
  ('S','Envio a domicilio'),
  ('P','Recoger en sucursal')
)

class CheckoutForm(forms.Form):
  
    name = forms.CharField(      
      max_length=100,         
      widget=forms.TextInput(attrs={
          'class':'form-control',
          'placeholder': 'fulanito perez'   
      }))
    
    mobile_phone = forms.CharField(      
      max_length=10,         
      widget=forms.TextInput(attrs={
          'class':'form-control',
          'placeholder': '3312345678'   
      }))
    
    email = forms.CharField(      
      max_length=50,         
      widget=forms.TextInput(attrs={
          'class':'form-control',
          'placeholder': 'subject_123@gmail.com'   
      }))     
    
    delivery_option = forms.ChoiceField(
        widget=forms.RadioSelect, choices=DELIVERY_CHOICES
        )   
  
    # exterior address
    street_address = forms.CharField(
        max_length=120,
        widget=forms.TextInput(attrs={
          'class':'form-control',
          'placeholder': '1234 Main St'   
        }))
    # interior address
    apartment_address = forms.CharField(
        required=False,
         widget=forms.TextInput(attrs={
           'class':'form-control',
          'placeholder': 'Apartment or suite'   
        }))   
        
    state = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={
          'class':'form-control',
          'placeholder': 'Jalisco'   
        }))   
    
    municipality = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={
          'class':'form-control',
          'placeholder': 'Zapopan'   
        }))
    
    #country = CountryField(blanck_label='(selec country)').formfield(widget=COuntrySelectWidget(attrs={'class':'custom--select d-block w-100}))
    
    zip = forms.CharField(
        max_length=5,
        widget=forms.TextInput(attrs={
          'class':'form-control',
          'placeholder': '45010'   
        }))
    
    same_billing_address = forms.BooleanField(
        required=False        
        )
    
    save_info = forms.BooleanField(
        required=False
        )
    
    payment_option = forms.ChoiceField(
        required=False,
        widget=forms.RadioSelect, choices=PAYMENT_CHOICES
        )
    
    
    #def clean(self):
    #  cd = self.cleaned_data
    #  mp = cd.get('mobile_phone',None)     
    #  if not mp.isnumeric():
    #    raise forms.ValidationError("Enter a valid phone number")
    
    def clean_name(self):
      nm = self.cleaned_data['name']
      if not len(nm) > 1:
        raise form.ValidationError("You must insert a valid name")
      return nm
      
    def clean_mobile_phone(self):
      mp = self.cleaned_data['mobile_phone']
      if not mp.isnumeric() or not len(mp) == 10:
        raise forms.ValidationError("You must insert a valid 10 digits phone number.")
      return mp
    
    def clean_email(self):
      em = self.cleaned_data['email']
      try:
        validate_email(em)
      except ValidationError as e:
        raise forms.ValidationError("You must insert a valid email address.")      
      return em
    
    def clean_zip(self):
      delivery = self.cleaned_data['delivery_option']
      zp = self.cleaned_data['zip']  
      
      if delivery == 'P': # if delivery = pick up then do not validate zip
        return zp
      
      zp = self.cleaned_data['zip']      
      if not zp.isnumeric() or not len(zp) == 5:
        raise forms.ValidationError("You must insert a valid 5 digits ZIP number.")
      return zp
    
    
      
      
    
    
    
    
    
    
    
    
    
    
    
    
    
    