from django.test import TestCase
from django.urls import reverse
from .models import Url
import datetime

class IndexTests(TestCase):

    def setUp(self):
        Url.objects.create(short_url='gWp', original_url='http://facebook.com', clicks=0, created_at=datetime.date.today(), updated_at=datetime.date.today())

    def test_no_urls(self):
        """
        If no URLs exist, an appropriate message is displayed
        """
        Url.objects.all().delete()
        response = self.client.get(reverse('index'))
        self.assertContains(response, 'There are no URLs in the system yet!')

    def test_submitting_new_url_failure(self):
        """
        When submitting an invalid URL, an error is returned to the user
        """
        response = self.client.post(reverse('store'), {'original_url': 'google'})
        self.assertEqual(response.status_code, 404)

    def test_submitting_new_url_success(self):
        """
        When submitting a valid URL, a success message is displayed
        """
        response = self.client.post(reverse('store'), {'original_url': 'http://facebook.com'})
        self.assertEqual(response.status_code, 200)

    def test_visiting_short_url_missing(self):
        """
        If short URL does not exist, custom 404 page is displayed
        """
        short_url = 'hd3'
        url = Url.objects.filter(short_url=short_url)
        if(not url):
            response = self.client.get(reverse('short_url', args=(short_url,)))
            self.assertEqual(response.status_code, 404)

    def test_visiting_short_url(self):
        """
        If short URL exists, stats logged and redirected to original URL
        """
        short_url = 'gWp'
        url = Url.objects.filter(short_url=short_url)
        if(url):
            response = self.client.get(reverse('short_url', args=(short_url,)))
            self.assertEqual(response.status_code, 302)
        
