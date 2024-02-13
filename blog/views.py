from django.shortcuts import render, get_object_or_404 
from .models import Post, Comment
from django.views.generic import ListView
from .forms import EmailPostForm, CommentForm

class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'

def post_detail(request, year, month, day, post):
    #fetch a single post
    post = get_object_or_404(
        Post,
        slug=post,
        status='published',
        publish__year=year,
        publish__month=month,
        publish__day=day
    )
    return render(request,'blog/post/detail.html',{'post':post})

def post_share(request, post_id):
    # Retrieve post by id 
    post = get_object_or_404(Post, id=post_id, status='published')
    form = EmailPostForm(request.POST)
    if request.method == 'POST':
        #submit the form 
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Form fields passed validation
            cd = form.cleaned_data
            # ... send email
        else:
            form = EmailPostForm() 
    return render(
        request,
        'blog/post/share.html',
        {'post':post,'form':form}
    )

def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    
    # List of active comments for this post
    comments = post.comments.filter(active=True)

    new_comment = None
    comment_form = CommentForm(data=request.POST)
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post 
            new_comment.save()
            
        else:
            comment_form = CommentForm()
        
    return render(request,
                'blog/post/detail.html',
                {
                    'post':post,
                    'comments':comments,
                    'new_comment':new_comment,
                    'comment_form':comment_form
                })



