from django.shortcuts import get_object_or_404, render
from item.models import item
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required()
def index(request):
    items = item.objects.filter(created_by=request.user)

    return render(request,'dashboard/index.html',{
        'items':items,
    })
