from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.db.models import Q
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from channels.db import database_sync_to_async
from django.contrib import messages
from .models import Post, Category, Message, User, PrivateMessage
from .forms import PostForm, CustomUserCreationForm, CustomUserUpdateForm
from django.views.decorators.http import require_POST
# Create your views here.


def register_view(request):
    form = CustomUserCreationForm()
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = user.email.lower()
            user.save()
            login(request, user, backend='blogApp.backends.EmailBackend')
            return redirect('home')
        messages.error(request, 'An error occured during registration')
    return render(request, 'blogApp/login_register.html', {'form':form})


def login_view(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user, backend='blogApp.backends.EmailBackend')
            return redirect('home')
        else:
            messages.error(request, 'Invalid email or password')

    context = {'page': page}
    return render(request, 'blogApp/login_register.html', context)


def logout_view(request):
    logout(request)
    return redirect('home')




def home_view(request):
    q = request.GET.get('q', '')

    posts = Post.objects.filter(Q(category__name__icontains=q) | Q(title__icontains=q) | Q(description__icontains=q))

    post_messages = Message.objects.filter(Q(post__category__name__icontains=q))
    categories = Category.objects.all()[0:6]
    post_count = posts.count()

    context = {'posts':posts, 'categories':categories, 'post_count':post_count, 'post_messages':post_messages}
    return render(request, 'blogApp/home.html', context)


def post_view(request, pk):
    post = Post.objects.get(id=pk)
    post_messages = post.message_set.all()
    participants = post.participants.all()
    if request.method == 'POST':
        message = Message.objects.create(
            user = request.user,
            post = post,
            body = request.POST.get('body'),
        )
        post.participants.add(request.user)
        return redirect('post', pk=post.id)

    context = {'post':post, 'post_messages':post_messages, 'participants':participants}
    return render(request, 'blogApp/post.html', context)


def profile_view(request, pk):
    user = User.objects.get(id=pk)
    posts = user.post_set.all()
    post_messages = user.message_set.all()
    categories =  Category.objects.all()
    context = {'user':user, 'posts':posts, 'post_messages':post_messages, 'categories':categories}
    return render(request, 'blogApp/profile.html', context)


@login_required(login_url='login')
def create_post_view(request):
    form = PostForm()
    categories = Category.objects.all()
    if request.method == 'POST':
        category_name = request.POST.get('category')
        category, created = Category.objects.get_or_create(name=category_name)
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.created_by = request.user
            post.category = category
            post.save()
            return redirect('home')
        
    context = {'form':form, 'categories':categories}
    return render(request, 'blogApp/post_form.html', context)


@login_required(login_url='login')
def update_post_view(request, pk):
    post = Post.objects.get(id=pk)
    form = PostForm(instance=post)
    categories = Category.objects.all()

    if request.user != post.created_by:
        return HttpResponse('You are not allowed')
    if request.method == 'POST':
        category_name = request.POST.get('category')
        category, created = Category.objects.get_or_create(name=category_name)
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.category = category
            post.save()
            return redirect('home')
    context = {'form':form, 'categories':categories}
    return render(request, 'blogApp/post_form.html', context)


@login_required(login_url='login')
def delete_post_view(request, pk):
    post = Post.objects.get(id=pk)
    if request.user != post.created_by:
        return HttpResponse('You are not allowed')
    if request.method == 'POST':
        post.delete()
        return redirect('home')
    return render(request, 'blogApp/delete.html', {'obj':post})


@login_required(login_url='login')
def update_message_view(request, pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse('You are not allowed')

    post = message.post  
    post_messages = post.message_set.all()  
    participants = post.participants.all()  

    if request.method == 'POST':
        message.body = request.POST.get('body')
        message.save()
        return redirect('post', pk=post.id)

    
    context = {
        'post': post,
        'post_messages': post_messages,
        'participants': participants,
        'edit_message_body': message.body  
    }
    return render(request, 'blogApp/post.html', context)


@login_required(login_url='login')
def delete_message_view(request, pk):
    message = Message.objects.get(id=pk)
    if request.user != message.user:
        return HttpResponse('You are not allowed')
    if request.method == 'POST':
        message.delete()
        return redirect('home')
    return render(request, 'blogApp/delete.html', {'obj':message})


@login_required(login_url='login')
def update_user_view(request):
    user = request.user
    form = CustomUserUpdateForm(instance=user)

    if request.method == 'POST':
        form = CustomUserUpdateForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile', pk=user.id)

    context = {'form':form}
    return render(request, 'blogApp/update_user.html', context)


def category_page_view(request):
    q = request.GET.get('q', '')
    categories = Category.objects.filter(name__icontains=q)
    return render(request, 'blogApp/categories.html', {'categories':categories})


def activity_page_view(request):
    post_messages = Message.objects.all()
    return render(request, 'blogApp/activity_page.html', {'post_messages':post_messages})


@login_required(login_url='login')
def upvote_post_view(request, pk):
    post = Post.objects.get(id=pk)
    
    # If user already downvoted, remove downvote
    if request.user in post.downvotes.all():
        post.downvotes.remove(request.user)
    
    # Toggle upvote
    if request.user in post.upvotes.all():
        post.upvotes.remove(request.user)
    else:
        post.upvotes.add(request.user)
    
    return redirect('post', pk=post.id)


@login_required(login_url='login')
def downvote_post_view(request, pk):
    post = Post.objects.get(id=pk)
    
    # If user already upvoted, remove upvote
    if request.user in post.upvotes.all():
        post.upvotes.remove(request.user)
    
    # Toggle downvote
    if request.user in post.downvotes.all():
        post.downvotes.remove(request.user)
    else:
        post.downvotes.add(request.user)
    
    return redirect('post', pk=post.id)


@login_required(login_url='login')
@database_sync_to_async
def private_messages_view(request, username):
    other = get_object_or_404(User, username=username)
    if request.user == other:
        # show user's inbox
        chat_messages = []
        return render(request, 'blogApp/private_chat.html', {'other': other, 'chat_messages': chat_messages})

    # load messages between request.user and other
    chat_messages = PrivateMessage.objects.filter(
        (Q(sender=request.user) & Q(recipient=other)) |
        (Q(sender=other) & Q(recipient=request.user))
    ).order_by('created')

    return render(request, 'blogApp/private_chat.html', {'other': other, 'chat_messages': chat_messages})


@login_required(login_url='login')
@require_POST
@database_sync_to_async
def send_private_message_view(request, username):
    other = get_object_or_404(User, username=username)
    body = request.POST.get('body', '').strip()
    if body:
        pm = PrivateMessage.objects.create(sender=request.user, recipient=other, body=body)
        # If AJAX, return JSON
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'ok': True, 'id': pm.id, 'body': pm.body, 'sender': pm.sender.username, 'created': pm.created.isoformat()})
    return redirect('private-messages', username=other.username)

