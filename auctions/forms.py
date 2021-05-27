from django import forms
from django.db.models.base import Model
from django.forms import ModelForm, TextInput, EmailInput
from .models import Listing, Bid, ListingComment

class ListingForm(ModelForm):

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
    amount = forms.IntegerField(widget=forms.NumberInput(attrs={
        'class': 'form-control',
        'placeholder': 'Bid Amount'
    }), label='')
    
    class Meta:
        model = Bid
        fields = ['amount']

class PartialCommentForm(ModelForm):
    class Meta:
        model = ListingComment
        widgets = {
            'comment': forms.Textarea(
                attrs={
                    'class': 'form-control'
                }
            )
        }
        fields = ['comment']