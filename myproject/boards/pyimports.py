from django.urls import reverse,resolve
from django.test import TestCase
from .views import home, board_topics, new_topic
from .models import Board, Topic, Post
from django.test import Client, TestCase
from django.contrib.auth.models import User