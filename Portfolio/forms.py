from django import forms
from django.forms import inlineformset_factory
from .models import Category,Painting, ArtistModel,Milestones

class AddCategory(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['title','desc','cover']

class AddPainting(forms.ModelForm):
    class Meta:
        model = Painting
        fields = ['title','desc','image','video']

class EditAbout(forms.ModelForm):
    class Meta:
        model = ArtistModel
        fields = ['photo','bio','statement','inspirations','themes','mediums','video',]

MilestoneForm = inlineformset_factory (
    ArtistModel,
    Milestones,
    
    fields=['year','title','note'],
    extra=1,
    can_delete=True
)