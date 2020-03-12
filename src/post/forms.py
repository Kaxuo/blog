from django import forms
from tinymce import TinyMCE
from .models import Post, Comment


class TinyMCEWidget(TinyMCE):
    def use_required_attribute(self, *args):
        return False

class PostForm(forms.ModelForm):
    content = forms.CharField(
        widget = TinyMCEWidget(
            attrs ={'required': False, 'cols': 30, 'rows': 10}
        )
    )

    class Meta:
        # below,in "fields" , we're going to put what we want the user to see / create when he pushes on "create post", always a topple
        model = Post
        fields = ('title','overview','content','thumbnail','categories','featured','previous_post','next_post')

class CommentForm(forms.ModelForm):
    # you use attrs as you use class in HTLM , allow us to create the text area that has a form control class, CONTENT is the same IN CLASS META , and will be displayed
    content = forms.CharField(widget=forms.Textarea(attrs={
        "class": 'form-control',
        'placeholder': "Type your comment",
        'id': 'usercomment',
        'rows': '4'
    }))
    class Meta:
        model = Comment
        # because in models, it will only include de content  ( not user, timestap or post , in the comment class), IT HAS TO BE A TOPPLE
        fields = ('content',)