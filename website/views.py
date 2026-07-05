# Standard Django imports
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.http import JsonResponse
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.db.models import Q

# Models from your application
from superadmin.models import *

# System imports
import sys


# ── HOME ────────────────────────────────────────────────────────────────────
class HomePageView(View):
    def get(self, request):
        blogs = Blogs.objects.filter(is_active=True).order_by('-date', '-created_at')
        categories = BlogCategory.objects.filter(is_active=True)
        context = {
            'path': 'home',
            'blogs': blogs,
            'categories': categories,
        }
        return render(request, 'website/home/index.html', context)


# ── ABOUT ───────────────────────────────────────────────────────────────────
class AboutPageView(View):
    def get(self, request):
        context = {'path': 'about'}
        return render(request, 'website/about/index.html', context)


# ── CONTACT ─────────────────────────────────────────────────────────────────
class ContactPageView(View):
    def get(self, request):
        context = {'path': 'contact'}
        return render(request, 'website/contact/index.html', context)

    def post(self, request):
        import re
        from django.utils import timezone

        honeypot = request.POST.get('website_url', '')
        if honeypot:
            messages.error(request, "Spam submission detected.")
            return redirect('website:contactus')

        name = request.POST.get('Name', '').strip()
        email = request.POST.get('Email', '').strip()
        phone = request.POST.get('Phone', '').strip()
        service = request.POST.get('Service', '').strip()
        message = request.POST.get('Message', '').strip()

        if not name or len(name) < 2:
            messages.error(request, "Please enter a valid name.")
            return redirect('website:contactus')

        email_pattern = re.compile(r'^[^\s@]+@[^\s@]+\.[^\s@]+$')
        if not email or not email_pattern.match(email):
            messages.error(request, "Please enter a valid email address.")
            return redirect('website:contactus')

        phone_clean = re.sub(r'[\s\-\(\)]', '', phone)
        if not re.match(r'^\+?[0-9]{7,15}$', phone_clean):
            messages.error(request, "Please enter a valid phone number.")
            return redirect('website:contactus')

        if not service:
            messages.error(request, "Please select a service.")
            return redirect('website:contactus')

        if not message or len(message) < 10:
            messages.error(request, "Please enter a message (at least 10 characters).")
            return redirect('website:contactus')

        today_start = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        if ContactForm.objects.filter(email=email, created_at__gte=today_start).exists():
            messages.error(request, "You have already submitted a message today. We'll get back to you soon!")
            return redirect('website:contactus')

        ContactForm.objects.create(name=name, email=email, phone=phone, service=service, message=message)

        from django.conf import settings
        text_content = f"""
        <h3>New Contact Form Submission</h3>
        <table border="1" cellpadding="5" style="border-collapse: collapse;">
            <tr><th>Name</th><td>{name}</td></tr>
            <tr><th>Service</th><td>{service}</td></tr>
            <tr><th>Email</th><td>{email}</td></tr>
            <tr><th>Phone</th><td>{phone}</td></tr>
            <tr><th>Message</th><td>{message}</td></tr>
        </table>
        """
        try:
            mail = EmailMultiAlternatives(
                subject="Blue Dot - New Contact Form Submission",
                body=f"Name: {name}\nService: {service}\nEmail: {email}\nPhone: {phone}\nMessage: {message}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[settings.DEFAULT_FROM_EMAIL],
                reply_to=[email]
            )
            mail.attach_alternative(text_content, "text/html")
            mail.send()
        except Exception:
            pass

        messages.success(request, "Thank you! Your message has been received. We'll get back to you within 24 hours.")
        return redirect('website:contactus')


# ── NEWS & STORIES ───────────────────────────────────────────────────────────
class BlogListView(View):
    def get(self, request, *args, **kwargs):
        category_slug = request.GET.get('category', 'all')
        
        # Banner always shows the latest overall blog post
        featured = Blogs.objects.filter(is_active=True).order_by('-date', '-created_at').first()

        # Grid list shows all filtered posts (including the featured one)
        grid_blogs = Blogs.objects.filter(is_active=True).order_by('-date', '-created_at')
        if category_slug and category_slug != 'all':
            grid_blogs = grid_blogs.filter(category__slug=category_slug)

        # Check if Ajax request
        is_ajax_request = request.headers.get('x-requested-with') == 'XMLHttpRequest' or is_ajax(request)
        if is_ajax_request:
            context = {
                'blogs': grid_blogs,
            }
            return render(request, 'website/news/_news_grid.html', context)

        categories = BlogCategory.objects.filter(is_active=True)
        context = {
            'path': 'blogs',
            'featured': featured,
            'blogs': grid_blogs,
            'categories': categories,
            'active_category': category_slug,
        }
        return render(request, 'website/news/index.html', context)



