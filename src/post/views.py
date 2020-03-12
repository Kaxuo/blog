from django.shortcuts import render, get_object_or_404, redirect,reverse
from .models import Post, Author, PostView
from marketing.models import Signup
from .forms import CommentForm, PostForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count, Q



def get_author(user):
    qs= Author.objects.filter(user=user)
    if qs.exists():
        return qs[0]
    return None    
#search function , the q is the variable , the Q is the model
def search(request):
    queryset = Post.objects.all()
    query = request.GET.get('q')
    if query:
        queryset = queryset.filter(
            # does the queryset contains the title or does it have an overview
            Q(title__icontains=query) |
            Q(overview__icontains=query)
            # distinct : avoid getting the same post twice
        ).distinct()
    context = {
        'queryset' : queryset
    }

    return render(request, 'search_result.html', context)

# count each category 
def get_category_count():
    # return only the category field of each post , annotate : return dictioarry where each key is each category,
    # at first we put .value('categories) and got categorie + number , but then we put title (coming from models categories ) to get their name')
    queryset = Post \
        .objects \
        .values('categories__title') \
        .annotate(Count('categories__title'))
    return queryset


def index(request):
    featured = Post.objects.filter(featured=True)
    latest = Post.objects.order_by('-timestamp')[0:3]

    if request.method == "POST":
        email = request.POST['email']
        new_signup = Signup()
        new_signup.email = email
        new_signup.save()
    context = {
        'object_list': featured,
        'latest' : latest
    }
    return render(request, 'index.html', context)

def blog(request):
    category_count = get_category_count()
    print(category_count)
    # the print of category count will give us : QuerySet [{'categories': 1, 'categories__count': 2}, {'categories': 2, 'categories__count': 2}]
    #  and then  we got this with category__title : <QuerySet [{'categories__title': 'Business', 'categories__title__count': 2}, {'categories__title': 'Django', 'categories__title__count': 2}]
    blog_list = Post.objects.all()
    most_recent = Post.objects.order_by('-timestamp')[:3]
    # pass queryset into the paginator, and the number of POST we want to render
    paginator = Paginator(blog_list, 4)
    page_request_var = 'page'
    # click = ?pageX= (change page ) , the variable page is the number of page ( which one will be rendered)
    page = request.GET.get(page_request_var)
    try:
        paginated_queryset = paginator.page(page)
    # if we don't get a page, then we go on first page 
    except PageNotAnInteger:
        paginated_queryset = paginator.page(1)
    except EmptyPage:
    # if it's an empty page , the actual number of pages in the query set ( if we have 100 post, and 25 pages, then it will render 4 posts , if it's empty , we will return the twentyfifth page)
        paginated_queryset = paginator.page(paginator.num_pages)
    context = {
        'queryset' : paginated_queryset,
        'most_recent': most_recent,
        'page_request_var': page_request_var,
        'category_count': category_count

    }    
    return render(request, 'blog.html', context)

def post(request, id):
    # 2 lines below : created to allow post to render the sidebar 
    category_count = get_category_count()
    most_recent = Post.objects.order_by('-timestamp')[:3]
    post = get_object_or_404(Post, id=id)
    # if the user ios authenticated , we will actually create the view, if they're not, we won't take them as view
    if request.user.is_authenticated :
        PostView.objects.get_or_create(user = request.user, post=post)
    form = CommentForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
    # we need to pass some specific values : the post and the user to that comment 
            form.instance.user = request.user
            form.instance.post = post
            form.save()
            # redirect : after posting it , you will just get back to the page
            return redirect(reverse("post-detail", kwargs={
                'id': post.id
            }))
    context = {
        'form':form,
        'post': post,
        'category_count': category_count,
        'most_recent': most_recent,
    }
    # you need id for the get absolute url in views  , when you click on it , it will go to that id
    return render(request, 'post.html', context)


# the post_create file is used for create / update !!


def post_create(request):
    title= 'Create'
    # But to create one, we have to give it an author ! (it's required in model.post), so we created a def get user at the top ! (from class Author in model) ... Files = Files received
    form = PostForm(request.POST or None, request.FILES or None)
    author = get_author(request.user)
    if request.method == 'POST':
        if form.is_valid():
            form.instance.author=author
            form.save()
            return redirect(reverse("post-detail", kwargs ={
                # instance of the form /post that was just creatd 
                'id' : form.instance.id
            }))
    context = {
        'title': title,
        'form': form
    }
    return render(request, 'post_create.html', context)

def post_update(request, id):
    title = 'Update'
    post = get_object_or_404(Post, id=id)
    # instance = post we are editing 
    form = PostForm(request.POST or None, request.FILES or None, instance=post)
    author = get_author(request.user)
    if request.method == 'POST':
        if form.is_valid():
            form.instance.author = author
            form.save()
            # instance of the form /post that was just creatd 
            return redirect(reverse("post-detail", kwargs ={
                'id' : form.instance.id
            }))
    context = {
        'title': title,
        'form': form
    }
    return render(request, 'post_create.html', context)

def post_delete(request, id):
    post = get_object_or_404(Post , id=id)
    post.delete()
    return redirect(reverse("post-list"))