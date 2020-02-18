from django.contrib.auth.models import User
from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404, redirect
from .models import Board, Topic, Post
from .forms import NewTopicForm

# Create your views here.
def home(request):
    boards = Board.objects.all()
    context = {
        'boards':boards
    }
    return render(request, 'home.html', context)

def board_topics(request, board_id):
    try:
        board = Board.objects.get(id=board_id)
    except Board.DoesNotExist:
        raise Http404
    
    context = {
        'board': board
    }
    return render(request, 'topics.html', context)

def new_topic(request, board_id):
    board = get_object_or_404(Board, pk=board_id)
    user = User.objects.first()  # TODO: get the currently logged in user
    if request.method == 'POST':
        form = NewTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.board = board
            topic.starter = user
            topic.save()
            post = Post.objects.create(
                message=form.cleaned_data.get('message'),
                topic=topic,
                created_by=user
            )
            return redirect('board_topics', board_id=board.pk)  # TODO: redirect to the created topic page
    else:
        form = NewTopicForm()
    return render(request, 'new_topic.html', {'board': board, 'form': form})

# def new_topic(request, board_id):
#     board = get_object_or_404(Board, pk=board_id)
#     user = User.objects.first() # TODO: get the currently logged in user
#     if request.method == 'POST':
#         form = NewTopicForm(request.POST)
#         if form.is_valid():
#             topic = form.save(commit=False)
#             topic.board = board
#             topic.starter = user
#             topic.save()
#             post = Post.objects.create(
#                 message=form.cleaned_data.get('message'),
#                 topic=topic,
#                 created_by=user
#             )
#             return redirect('board_topics', board_id=board.id) # TODO: redirect to the created topic page
#         else:
#             form = NewTopicForm()

#         context = {
#             'board':board,
#             'form':form
#         }
#         return render(request, 'new_topic.html', context)
    