class BlogDetailPageView(View):
    def get(self, request, slug, *args, **kwargs):
        post = get_object_or_404(Blogs, slug=slug, is_active=True)
        recent = Blogs.objects.filter(is_active=True).exclude(id=post.id).order_by('-date', '-created_at')[:3]
        context = {
            'path': 'blog-detail',
            'post': post,
            'recent': recent,
        }
        return render(request, 'website/news/detail.html', context)


# ── CAREERS ──────────────────────────────────────────────────────────────────
class CareersPageView(View):
    def get(self, request):
        careers = Career.objects.filter(is_active=True).order_by('-date', '-created_at')
        context = {
            'path': 'careers',
            'careers': careers,
        }
        return render(request, 'website/careers/index.html', context)


class CareerDetailView(View):
    def get(self, request, slug):
        career = get_object_or_404(Career, slug=slug, is_active=True)
        context = {
            'path': 'careers',
            'career': career,
        }
        return render(request, 'website/careers/detail.html', context)

    def post(self, request, slug):
        import re
        from django.utils.html import strip_tags
        from django.conf import settings
        from django.core.mail import EmailMultiAlternatives
        from django.template.loader import render_to_string
        from email.mime.image import MIMEImage
        import os

        career = get_object_or_404(Career, slug=slug, is_active=True)
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        location = request.POST.get('location', '').strip()
        resume = request.FILES.get('resume')

        # Check OTP verification
        session_verified = request.session.get('email_verified')
        session_verified_email = request.session.get('verified_email')
        
        if not session_verified or not session_verified_email or session_verified_email.lower() != email.lower():
            return JsonResponse({'status': 'error', 'message': 'Please verify your email address before submitting.'}, status=400)

        # Validations
        if not name or len(name) < 2:
            return JsonResponse({'status': 'error', 'message': 'Please enter a valid name (at least 2 characters).'}, status=400)
            
        email_pattern = re.compile(r'^[^\s@]+@[^\s@]+\.[^\s@]+$')
        if not email or not email_pattern.match(email):
            return JsonResponse({'status': 'error', 'message': 'Please enter a valid email address.'}, status=400)
            
        phone_clean = re.sub(r'[\s\-\(\)]', '', phone)
        if not re.match(r'^\+?[0-9]{7,15}$', phone_clean):
            return JsonResponse({'status': 'error', 'message': 'Please enter a valid phone number.'}, status=400)
            
        if not location:
            return JsonResponse({'status': 'error', 'message': 'Please enter your location.'}, status=400)
            
        if not resume:
            return JsonResponse({'status': 'error', 'message': 'Please upload your resume.'}, status=400)

        name = strip_tags(name)
        email = strip_tags(email)
        phone = strip_tags(phone)
        location = strip_tags(location)

        # Save record
        application = CareerApplication.objects.create(
            career=career,
            name=name,
            email=email,
            phone=phone,
            location=location,
            resume=resume
        )

        # 1. Send application details email to mail@bluedotassist.com
        subject_owner = f"Blue Dot - New Career Application: {career.title}"
        body_owner = f"New career application received for position: {career.title}\n\n" \
                     f"Name: {name}\n" \
                     f"Email: {email}\n" \
                     f"Phone: {phone}\n" \
                     f"Location: {location}\n"
                     
        html_owner = f"""
        <h3>New Career Application Received</h3>
        <p><strong>Position:</strong> {career.title}</p>
        <table border="1" cellpadding="8" style="border-collapse: collapse; border-color: #ddd; font-family: sans-serif; width: 100%; max-width: 500px;">
            <tr style="background-color: #f2f2f2;"><th align="left">Field</th><th align="left">Submitted Value</th></tr>
            <tr><td><strong>Position</strong></td><td>{career.title}</td></tr>
            <tr><td><strong>Name</strong></td><td>{name}</td></tr>
            <tr><td><strong>Email</strong></td><td>{email}</td></tr>
            <tr><td><strong>Phone</strong></td><td>{phone}</td></tr>
            <tr><td><strong>Location</strong></td><td>{location}</td></tr>
        </table>
        """
        
        try:
            mail_owner = EmailMultiAlternatives(
                subject=subject_owner,
                body=body_owner,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=['mail@bluedotassist.com']
            )
            mail_owner.attach_alternative(html_owner, "text/html")
            
            # Attach resume
            if resume:
                resume.seek(0)
                mail_owner.attach(resume.name, resume.read(), resume.content_type)
                
            mail_owner.send()
        except Exception:
            pass

        # 2. Send Applicant a confirmation email
        applicant_subject = f"Your application for {career.title} - Blue Dot"
        applicant_context = {
            'name': name,
            'email': email,
            'phone': phone,
            'service': f"Job Application: {career.title}",
            'message': f"Thank you for applying for the position of {career.title}. We have received your CV and details.",
            'country': location,
        }
        applicant_html = render_to_string('website/emails/applicant_email.html', applicant_context)
        applicant_text = f"Dear {name},\n\nThank you for applying for the position of {career.title} at Blue Dot. We have received your application and will review it shortly.\n\nBest regards,\nBlue Dot Team"
        
        try:
            mail_applicant = EmailMultiAlternatives(
                subject=applicant_subject,
                body=applicant_text,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[email]
            )
            mail_applicant.attach_alternative(applicant_html, "text/html")
            mail_applicant.mixed_subtype = 'related'
            
            # Attach logo
            logo_path = os.path.join(settings.BASE_DIR, 'static', 'website', 'images', 'bl-logo.png')
            if os.path.exists(logo_path):
                with open(logo_path, 'rb') as f:
                    logo_data = f.read()
                mime_image = MIMEImage(logo_data)
                mime_image.add_header('Content-ID', '<bluedot_logo>')
                mime_image.add_header('Content-Disposition', 'inline', filename='bl-logo.png')
                mail_applicant.attach(mime_image)
                
            mail_applicant.send()
        except Exception:
            pass

        # Clear session verification
        request.session['email_verified'] = False
        request.session['verified_email'] = None
        request.session.modified = True

        return JsonResponse({'status': 'success', 'redirect_url': '/thank-you/'})


