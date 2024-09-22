from django import forms
from .models import *

class ProductFilterForm(forms.Form):
    bottle_volume = forms.ModelMultipleChoiceField(
        queryset=BottleVolume.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )
    bottle_type = forms.ModelMultipleChoiceField(
        queryset=BottleType.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )
    bottle_color = forms.ModelMultipleChoiceField(
        queryset=BottleColor.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )
    bottle_cap_type = forms.ModelMultipleChoiceField(
        queryset=BottleCapType.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )
    general_category = forms.ModelMultipleChoiceField(
        queryset=GeneralCategory.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )
    sub_category = forms.ModelMultipleChoiceField(
        queryset=SubCategory.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )


class ReviewForm(forms.ModelForm):
    SHOW_NAME_CHOICES = [
        (True, 'Evet'),
        (False, 'Hayır')
    ]
    show_name = forms.ChoiceField(choices=SHOW_NAME_CHOICES, widget=forms.RadioSelect)

    class Meta:
        model = Review
        fields = ['title', 'comment', 'show_name']

    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'placeholder': 'Ad Soyad',  'style': 'width: 100%; padding: 5px 10px;'})
        self.fields['comment'].widget.attrs.update({'placeholder': 'Yorumunuz', 'rows': "2", 'style': 'width: 100%; padding: 5px 10px;'})
        self.fields['show_name'].label = False  # Hide label for radio buttons
