from django import forms
from django.forms import ModelForm, TextInput, EmailInput
from .models import Listing

# So when we handle a model instance in a view, we typically 
# retrieve it from the database. When we’re dealing with a form we 
# typically instantiate it in the view.

# A Form instance has an is_valid() method, which runs validation routines 
# for all its fields. When this method is called, if all fields contain 
# valid data, it will:
    # return True
    # place the form’s data in its cleaned_data attribute.

class ListingForm(ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'starting_bid', 'image_url', 'description']