# ── SERVICES ─────────────────────────────────────────────────────────────────
class ServiceAirAmbulanceView(View):
    def get(self, request):
        context = {'path': 'services'}
        return render(request, 'website/services/air-ambulance.html', context)


class ServiceCommercialView(View):
    def get(self, request):
        context = {'path': 'services'}
        return render(request, 'website/services/commercial-airline-transfer.html', context)


class ServiceMedicalEscortView(View):
    def get(self, request):
        context = {'path': 'services'}
        return render(request, 'website/services/medical-escort.html', context)


class ServiceHelicopterView(View):
    def get(self, request):
        context = {'path': 'services'}
        return render(request, 'website/services/helicopter-air-ambulance.html', context)


# ── FLEET ────────────────────────────────────────────────────────────────────
class FleetSelectView(View):
    def get(self, request):
        context = {'path': 'fleet'}
        return render(request, 'website/fleet/select.html', context)


class FleetView(View):
    def get(self, request):
        context = {'path': 'fleet'}
        return render(request, 'website/fleet/index.html', context)


class FleetChallenger604View(View):
    def get(self, request):
        context = {'path': 'fleet'}
        return render(request, 'website/fleet/challenger-604.html', context)


class FleetChallenger605View(View):
    def get(self, request):
        context = {'path': 'fleet-605'}
        return render(request, 'website/fleet/challenger-605.html', context)


class FleetKingAirB200View(View):
    def get(self, request):
        context = {'path': 'fleet'}
        return render(request, 'website/fleet/king-air-b200.html', context)


class FleetKingAirC90View(View):
    def get(self, request):
        context = {'path': 'fleet'}
        return render(request, 'website/fleet/king-air-c90.html', context)


# ── REGIONS ──────────────────────────────────────────────────────────────────
class RegionBahrainView(View):
    def get(self, request):
        context = {'path': 'regions'}
        return render(request, 'website/regions/bahrain.html', context)


