from django import forms
from .models import Profile
from .models import Post, Like, Comment

class ProfileForm(forms.ModelForm):
    date_of_birth = forms.DateField(widget=forms.DateInput(format = '%d-%m-%Y'), input_formats=('%d/%m/%Y', '%d-%m-%Y'), required=False)
    hobbies = forms.CharField(widget=forms.Textarea, required=False)
    education = forms.CharField(widget=forms.Textarea, required=False)

    class Meta:
        model = Profile
        fields = ('name', 'date_of_birth', 'hobbies', 'education', 'image')
        exclude = ('user', 'image_url','url',)

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'text', 'image')
        exclude = ('image_url', )

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('author', 'text',)
