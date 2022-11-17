from django import forms
from django.core.exceptions import ValidationError
from account.helpers.profile import ProfileReview


class ProfileReviewForm(forms.ModelForm):
    title = forms.CharField(label="Title of your review", widget=forms.TextInput(
        attrs={
            "class": "form-control",
            "placeholder":"If you could say it in one sentence, what would you say?"
        }
    ))
    review = forms.CharField(label="Your Review", widget=forms.Textarea(
        attrs={
            "class":"form-control",
            "rows":4,
        }
    ))
    class Meta:
        model = ProfileReview
        fields = ['title', 'review']
        
    def clean(self, *args, **kwargs):
        cleaned_data = super().clean(*args, **kwargs)
        title = cleaned_data.get("title")
        review = cleaned_data.get('review')
        
        if not title and review:
            raise ValidationError("Both fields {} and {} are required!".format(title, review))
        return cleaned_data
        
        