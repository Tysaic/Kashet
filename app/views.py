from django.shortcuts import render, redirect

# Create your views here.

def root_redirect(request):
    return redirect('app:index')  # Redirect to URL named 'index' in app namespace

def index (request):
    return render(request, 'index.html')