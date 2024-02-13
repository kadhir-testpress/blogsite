from django import forms
from .models import Comment

class EmailPostForm(forms.Form):
    #Form to share post
    name = forms.CharField(max_length=40)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False,
                                widget=forms.Textarea)
    
class CommentForm(forms.ModelForm):
    #Comment model form 
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')
