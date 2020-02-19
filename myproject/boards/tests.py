from django.urls import reverse,resolve
from django.test import TestCase
from .views import home, board_topics, new_topic, board_redirect
from .models import Board, Topic, Post
from django.test import Client, TestCase
from django.contrib.auth.models import User
from .forms import NewTopicForm


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
    
    # Created own test to redirect user when they enter /boards/
    def test_home_url_board_redirect(self):
        view = resolve('/boards/')
        self.assertEquals(view.func, board_redirect)

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
        view = resolve('/boards/1/')
        self.assertEquals(view.func, board_topics)

    def test_board_topics_view_contains_navigation_links(self):
        board_topics_url = reverse('board_topics', kwargs={'board_id':1})
        homepage_url = reverse('home')
        new_topic_url = reverse('new_topic', kwargs={'board_id':1})

        response = self.client.get(board_topics_url)

        self.assertContains(response, 'href="{0}"'.format(homepage_url))
        self.assertContains(response, 'href="{0}"'.format(new_topic_url))

    

class NewTopicTests(TestCase):
    def setUp(self):
        Board.objects.create(name='Django', description='This is a board about Django.')
        User.objects.create_user(username='john', email='john@doe.com', password='123')

    # Changed 'self.client.get(new_topic_url)' to 'post'
    def test_new_topic_view_success_status_code(self):
        url = reverse('new_topic', kwargs={'board_id': 1})
        response = self.client.post(url)
        self.assertEquals(response.status_code, 200)

    def test_new_topic_view_not_found_status_code(self):
        maxLimit = Board.objects.all().count() + 1
        url = reverse('new_topic', kwargs={'board_id': maxLimit})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)

    def test_new_topic_url_resolves_new_topic_view(self):
        view = resolve('/boards/1/new/')
        self.assertEquals(view.func, new_topic)

    # Also changed 'self.client.get(new_topic_url)' to 'post'
    def test_new_topic_view_contains_link_back_to_board_topic_view(self):
        new_topic_url = reverse('new_topic', kwargs={'board_id':1})
        board_topics_url = reverse('board_topics', kwargs={'board_id':1})
        response = self.client.post(new_topic_url)
        self.assertContains(response, 'href="{0}"'.format(board_topics_url))

    def test_csrf(self):
        url = reverse('new_topic', kwargs={'board_id': 1})
        '''
        This test was fixed because 'self.client.get(url)' was changed into 'self.client.post(url)'
        which makes sense because we're testing a POST request within the view instead of GET
        '''
        response = self.client.post(url)
        print(response)
        self.assertContains(response, 'csrfmiddlewaretoken')

    def test_new_topic_valid_post_data(self):
        url = reverse('new_topic', kwargs={'board_id':1})
        data = {
            'subject': 'Test title',
            'message': 'Lorem ipsum dolor sit amet'
        }
        response = self.client.post(url, data)
        self.assertTrue(Topic.objects.exists())
        self.assertTrue(Post.objects.exists())

    def test_new_topic_invalid_post_data(self):
        '''
        Invalid post data should not redirect
        The expected behavior is to show the form again with validation errors
        '''
        url = reverse('new_topic', kwargs={'board_id': 1})
        response = self.client.post(url, {})
        self.assertEquals(response.status_code, 200)

    def test_new_topic_invalid_post_data_empty_field(self):
        '''
        Invalid post data should not redirect
        The expected behavior is to show the form again with validation error
        '''
        url = reverse('new_topic', kwargs={'board_id':1})
        data = {
            'subject':'',
            'message':''
        }
        response = self.client.post(url, data)
        self.assertEquals(response.status_code, 200)
        self.assertFalse(Topic.objects.exists())
        self.assertFalse(Post.objects.exists())

    # The following tests are for NewTopicForm
    def test_contains_form(self):  # <- new test
        url = reverse('new_topic', kwargs={'board_id': 1})
        response = self.client.get(url)
        form = response.context.get('form')
        # assertIsInstance -> grabbing the form instance in the context data, and checking if it is a NewTopicForm
        self.assertIsInstance(form, NewTopicForm)

    def test_new_topic_invalid_post_data(self):  # <- updated this one
        '''
        Invalid post data should not redirect
        The expected behavior is to show the form again with validation errors
        '''
        url = reverse('new_topic', kwargs={'board_id': 1})
        response = self.client.post(url, {})
        form = response.context.get('form')
        self.assertEquals(response.status_code, 200)
        self.assertTrue(form.errors)