class RegionOmanView(View):
    def get(self, request):
        context = {'path': 'regions'}
        return render(request, 'website/regions/oman.html', context)


class RegionQatarView(View):
    def get(self, request):
        context = {'path': 'regions'}
        return render(request, 'website/regions/qatar.html', context)


class RegionSaudiView(View):
    def get(self, request):
        context = {'path': 'regions'}
        return render(request, 'website/regions/saudi-arabia.html', context)


# ── THANK YOU ────────────────────────────────────────────────────────────────
class ThankYouView(View):
    def get(self, request):
        context = {'path': 'thankyou'}
        return render(request, 'website/thankyou/index.html', context)


# ── ERROR PAGES ──────────────────────────────────────────────────────────────
def error_404(request, exception):
    return render(request, 'website/error_404.html', status=404)


class ComingSoonPageView(View):
    def get(self, request, *args, **kwargs):
        context = {'path': 'coming-soon'}
        return render(request, 'website/coming_soon.html', context)


# ── HELPER ───────────────────────────────────────────────────────────────────
def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'
# ── LEADERSHIP ───────────────────────────────────────────────────────────────
class LeadershipDetailView(View):
    def get(self, request, slug, *args, **kwargs):
        context = {'path': 'leadership'}
        # Map slug to template name
        template_name = f'website/leadership/{slug}.html'
        return render(request, template_name, context)

# ── LEGAL ────────────────────────────────────────────────────────────────────
class PrivacyPolicyView(View):
    def get(self, request):
        context = {'path': 'privacy-policy'}
        return render(request, 'website/legal/privacy-policy.html', context)

class TermsConditionView(View):
    def get(self, request):
        context = {'path': 'terms-and-condition'}
        return render(request, 'website/legal/terms-and-condition.html', context)


# ── OTP & ENQUIRY VIEWS ──────────────────────────────────────────────────────
import random
import re
from django.utils import timezone
from datetime import timedelta
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.utils.html import strip_tags
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from email.mime.image import MIMEImage
import os
from django.conf import settings

class SendOTPView(View):
    def post(self, request):
        email = request.POST.get('email', '').strip()
        if not email:
            return JsonResponse({'status': 'error', 'message': 'Email address is required.'}, status=400)
        
        try:
            validate_email(email)
        except ValidationError:
            return JsonResponse({'status': 'error', 'message': 'Please enter a valid email address.'}, status=400)
        
        # Throttling check: check if an OTP was sent recently (within last 60 seconds)
        last_sent_str = request.session.get('otp_timestamp')
        if last_sent_str:
            try:
                last_sent = timezone.datetime.fromisoformat(last_sent_str)
                if timezone.now() - last_sent < timedelta(seconds=60):
                    return JsonResponse({'status': 'error', 'message': 'Please wait 60 seconds before requesting another code.'}, status=429)
            except (ValueError, TypeError):
                pass
        
        # Generate 4-digit numeric OTP
        otp = str(random.randint(1000, 9999))
        
        # Store in session
        request.session['email_otp'] = otp
        request.session['otp_email'] = email
        request.session['otp_timestamp'] = timezone.now().isoformat()
        request.session['otp_failed_attempts'] = 0
        request.session['otp_locked'] = False
        request.session.modified = True
        
        # Render email HTML
        context = {
            'otp': otp,
            'email': email,
        }
        html_content = render_to_string('website/emails/otp_email.html', context)
        text_content = f"Your Blue Dot verification code is: {otp}"
        
        try:
            mail = EmailMultiAlternatives(
                subject="Blue Dot - Email Verification Code",
                body=text_content,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[email]
            )
            mail.attach_alternative(html_content, "text/html")
            mail.mixed_subtype = 'related'  # Set subtype to 'related' so inline attachments show up correctly!
            
            # Attach logo
            logo_path = os.path.join(settings.BASE_DIR, 'static', 'website', 'images', 'bl-logo.png')
            if os.path.exists(logo_path):
                with open(logo_path, 'rb') as f:
                    logo_data = f.read()
                mime_image = MIMEImage(logo_data)
                mime_image.add_header('Content-ID', '<bluedot_logo>')
                mime_image.add_header('Content-Disposition', 'inline', filename='bl-logo.png')
                mail.attach(mime_image)
                
            mail.send()
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': f'Failed to send verification email. Please try again. ({str(e)})'}, status=500)
            
        return JsonResponse({'status': 'success', 'message': 'Verification code sent to your email.'})


