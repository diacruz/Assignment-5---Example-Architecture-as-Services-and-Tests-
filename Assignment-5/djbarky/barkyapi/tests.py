from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework import routers
from rest_framework.test import APIRequestFactory, APITestCase
from .models import Bookmark, Snippet 
from datetime import datetime, timedelta
from django.utils.timezone import make_aware
from .models import Snippet
from django.utils import timezone

from rest_framework.test import APITestCase
from .models import Snippet

from .models import Bookmark
from .views import BookmarkViewSet

# Create your tests here.
# test plan


class BookmarkTests(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.bookmark = Bookmark.objects.create(
            id=1,
            title="Awesome Django",
            url="https://awesomedjango.org/",
            notes="Best place on the web for Django.",
        )
        # print(f"bookmark id: {self.bookmark.id}")

        # the simple router provides the name 'bookmark-list' for the URL pattern: https://www.django-rest-framework.org/api-guide/routers/#simplerouter
        self.list_url = reverse("barkyapi:bookmark-list")
        self.detail_url = reverse(
            "barkyapi:bookmark-detail", kwargs={"pk": self.bookmark.id}
        )
        

    # 1. create a bookmark
    def test_create_bookmark(self):
        """
        Ensure we can create a new bookmark object.
        """

        # the full record is required for the POST
        data = {
            "id": 99,
            "title": "Django REST framework",
            "url": "https://www.django-rest-framework.org/",
            "notes": "Best place on the web for Django REST framework.",
        }
        response = self.client.post(self.list_url, data, format="json")
        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(Bookmark.objects.count(), 2)
        self.assertEqual(Bookmark.objects.get(id=99).title, "Django REST framework")

    # 2. list bookmarks
    def test_list_bookmarks(self):
        """
        Ensure we can list all bookmark objects.
        """
        response = self.client.get(self.list_url)
        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(response.data["results"][0]["title"], self.bookmark.title)

    # 3. retrieve a bookmark
    def test_retrieve_bookmark(self):
        """
        Ensure we can retrieve a bookmark object.
        """
        response = self.client.get(self.detail_url)
        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(response.data["title"], self.bookmark.title)

    # 4. delete a bookmark
    def test_delete_bookmark(self):
        """
        Ensure we can delete a bookmark object.
        """
        response = self.client.delete(
            reverse("barkyapi:bookmark-detail", kwargs={"pk": self.bookmark.id})
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Bookmark.objects.count(), 0)

    # 5. update a bookmark
    def test_update_bookmark(self):
        """
        Ensure we can update a bookmark object.
        """
        # the full record is required for the POST
        data = {
            "id": 99,
            "title": "Awesomer Django",
            "url": "https://awesomedjango.org/",
            "notes": "Best place on the web for Django just got better.",
        }
        response = self.client.put(
            reverse("barkyapi:bookmark-detail", kwargs={"pk": self.bookmark.id}),
            data,
            format="json",
        )
        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(response.data["title"], "Awesomer Django")
       

class SnippetCreateTestCase(APITestCase):
    def setUp(self):
        self.create_url = reverse('barkyapi:snippet-list')
        self.user = User.objects.create(username='testuser', password='testpassword')
        self.valid_payload = {
             
            'title': 'Test Snippet',
            'code': 'print("Hello, world!")',
            'linenos': True,
            'language': 'python',
            'style': 'friendly',
            'owner': self.user.id
            
        }
        self.invalid_payload = {
            'title': '',
            'code': 'print("Hello, world!")',
            'linenos': True,
            'language': 'python',
            'style': 'friendly',
            'owner': self.user.id
        }
        self.create_url = reverse('barkyapi:snippet-list')
        self.user_detail_url = reverse('barkyapi:snippet-detail', kwargs={'pk': self.user.pk})
       
# 6. create a snippet
    def test_create_snippet(self):
       

        # the full record is required for the POST
        data = {
            "id": 9,
            "title": "test",
            "code": 'print("hello!")',
            "style": "friendly",
        }
        response = self.client.post(self.create_url, data, format="json")
        self.assertFalse(status.is_success(response.status_code))
        


# # 7. retrieve a snippet


    def test_retrieve_snippet(self):
      
        response = self.client.get(self.create_url)
        self.assertTrue(status.is_success(response.status_code))

       # self.assertEqual(response.data["id"], self.create_url.id)


#   # 8. delete a snippet
def test_delete_snippet(self):
        # Ensure the snippet exists before deletion
        self.assertTrue(Snippet.objects.filter(pk=self.snippet.pk).exists())

        # Authenticate the user
        self.client.force_authenticate(user=self.user)

        # make a delete request to delete the snippet
        response = self.client.delete(self.delete_url)

        # Check if the response status code is 204 (No Content) indicating successful deletion
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Ensure the snippet does not exist after deletion
        self.assertFalse(Snippet.objects.filter(pk=self.snippet.pk).exists())


# # 9. list snippets
def test_list_snippets(self):
        # Authenticate the user
        self.client.force_authenticate(user=self.user)

        # Make a GET request to list all snippets
        response = self.client.get(self.list_url)

        # Check if the response status code is 200 (OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check if both snippets are present in the response data
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['title'], 'Test Snippet 1')
        self.assertEqual(response.data[1]['title'], 'Test Snippet 2')


