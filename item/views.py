from django.shortcuts import get_object_or_404, render,redirect
from django.db.models import Q
from .models import item,Category
from django.contrib.auth.decorators import login_required
from .forms import NewItemForm,EditItemForm
# Create your views here.

def items(request):
    query = request.GET.get('query','')  #(name,default)
    category_id = request.GET.get('category',0) # category_id is provided by default by django
    categories = Category.objects.all()
    items = item.objects.filter(is_sold=False)

    if category_id:
        items = items.filter(category_id=category_id)

    if query:
        items = items.filter(Q(name__icontains=query) | Q(description__icontains=query))

    return render(request,'item/items.html',{
        'items':items,
        'query':query,
        'categories':categories,
        'category_id':int(category_id)
    })

def detail(request,pk):
    i = get_object_or_404(item,pk=pk)
    related_items = item.objects.filter(category=i.category,is_sold=False).exclude(pk=pk)[0:3]
    return render(request,'item/detail.html',{
        'item':i,
        'related_items':related_items
    })

@login_required
def new(request):
    if request.method=='POST':
        form = NewItemForm(request.POST,request.FILES)

        if form.is_valid():
            new_item = form.save(commit=False)
            new_item.created_by = request.user
            new_item.save()

            return redirect('item:detail',pk=new_item.id)

    else:
        form = NewItemForm()

    return render(request,'item/form.html',{
        'form':form,
        'title':'New item'
    })

@login_required
def edit(request,pk):
    current_item = get_object_or_404(item,pk=pk,created_by=request.user)
    if request.method=='POST':
        form = EditItemForm(request.POST,request.FILES,instance=current_item)

        if form.is_valid():
            form.save();

            return redirect('item:detail',pk=current_item.id)

    else:
        form = EditItemForm(instance=current_item)

    return render(request,'item/form.html',{
        'form':form,
        'title':'Edit item'
    })

@login_required()
def delete(request,pk):
    current_item = get_object_or_404(item,pk=pk,created_by=request.user)

    current_item.delete()

    return redirect('dashboard:index')