from django import forms
from core.helper.helper import Review



class FacilityReviewForm(forms.ModelForm):
    title = forms.CharField(label="Title of your review", widget=forms.TextInput(attrs={
        "class":"form-control",
        "placeholder":"If you could say it in one sentence, what would you say?"
        
    }))
    
    review =  forms.CharField(label="Your review", widget=forms.Textarea(attrs={
        "class":"form-control",
        "placeholder":"Write your actual review here...",
        "rows":3
        
    }))
    
    class Meta:
        model = Review
        fields = ['title', 'review']