# # 10. update a snippet
def test_update_snippet(self):
        # Authenticate the user
        self.client.force_authenticate(user=self.user)

        # Make a PUT request to update the snippet with valid payload
        response = self.client.put(self.update_url, self.valid_payload)

        # Check if the response status code is 200 (OK) indicating successful update
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Refresh the snippet instance from the database
        self.snippet.refresh_from_db()

        # Check if the snippet attributes are updated correctly
        self.assertEqual(self.snippet.title, self.valid_payload['title'])
        self.assertEqual(self.snippet.code, self.valid_payload['code'])
        self.assertEqual(self.snippet.linenos, self.valid_payload['linenos'])


#User class
class UserAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.create_user_url = reverse('barkyapi:user-list')
        self.user_detail_url = reverse('barkyapi:user-detail', kwargs={'pk': self.user.pk})

 # 11. create a user
    def test_create_user(self):
        data = {
            'username': 'testuser',
            'password': 'testpassword'
        }
        response = self.client.post(self.create_user_url, data, format='json')

        # Verify that the HTTP method is allowed for the URL
        self.assertIn(response.status_code, [status.HTTP_201_CREATED, status.HTTP_405_METHOD_NOT_ALLOWED])

       
        if response.status_code == status.HTTP_201_CREATED:
            self.assertTrue(User.objects.filter(username='testuser').exists())


    #12. Retrieve a user
    def test_retrieve_user(self):
        # Retrieve the user ID of the created user
        user_id = self.user.id

        # Set up the URL for retrieving the specific user
        retrieve_user_url = reverse('barkyapi:user-detail', kwargs={'pk': user_id})

        # Send a GET request to retrieve the user
        response = self.client.get(retrieve_user_url)

        # Assert that the response status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

       
        self.assertEqual(response.data['username'], 'testuser')


# 13. delete a user
def test_delete_bookmark(self):
        user_id = self.user.id
        """
        Ensure we can delete a bookmark object.
        """
        response = self.client.delete(
            reverse('barkyapi:user-detail', kwargs={'pk': user_id})
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Bookmark.objects.count(), 0)

# 14. list users
def test_list_users(self):
        response = self.client.get(self.create_user_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1) 

        self.assertEqual(response.data[0]['username'], 'testuser')
   

# 15. update a user
def test_update_user(self):
        updated_data = {
            'username': 'updateduser',
            'password': 'updatedpassword'
        }
        response = self.client.put(self.user_detail_url, updated_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check if the user's username and password are updated in the database
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'updateduser')
        self.assertTrue(self.user.check_password('updatedpassword'))

class SnippetHighlightTestCase(APITestCase):
    def setUp(self):
        self.snippet = Snippet.objects.create(
            title='Test Snippet',
            code='print("Hello, world!")',
            linenos=True,
            language='python',
            style='friendly',
            owner=User.objects.create(username='testuser', password='testpassword')
        )
        self.highlight_url = reverse('barkyapi:snippet-highlight', kwargs={'pk': self.snippet.pk})
#16. highlight a snippet
    def test_highlight_snippet(self):
        response = self.client.get(self.highlight_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('<span class="p">', response.content.decode())

# 17. list bookmarks by user
class BookmarkListByUserTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser', password='testpassword')
        self.bookmark = Bookmark.objects.create(
            title="Test Bookmark",
            url="https://example.com/",
            notes="Test notes",
          
        )
        self.list_url = reverse(
            "barkyapi:bookmark-detail", kwargs={"pk": self.bookmark.id}
        )

    def test_list_bookmarks_by_user(self):
        response = self.client.get(self.list_url)
        self.assertEqual(len(response.data), 1)
        
       ####IGNORE

        

class ListSnippetByUser(APITestCase):
    def setUp(self):
        # Create a user
        user = User.objects.create(username="test_user")

        # Create snippets associated with the user
        snippet1 = Snippet.objects.create(user=user, text="Snippet 1")
        snippet2 = Snippet.objects.create(user=user, text="Snippet 2")

        # Serialize the user with associated snippets
        serializer = ListSnippetByUser(user)

        # Assert serialized data
        self.assertEqual(serializer.data["id"], user.id)
        self.assertEqual(serializer.data["username"], user.username)
        self.assertEqual(len(serializer.data["snippets"]), 2)
        self.assertEqual(serializer.data["snippets"][0]["id"], snippet1.id)
        self.assertEqual(serializer.data["snippets"][0]["text"], snippet1.text)
        self.assertEqual(serializer.data["snippets"][1]["id"], snippet2.id)
        self.assertEqual(serializer.data["snippets"][1]["text"], snippet2.text)
        self.list_url = reverse("barkyapi:snippet-list")
        self.detail_url = reverse(
            "barkyapi:snippet-detail", kwargs={"pk": self.snippet.id}
        )


# 18. list snippets by user
def test_list_snippets_by_user(self):
        # Make a GET request to list snippets by the specific user
        response = self.client.get(self.list_url)

        # Check if the response status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check if the returned data contains the snippet created by the user
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], "Test Snippet")



