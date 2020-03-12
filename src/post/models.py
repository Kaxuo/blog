from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from tinymce import HTMLField

# the line below fits the index page, where there are description and then description andthen a picture on the right or left
User = get_user_model()

class PostView(models.Model):
    # we're going to keep track of the user( if he viewed a specific post)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
     # Post needs to be in quote because he's referenced below !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    post = models.ForeignKey('Post', on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class Author(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    profile_picture = models.ImageField()

    def __str__(self):
        return self.user.username

class Category(models.Model):
    title = models.CharField(max_length=20)
    def __str__(self):
        return self.title

class Comment(models.Model):
    # we put one to one keyfield first but it didn't work so we changed to foreignkey
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    #  which post the comment was actually on 
    post = models.ForeignKey('Post', related_name='comments', on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Post(models.Model):
    title = models.CharField(max_length=100)
    overview = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    # comment_count = models.IntegerField(default = 0)
    # view_count = models.IntegerField(default = 0)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    thumbnail = models.ImageField()
    content = HTMLField()
    # manyu to manyu categories : we can select many different categories
    categories = models.ManyToManyField(Category)
    # if it's true, they will be rendered on the index page
    featured = models.BooleanField()
    # when we create the post we can specify thje next one and the previous one
    previous_post = models.ForeignKey('self', related_name='previous', on_delete=models.SET_NULL, blank=True,null = True )
    next_post = models.ForeignKey('self', related_name='next', on_delete=models.SET_NULL, blank=True,null = True )

    def __str__(self):
        return self.title

# manage to get the id when you click on it 
    def get_absolute_url(self):
    # pass view name, in blog url
        return reverse('post-detail', kwargs= {
            'id': self.id 
        })
    def get_update_url(self):
    # pass view name, in blog url
        return reverse('post-update', kwargs= {
            'id': self.id 
        })

    def get_delete_url(self):
    # pass view name, in blog url
        return reverse('post-delete', kwargs= {
            'id': self.id 
        })
        
 # will get all the ocmmment related to that post 
    @property
    def get_comments(self):
        return self.comments.all().order_by('-timestamp')

    @property
    def comment_count(self):
        # grab all post view model and filter them with post = self.post. Return a count of all the posts that are equal to this specific and how many views we have for this post
        return Comment.objects.filter(post=self).count()

    @property
    def view_count(self):
        # grab all post view model and filter them with post = self.post. Return a count of all the posts that are equal to this specific and how many views we have for this post
        return PostView.objects.filter(post=self).count()


