from django.shortcuts import get_object_or_404, redirect, render
from item.models import item
from .models import Conversation
from .forms import ConversationMessageForm
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def new_conversation(request,item_pk):
    Item = get_object_or_404(item,pk=item_pk)

    if Item.created_by == request.user:
        return redirect('dashboard:index')
    
    conversations = Conversation.objects.filter(item=Item).filter(members__in=[request.user.id])

    if(conversations):
        #redirect to convesation
        return redirect('conversation:detail',pk=conversations.first().id)

    if request.method == 'POST':
        form = ConversationMessageForm(request.POST)

        if form.is_valid():
            #create conversation object
            conversation = Conversation.objects.create(item=Item)
            conversation.members.add(request.user) 
            conversation.members.add(Item.created_by)
            conversation.save()

            conversation_message = form.save(commit=False)
            conversation_message.conversation = conversation #set reference
            conversation_message.created_by = request.user
            conversation_message.save()

            return redirect('item:detail',pk=item_pk)
    else:
        #create empty form
        form = ConversationMessageForm()
            

    return render(request,'conversation/new.html',{
        'form':form,
    })

@login_required
def inbox(request):
    conversations = Conversation.objects.filter(members__in=[request.user.id])

    return render(request,'conversation/inbox.html',{
        'conversations':conversations,
    })

@login_required
def detail(request,pk):
    conversation = Conversation.objects.filter(members__in=[request.user.id]).get(pk=pk)  #fetch conversation

    if request.method=='POST':
        form=ConversationMessageForm(request.POST)

        if form.is_valid():
            conversation_message = form.save(commit=False)
            conversation_message.conversation = conversation
            conversation_message.created_by = request.user
            conversation_message.save()

            return redirect('conversation:detail',pk=pk)
    
    else:
        form = ConversationMessageForm()

    return render(request,'conversation/detail.html',{
        'conversation':conversation,
        'form':form,
    })


