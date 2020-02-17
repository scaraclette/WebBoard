from django.urls import reverse,resolve
from django.test import TestCase
from .views import home, board_topics
from .models import Board
from django.test import Client, TestCase

class HomeTests(TestCase):
    def setUp(self):
        self.board = Board.objects.create(name='Django', description='This is a board about Django.')
        url = reverse('home')
        self.response = self.client.get(url)

    def test_home_view_status_code(self):
        url = reverse('home')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_home_url_resolves_home_view(self):
        # need to put slash on resolve('/') because it matches URL name rather than path resolve('')
        view = resolve('/')
        self.assertEquals(view.func, home)

    def test_home_view_contains_link_to_topics_page(self):
        board_topics_url = reverse('board_topics', kwargs={'board_id':self.board.id})
        self.assertContains(self.response, 'href="{0}"'.format(board_topics_url))

class BoardTopicsTest(TestCase):
    # Previously struggled with not having objects saved in test database. Error due to typing function as setup instead of setUp
    def setUp(self):
        Board.objects.create(name='Django', description='This is a board about Django.')

    # Fix test
    def test_board_topics_view_success_status_code(self):
        # output of the following line: "/boards/1". Object for reverse is str
        url = reverse('board_topics', kwargs={'board_id':'1'})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        
    def test_board_topics_view_not_found_status_code(self):
        maxLimit = Board.objects.all().count() + 1
        url = reverse('board_topics', kwargs={'board_id': maxLimit})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)
    
    def test_board_topics_url_resolves_board_topics_view(self):
        view = resolve('/boards/1')
        self.assertEquals(view.func, board_topics)