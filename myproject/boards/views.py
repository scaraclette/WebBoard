from django.http import HttpResponse, Http404
from django.shortcuts import render
from .models import Board

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