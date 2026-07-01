from django.test import TestCase, Client
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from superadmin.models import ContactForm, Career, CareerApplication
from django.core import mail

class FormVerificationTests(TestCase):
    def setUp(self):
        self.client = Client()
        # Create a mock career position for testing career applications
        self.career = Career.objects.create(
            title="Senior AI Engineer",
            slug="senior-ai-engineer",
            is_active=True
        )

    def test_otp_flow_and_locking(self):
        # 1. Request OTP
        response = self.client.post(reverse('website:send_otp'), {'email': 'zuarakcore@gmail.com'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('email_otp', self.client.session)
        self.assertEqual(self.client.session['otp_email'], 'zuarakcore@gmail.com')
        
        otp = self.client.session['email_otp']
        self.assertTrue(otp.isdigit() and len(otp) == 4)

        # 2. Try verifying with wrong OTP multiple times to test lock
        for i in range(9):
            response = self.client.post(reverse('website:verify_otp'), {
                'email': 'zuarakcore@gmail.com',
                'otp': '9999' # incorrect OTP
            })
            self.assertEqual(response.status_code, 400)
            self.assertEqual(response.json()['message'], 'Invalid verification code.')

        # The 10th failure should lock the session
        response = self.client.post(reverse('website:verify_otp'), {
            'email': 'zuarakcore@gmail.com',
            'otp': '9999'
        })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['message'], 'Too many failed verification attempts. Please request a new code.')
        self.assertTrue(self.client.session['otp_locked'])
        self.assertIsNone(self.client.session['email_otp'])

        # Try verifying with correct OTP now; it should fail because of lock
        response = self.client.post(reverse('website:verify_otp'), {
            'email': 'zuarakcore@gmail.com',
            'otp': otp
        })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['message'], 'Too many failed verification attempts. Please request a new code.')

    def test_successful_otp_and_enquiry_submission(self):
        # 1. Request OTP
        response = self.client.post(reverse('website:send_otp'), {'email': 'zuarakcore@gmail.com'})
        self.assertEqual(response.status_code, 200)
        otp = self.client.session['email_otp']

        # 2. Verify with correct OTP
        response = self.client.post(reverse('website:verify_otp'), {
            'email': 'zuarakcore@gmail.com',
            'otp': otp
        })
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.client.session['email_verified'])
        self.assertEqual(self.client.session['verified_email'], 'zuarakcore@gmail.com')

        # 3. Submit enquiry form
        response = self.client.post(reverse('website:submit_enquiry'), {
            'name': 'Test User',
            'email': 'zuarakcore@gmail.com',
            'phone': '+91 97454 10000',
            'services': 'Air Ambulance',
            'message': 'This is a valid enquiry message for testing.',
            'consent': 'on',
            'country': 'Oman'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('redirect_url', response.json())
        self.assertEqual(response.json()['redirect_url'], '/thank-you/')

        # Verify record is saved in DB
        self.assertEqual(ContactForm.objects.count(), 1)
        enquiry = ContactForm.objects.first()
        self.assertEqual(enquiry.name, 'Test User')
        self.assertEqual(enquiry.country, 'Oman')

    def test_career_apply_flow(self):
        # 1. Request OTP
        response = self.client.post(reverse('website:send_otp'), {'email': 'zuarakcore@gmail.com'})
        self.assertEqual(response.status_code, 200)
        otp = self.client.session['email_otp']

        # 2. Verify with correct OTP
        response = self.client.post(reverse('website:verify_otp'), {
            'email': 'zuarakcore@gmail.com',
            'otp': otp
        })
        self.assertEqual(response.status_code, 200)

        # 3. Submit Career Application
        pdf_file = SimpleUploadedFile("resume.pdf", b"pdf content", content_type="application/pdf")
        response = self.client.post(reverse('website:career_detail', kwargs={'slug': self.career.slug}), {
            'name': 'Applicant Name',
            'email': 'zuarakcore@gmail.com',
            'phone': '+91 98765 43210',
            'location': 'Kochi, Kerala',
            'resume': pdf_file
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('redirect_url', response.json())
        self.assertEqual(response.json()['redirect_url'], '/thank-you/')

        # Verify application record is saved
        self.assertEqual(CareerApplication.objects.count(), 1)
        app = CareerApplication.objects.first()
        self.assertEqual(app.name, 'Applicant Name')
        self.assertEqual(app.career, self.career)
