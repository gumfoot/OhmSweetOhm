from django import forms
from .models import Wishlist
from .models import UserInfo, Accessories

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from.models import Pay,UserMessage,Product_images



class AddToWishlistForm(forms.ModelForm):
    class Meta:
        model = Wishlist
        fields = ['product']




class NewUserForm(UserCreationForm):
	email = forms.EmailField(required=True)

	class Meta:
		model = User
		fields = ("username", "email", "password1", "password2")

	def save(self, commit=True):
		user = super(NewUserForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		if commit:
			user.save()
		return user
	

class PayForm(forms.ModelForm):
    class Meta:
        model = Pay
        fields = ('name', 'card_number', 'hetevi_tver', 'phone_number', 'email')

# class AddressForm(forms.Form):
#     address = forms.CharField(max_length=255)
#     phone_number = forms.CharField(max_length=50)
#     email = forms.EmailField()


class UserMessageForm(forms.ModelForm):
    class Meta:
        model = UserMessage
        fields = ('name','phone', 'email', 'address', 'message')
        


class ContactForm(forms.ModelForm):
    class Meta:
        model = UserInfo
        fields = ['name', 'email', 'phone', 'address']



class ProductImageForm(forms.ModelForm):
    class Meta:
        model = Product_images
        fields = ['product', 'pictures',]


class ProductFilterForm(forms.Form):
    category = forms.CharField(required=False)



class AccessoriesImageForm(forms.ModelForm):
    class Meta:
        model = Product_images
        fields = ['product', 'pictures',]


class AccessoriesFilterForm(forms.Form):
    category = forms.CharField(required=False)


from .models import Product_detail

class ProductDetailAdminForm(forms.ModelForm):
    class Meta:
        model = Product_detail
        fields = '__all__'
        widgets = {
            'color': forms.TextInput(attrs={'type': 'color'})  # Use a color picker widget
        }    

        def save(self, commit=True):
            instance = super().save(commit=False)
            if commit:
                instance.save()
            return instance