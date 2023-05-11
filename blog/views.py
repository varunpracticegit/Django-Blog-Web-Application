from django.shortcuts import render, HttpResponseRedirect, redirect
from .forms import SignUpForm, LoginForm, PostForm, CommentForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import Post, Comment
from django.contrib.auth.models import Group
from django.urls import reverse




# Home view

def home(request):
    posts = Post.objects.all()
    comments = CommentForm()
    com = Comment.objects.all()

    if request.method == 'POST':
        comments = CommentForm(request.POST)
        if comments.is_valid():
            post_id = request.POST.get('post_id')
            name = comments.cleaned_data.get('name')
            body = comments.cleaned_data.get('body')
            post = Post.objects.get(id=post_id)
            comment = Comment(name=name, body=body, post=post)
            comment.save()
            messages.success(request, 'Comment added successfully!')
        return redirect('home')

    return render(request, 'blog/home.html', {'posts': posts, 'comments': comments, 'com':com})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = Comment.objects.filter(post=post)

    return render(request, 'blog/home.html', {'post': post, 'comments': comments})




# About view
def about(request):
    return render(request, 'blog/about.html')

# Contact view
def contact(request):
    return render(request, 'blog/contact.html')

# Dashboard view
def dashboard(request):
    com = Comment.objects.all()
    if request.user.is_authenticated:
     posts = Post.objects.all()
     user = request.user
     full_name = user.get_full_name()
     gps = user.groups.all()
     return render(request, 'blog/dashboard.html', {'com':com, 'posts':posts, 'full_name':full_name, 'groups': gps})

    else:
      return HttpResponseRedirect('/login/')

# Logout view
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')

# Signup view

def user_signup(request):
    # if not request.user.is_authenticated:
      if request.method == 'POST':
          form = SignUpForm(request.POST)
          if form.is_valid():
           messages.success(request, 'Account created successfully !!')
           user = form.save()
           group = Group.objects.get(name='Author')
           user.groups.add(group)

      else:
        form = SignUpForm()
      return render(request, 'blog/signup.html', {'form':form})
    # else:
    #   return HttpResponseRedirect('/') 


# Login view
def user_login(request):
    
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = LoginForm(request = request, data = request.POST)
            if form.is_valid():
                uname = form.cleaned_data['username']
                upass = form.cleaned_data['password']
                user = authenticate(username = uname, password = upass)
                if user is not None:
                 login(request, user)
                messages.success(request, 'Logged in successfully')
                return HttpResponseRedirect('/dashboard/')
        else:
         form = LoginForm()
        return render(request, 'blog/login.html', {'form':form})
    else:
        return HttpResponseRedirect('/dashboard/')
    
#Add new Post view
def add_post(request):
   if request.user.is_authenticated:
      if request.method == 'POST':
         form = PostForm(request.POST)
         if form.is_valid():
            title = form.cleaned_data['title']
            body = form.cleaned_data['body']
            post = Post(title=title, body = body)
            post.save()
            form = PostForm()
      else:
         form = PostForm()  
      return render(request, 'blog/addpost.html', {'form':form})
   else:
      return HttpResponseRedirect('/login/')
   
 #Update Post view
def update_post(request, id):
   if request.user.is_authenticated:
      if request.method == 'POST':
         pi = Post.objects.get(pk=id)
         form = PostForm(request.POST, instance=pi)
         if form.is_valid():
          form.save()
          return HttpResponseRedirect('/dashboard/')
      else:
         pi = Post.objects.get(pk=id)
         form = PostForm(instance=pi)
      return render(request, 'blog/updatepost.html', {'form': form})
   else:
      return HttpResponseRedirect('/login/')


   
#Delete Post view
def delete_post(request, id):
   if request.user.is_authenticated:
      if request.method == 'POST':
         pi = Post.objects.get(pk=id)
         pi.delete()
         return HttpResponseRedirect('/dashboard/')
   else:
      return HttpResponseRedirect('/login/')
   

