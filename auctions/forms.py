from django import forms
from .models import Category

categories = [(c.id, c.category) for c in Category.objects.all()]

class CreateListing(forms.Form):
    title = forms.CharField(label='Title',
                            max_length=64)
    description = forms.CharField(label='Description',
                                  widget=forms.Textarea())
    startingBid = forms.DecimalField(label='Starting bid',
                                    decimal_places=2,
                                    widget=forms.NumberInput(attrs={'step' : '.05'}))
    image = forms.CharField(label='Image Url',
                            required=False)
    category = forms.ChoiceField(label="Category",
                                 choices=categories,
                                 widget=forms.RadioSelect)
    
class Feedback(forms.Form):
    feedback = forms.CharField(max_length=200,
                               widget=forms.Textarea, 
                               label=False)
    
class BidForm(forms.Form):
    bid = forms.DecimalField(label='Bid',
                             decimal_places=2,
                             widget=forms.NumberInput(attrs={'step' : '.05'}))