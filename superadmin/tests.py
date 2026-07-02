from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from superadmin.models import ContactForm, BlogCategory, Blogs, Career, CareerApplication
import datetime

class SuperadminFilterTestCase(TestCase):
    def setUp(self):
        # Create test user and client
        self.user = User.objects.create_superuser(username='admin', email='admin@test.com', password='password')
        self.client = Client()
        self.client.force_login(self.user)

    def test_contact_list_source_filtering(self):
        # Create contact messages with different sources
        ContactForm.objects.create(name='John Web', email='john@web.com', phone='+971500000001', service='air-ambulance', message='Need transport support', country='Website')
        ContactForm.objects.create(name='Ali Oman', email='ali@oman.com', phone='+971500000002', service='air-ambulance', message='Need transport support', country='Oman')
        ContactForm.objects.create(name='Hassan Qatar', email='hassan@qatar.com', phone='+971500000003', service='air-ambulance', message='Need transport support', country='Qatar')
        ContactForm.objects.create(name='Saeed Saudi', email='saeed@saudi.com', phone='+971500000004', service='air-ambulance', message='Need transport support', country='Saudi Arabia')

        # Test no filter
        response = self.client.get(reverse('superadmin:ContactList'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['datas']), 4)

        # Test filter by Website
        response = self.client.get(reverse('superadmin:ContactList'), {'source': 'Website'})
        self.assertEqual(len(response.context['datas']), 1)
        self.assertEqual(response.context['datas'][0].name, 'John Web')

        # Test filter by Saudi
        response = self.client.get(reverse('superadmin:ContactList'), {'source': 'Saudi'})
        self.assertEqual(len(response.context['datas']), 1)
        self.assertEqual(response.context['datas'][0].name, 'Saeed Saudi')

        # Test filter by Oman
        response = self.client.get(reverse('superadmin:ContactList'), {'source': 'Oman'})
        self.assertEqual(len(response.context['datas']), 1)
        self.assertEqual(response.context['datas'][0].name, 'Ali Oman')

    def test_news_list_category_filtering(self):
        # Create categories
        cat1 = BlogCategory.objects.create(name='Medical Transport', name_ar='النقل الطبي')
        cat2 = BlogCategory.objects.create(name='Company News', name_ar='أخبار الشركة')

        # Create blogs
        blog1 = Blogs.objects.create(title='Transport Blog unique key 1', content='content1', category=cat1, is_active=True)
        blog2 = Blogs.objects.create(title='News Blog unique key 2', content='content2', category=cat2, is_active=True)

        # Test no filter includes the blogs we created
        response = self.client.get(reverse('superadmin:NewsList'))
        self.assertEqual(response.status_code, 200)
        titles = [b.title for b in response.context['datas']]
        self.assertIn('Transport Blog unique key 1', titles)
        self.assertIn('News Blog unique key 2', titles)

        # Test filter by cat1
        response = self.client.get(reverse('superadmin:NewsList'), {'category': cat1.id})
        for blog in response.context['datas']:
            self.assertEqual(blog.category, cat1)
        titles_filtered = [b.title for b in response.context['datas']]
        self.assertIn('Transport Blog unique key 1', titles_filtered)
        self.assertNotIn('News Blog unique key 2', titles_filtered)

        # Test filter by cat2
        response = self.client.get(reverse('superadmin:NewsList'), {'category': cat2.id})
        for blog in response.context['datas']:
            self.assertEqual(blog.category, cat2)
        titles_filtered2 = [b.title for b in response.context['datas']]
        self.assertNotIn('Transport Blog unique key 1', titles_filtered2)
        self.assertIn('News Blog unique key 2', titles_filtered2)

    def test_career_applications_filtering(self):
        # Create careers
        c1 = Career.objects.create(title='Air Ambulance Nurse', location='Dubai', date=datetime.date.today() + datetime.timedelta(days=10))
        c2 = Career.objects.create(title='Rescue Pilot', location='Abu Dhabi', date=datetime.date.today() + datetime.timedelta(days=15))

        # Create applications
        CareerApplication.objects.create(career=c1, name='Nurse Applicant', email='nurse@test.com', phone='1234567')
        CareerApplication.objects.create(career=c2, name='Pilot Applicant', email='pilot@test.com', phone='7654321')

        # Test no filter
        response = self.client.get(reverse('superadmin:ApplicationList'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['applications']), 2)

        # Test filter by career 1
        response = self.client.get(reverse('superadmin:ApplicationList'), {'career': c1.id})
        self.assertEqual(len(response.context['applications']), 1)
        self.assertEqual(response.context['applications'][0].name, 'Nurse Applicant')

        # Test filter by career 2
        response = self.client.get(reverse('superadmin:ApplicationList'), {'career': c2.id})
        self.assertEqual(len(response.context['applications']), 1)
        self.assertEqual(response.context['applications'][0].name, 'Pilot Applicant')

