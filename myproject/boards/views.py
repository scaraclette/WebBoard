from django.http import HttpResponse
from django.shortcuts import render
from .models import Board

# Create your views here.
def home(request):
    boards = Board.objects.all()
    context = {
        'boards':boards
    }
    return render(request, 'home.html', context)