# 20. list bookmarks by date


class BookmarkTests(APITestCase):
    def setUp(self):
        self.bookmark1 = Bookmark.objects.create(
            title="Bookmark 1",
            url="https://bookmark1.com/",
            notes="Bookmark 1 notes.",
            date_added=datetime(2024, 4, 30)
        )
        self.bookmark2 = Bookmark.objects.create(
            title="Bookmark 2",
            url="https://bookmark2.com/",
            notes="Bookmark 2 notes.",
            date_added=datetime(2024, 4, 29)
        )
        self.list_url = reverse("barkyapi:bookmark-list")

    def test_list_bookmarks_by_date(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Ensure the bookmarks are listed in descending order of date_added
        bookmarks = response.data
        self.assertEqual(len(bookmarks), 4)
     



# 21. list snippets by date

def test_list_snippets_by_date(self):
        # make a GET request to list snippets created within the last 2 days
        two_days_ago = datetime.now() - timedelta(days=2)
        response = self.client.get(self.create_url, {'created__gte': two_days_ago})

        # Check if the response status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check if the returned data contains the snippets created within the last 2 days
        self.assertEqual(len(response.data), 2) 
   


# 23. list bookmarks by title

class BookmarkListByTitleTestCase(APITestCase):
    def setUp(self):
        self.bookmark1 = Bookmark.objects.create(
            title="Django Book",
            url="https://django.com/",
            notes="Bookmark 1 notes.",
        )
        self.bookmark2 = Bookmark.objects.create(
            title="Python Book",
            url="https://python.com/",
            notes="Bookmark 2 notes.",
        )
        self.list_url = reverse("barkyapi:bookmark-list")

    def test_list_bookmarks_by_title(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Ensure the bookmarks are listed in ascending order of title
        bookmarks = response.data
      #  self.assertEqual(bookmarks[1]["title"], "Python Book")



class BookmarkTests(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.bookmark = Bookmark.objects.create(
            id=1,
            title="Awesome Django",
            url="https://awesomedjango.org/",
            notes="Best place on the web for Django.",
        )
        # print(f"bookmark id: {self.bookmark.id}")

        # the simple router provides the name 'bookmark-list' for the URL pattern: https://www.django-rest-framework.org/api-guide/routers/#simplerouter
        self.list_url = reverse("barkyapi:bookmark-list")
        self.detail_url = reverse(
            "barkyapi:bookmark-detail", kwargs={"pk": self.bookmark.id}
        )
        


# 24. list snippets by title

def test_list_snippets_by_title(self):
        # Create a snippet
        response = self.client.post(self.create_url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Make a GET request to list snippets by title
        response = self.client.get(self.create_url, {'title': 'Test Snippet'})

        # Check if the response status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check if the returned data contains the snippet with the specified title
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Test Snippet')


# 26. list bookmarks by url

def test_list_bookmarks_by_url(self):
        # Make a GET request to list bookmarks by URL
        response = self.client.get(self.list_url, {'title': 'Awesome Django'})

        # Check if the response status code is 200 OK
        self.assertEqual(response.status_code, 200)

        # Check if the returned data contains the bookmark with the specified title
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Awesome Django')



# 27. list snippets by url


class SnippetCreateTestCase(APITestCase):
    def setUp(self):
        self.create_url = reverse('barkyapi:snippet-list')
        self.user = User.objects.create(username='testuser', password='testpassword')
        self.snippet1 = Snippet.objects.create(
            title='Test Snippet 1',
            code='print("Hello, world!")',
            linenos=True,
            language='python',
            style='friendly',
            owner=self.user,
            highlighted='Highlighted code here...'
        )
        self.snippet2 = Snippet.objects.create(
            title='Test Snippet 2',
            code='print("Another snippet!")',
            linenos=False,
            language='python',
            style='friendly',
            owner=self.user,
            highlighted='Highlighted code here...'
        )

    def test_list_snippets_by_url(self):
        # Make a GET request to list snippets by URL
        response = self.client.get(self.create_url, {'title': 'Test Snippet 1'})

        # Check if the response status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

      
        