class VerifyOTPView(View):
    def post(self, request):
        email = request.POST.get('email', '').strip()
        otp_input = request.POST.get('otp', '').strip()
        
        if not email or not otp_input:
            return JsonResponse({'status': 'error', 'message': 'Email and verification code are required.'}, status=400)
            
        session_otp = request.session.get('email_otp')
        session_email = request.session.get('otp_email')
        session_timestamp_str = request.session.get('otp_timestamp')
        failed_attempts = request.session.get('otp_failed_attempts', 0)
        
        # Log session keys and emails for console debugging
        print(f"[OTP Debug] Session Key: {request.session.session_key}")
        print(f"[OTP Debug] Input Email: '{email}', Input OTP: '{otp_input}'")
        print(f"[OTP Debug] Session Email: '{session_email}', Session OTP: '{session_otp}', Failed Attempts: {failed_attempts}")
        
        if request.session.get('otp_locked'):
            return JsonResponse({'status': 'error', 'message': 'Too many failed verification attempts. Please request a new code.'}, status=400)

        if not session_otp or not session_email or session_email.lower() != email.lower():
            return JsonResponse({'status': 'error', 'message': 'No verification code was sent to this email. Please request a code first.'}, status=400)
            
        # Max attempts check
        if failed_attempts >= 10:
            request.session['email_otp'] = None # Invalidate
            request.session['otp_locked'] = True
            request.session.modified = True
            return JsonResponse({'status': 'error', 'message': 'Too many failed verification attempts. Please request a new code.'}, status=400)
            
        # Expiration check (10 minutes)
        if session_timestamp_str:
            try:
                session_timestamp = timezone.datetime.fromisoformat(session_timestamp_str)
                if timezone.now() - session_timestamp > timedelta(minutes=10):
                    request.session['email_otp'] = None # Invalidate
                    request.session.modified = True
                    return JsonResponse({'status': 'error', 'message': 'Verification code has expired. Please request a new one.'}, status=400)
            except (ValueError, TypeError):
                pass
                
        if session_otp == otp_input:
            # Mark verified
            request.session['email_verified'] = True
            request.session['verified_email'] = email
            request.session['email_otp'] = None # Clear
            request.session.modified = True
            return JsonResponse({'status': 'success', 'message': 'Email verified successfully!'})
        else:
            new_attempts = failed_attempts + 1
            request.session['otp_failed_attempts'] = new_attempts
            if new_attempts >= 10:
                request.session['email_otp'] = None
                request.session['otp_locked'] = True
                request.session.modified = True
                return JsonResponse({'status': 'error', 'message': 'Too many failed verification attempts. Please request a new code.'}, status=400)
            request.session.modified = True
            return JsonResponse({'status': 'error', 'message': 'Invalid verification code.'}, status=400)


