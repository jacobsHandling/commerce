from django import forms

# So when we handle a model instance in a view, we typically 
# retrieve it from the database. When we’re dealing with a form we 
# typically instantiate it in the view.

# A Form instance has an is_valid() method, which runs validation routines 
# for all its fields. When this method is called, if all fields contain 
# valid data, it will:
    # return True
    # place the form’s data in its cleaned_data attribute.

class ListingForm(forms.Form):
    title = forms.CharField(max_length=64)  #Django will automatically render label="Title" based on the var name :O
    description = forms.Textarea()
    current_bid = forms.IntegerField()
    image_url = forms.URLField()