from django.shortcuts import render,redirect
from item.models import Category,item
from .forms import SignupForm
from django.contrib.auth.models import auth
# Create your views here.
def index(request):
    # request :- info about- browser, ip address,get post request
    items = item.objects.filter(is_sold = False)[0:6]
    categories = Category.objects.all()

    return render(request,'core/index.html',{
        'items':items,
        'categories':categories
    })
    #we pass request so that it can be available in the template
def contact(request):
    return render(request,'core/contact.html')

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('/login/')
    else: 
        form = SignupForm()

    return render(request,'core/signup.html',{
        'form':form
    })

def logout(request):
    auth.logout(request)
    return redirect('/login/')