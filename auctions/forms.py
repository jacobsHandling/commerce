from django import forms
from django.db.models.base import Model
from django.forms import ModelForm, TextInput, EmailInput
from .models import Listing, Bid, ListingComment

# So when we handle a model instance in a view, we typically 
# retrieve it from the database. When we’re dealing with a form we 
# typically instantiate it in the view.

# A Form instance has an is_valid() method, which runs validation routines 
# for all its fields. When this method is called, if all fields contain 
# valid data, it will:
    # return True
    # place the form’s data in its cleaned_data attribute.

class ListingForm(ModelForm):

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['categories'].widget.attrs.update({'name': 'Categories (hold "command" on mac to select multiple)'})

    class Meta:
        model = Listing
        widgets = {
            'title': forms.TextInput(
                attrs={
                    'class': 'form-control'
                    }
                ),
            'categories': forms.SelectMultiple(
                attrs={
                    'class': 'form-control'
                    }
                ),
            'starting_price': forms.NumberInput(
                attrs={
                    'class': 'form-control'
                    }
                ),
            'image_url': forms.URLInput(
                attrs={
                    'class': 'form-control'
                    }
                ),
            'description': forms.Textarea(
                attrs={
                    'class': 'form-control'
                    }
                ),
            }


        fields = ['title', 'categories','starting_price', 'image_url', 'description']

class PartialBidForm(ModelForm):
    class Meta:
        model = Bid
        fields = ['amount']

class PartialCommentForm(ModelForm):
    class Meta:
        model = ListingComment
        fields = ['comment']