from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import BlogPost
from django.db.models import Q

def login(request):
    blogposts = BlogPost.objects.all()
    search_query = ""
    if request.method == "POST": 
        if "create" in request.POST:
            title = request.POST.get("title")
            content = request.POST.get("content")
            BlogPost.objects.create(
                title=title,
                content=content
            )
            messages.success(request, "Your new blog added successfully")
    
        elif "update" in request.POST:
            id = request.POST.get("id")
            title = request.POST.get("title")
            content = request.POST.get("content")
            blogpost = BlogPost.objects.get(id=id)
            blogpost.title = title
            blogpost.content = content
            blogpost.save()
            messages.success(request, "Your blog updated successfully")
    
        elif "delete" in request.POST:
            id = request.POST.get("id")
            BlogPost.objects.get(id=id).delete()
            messages.success(request, "Your blog deleted successfully")
        
        elif "search" in request.POST:
            search_query = request.POST.get("query")
            blogposts = BlogPost.objects.filter(Q(title__icontains=search_query))
            # blogposts = BlogPost.objects.filter(Q(title_icontains=search_query) | Q(content_icontains=search_query))

    context = {"blogposts": blogposts, "search_query": search_query}
    return render(request, "login.html", context=context)

def index(request):
    return render(request, 'index.html')

def contact(request):
    return render(request, 'contact.html')

def blog(request):
    return render(request, 'blog.html')

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect("login")  # Replace with the page you want after login
        else:
            messages.error(request, "Invalid username or password")
            return redirect("home")

    return render(request, "header.html")

def signup_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect("home")
        
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        messages.success(request, "Account created successfully")
        return redirect("home")

    return render(request, "header.html")