class SubmitEnquiryView(View):
    def post(self, request):
        # Honeypot checks
        honeypot = request.POST.get('website_url', '') or request.POST.get('_honey', '')
        if honeypot:
            return JsonResponse({'status': 'success', 'redirect_url': '/thank-you/'})
            
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        service = request.POST.get('services', '').strip()
        message = request.POST.get('message', '').strip()
        consent = request.POST.get('consent', '')
        country = request.POST.get('country', 'Website').strip()

        # Validations
        if not name or len(name) < 2:
            return JsonResponse({'status': 'error', 'message': 'Please enter a valid name (at least 2 characters).'}, status=400)
            
        email_pattern = re.compile(r'^[^\s@]+@[^\s@]+\.[^\s@]+$')
        if not email or not email_pattern.match(email):
            return JsonResponse({'status': 'error', 'message': 'Please enter a valid email address.'}, status=400)
            
        phone_clean = re.sub(r'[\s\-\(\)]', '', phone)
        if not re.match(r'^\+?[0-9]{7,15}$', phone_clean):
            return JsonResponse({'status': 'error', 'message': 'Please enter a valid phone number (7 to 15 digits).'}, status=400)
            
        if not service:
            return JsonResponse({'status': 'error', 'message': 'Please select a service.'}, status=400)
            
        if not message or len(message) < 10:
            return JsonResponse({'status': 'error', 'message': 'Please enter a message (at least 10 characters).'}, status=400)
            
        if not consent:
            return JsonResponse({'status': 'error', 'message': 'You must accept the terms and consent to submit the form.'}, status=400)

        # Check session verification
        session_verified = request.session.get('email_verified')
        session_verified_email = request.session.get('verified_email')
        
        if not session_verified or not session_verified_email or session_verified_email.lower() != email.lower():
            return JsonResponse({'status': 'error', 'message': 'Please verify your email address before submitting the form.'}, status=400)

        # Sanitize data
        name = strip_tags(name)
        email = strip_tags(email)
        phone = strip_tags(phone)
        service = strip_tags(service)
        message = strip_tags(message)
        country = strip_tags(country)

        # Save ContactForm record
        enquiry = ContactForm.objects.create(
            name=name,
            email=email,
            phone=phone,
            service=service,
            message=message,
            country=country
        )

        # 1. Send Enquiry to mail@bluedotassist.com
        # format of content:
        subject_owner = f"Blue Dot - New Enquiry ({country})"
        body_owner = f"New enquiry received from {country} page:\n\n" \
                     f"Name: {name}\n" \
                     f"Email: {email}\n" \
                     f"Phone: {phone}\n" \
                     f"Service: {service}\n" \
                     f"Country/Source: {country}\n" \
                     f"Message:\n{message}\n"
                     
        html_owner = f"""
        <h3>New Enquiry Received</h3>
        <p><strong>Source / Country:</strong> {country}</p>
        <table border="1" cellpadding="8" style="border-collapse: collapse; border-color: #ddd; font-family: sans-serif; width: 100%; max-width: 500px;">
            <tr style="background-color: #f2f2f2;"><th align="left">Field</th><th align="left">Submitted Value</th></tr>
            <tr><td><strong>Name</strong></td><td>{name}</td></tr>
            <tr><td><strong>Email</strong></td><td>{email}</td></tr>
            <tr><td><strong>Phone</strong></td><td>{phone}</td></tr>
            <tr><td><strong>Service</strong></td><td>{service}</td></tr>
            <tr><td><strong>Country/Source</strong></td><td>{country}</td></tr>
            <tr><td><strong>Message</strong></td><td>{message}</td></tr>
        </table>
        """
        
        try:
            mail_owner = EmailMultiAlternatives(
                subject=subject_owner,
                body=body_owner,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=['mail@bluedotassist.com'],
                reply_to=[email]
            )
            mail_owner.attach_alternative(html_owner, "text/html")
            mail_owner.send()
        except Exception:
            pass

        # 2. Send Applicant a confirmation email using HTML template
        applicant_subject = "We have received your enquiry - Blue Dot"
        applicant_context = {
            'name': name,
            'email': email,
            'phone': phone,
            'service': service,
            'message': message,
            'country': country,
        }
        applicant_html = render_to_string('website/emails/applicant_email.html', applicant_context)
        applicant_text = f"Dear {name},\n\nThank you for contacting Blue Dot. We have received your enquiry regarding {service} and will get back to you shortly.\n\nBest regards,\nBlue Dot Team"
        
        try:
            mail_applicant = EmailMultiAlternatives(
                subject=applicant_subject,
                body=applicant_text,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[email]
            )
            mail_applicant.attach_alternative(applicant_html, "text/html")
            mail_applicant.mixed_subtype = 'related'  # Set subtype to 'related' so inline attachments show up correctly!
            
            # Attach logo
            logo_path = os.path.join(settings.BASE_DIR, 'static', 'website', 'images', 'bl-logo.png')
            if os.path.exists(logo_path):
                with open(logo_path, 'rb') as f:
                    logo_data = f.read()
                mime_image = MIMEImage(logo_data)
                mime_image.add_header('Content-ID', '<bluedot_logo>')
                mime_image.add_header('Content-Disposition', 'inline', filename='bl-logo.png')
                mail_applicant.attach(mime_image)
                
            mail_applicant.send()
        except Exception:
            pass

        # Clear session verification flags after successful submit
        request.session['email_verified'] = False
        request.session['verified_email'] = None
        request.session.modified = True

        return JsonResponse({'status': 'success', 'redirect_url': '/thank-you/'})