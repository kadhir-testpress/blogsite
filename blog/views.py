from django.shortcuts import render, get_object_or_404 
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count
from django.contrib.postgres.search import SearchVector
from .models import Post
from .forms import EmailPostForm, CommentForm, SearchForm

from taggit.models import Tag

def post_list(request, tag_slug=None):
    object_list = Post.published.all()
    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])

    paginator = Paginator(object_list, 3) # 3 posts in each page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    return render(request,
                 'blog/post/list.html',
                 {'page': page,
                  'posts': posts,
                  'tag': tag})

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
            
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags','-publish')[:4]
    return render(request,
                'blog/post/detail.html',
                {
                    'post':post,
                    'comments':comments,
                    'new_comment':new_comment,
                    'comment_form':comment_form,
                    'similar_posts':similar_posts,
                })

def post_search(request):
    form = SearchForm()
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = Post.published.annotate(
                search=SearchVector('title','body'),
            ).filter(search=query)
    return render(request,'blog/post/search.html',{
        'form':form,
        'query':query,
        'results':results
    })


