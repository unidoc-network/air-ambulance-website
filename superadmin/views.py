# Standard library imports
from typing import Any, Dict
from django.db import connections
from django.db.models import Max, Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.template import loader
from django.template.loader import render_to_string
from django.views import View

# Django authentication and mixins
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import check_password
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

# Local app imports
from superadmin.helper import is_ajax, renderhelper
from superadmin.models import ContactForm, Blogs, BlogCategory, Career, CareerApplication

COUNTRIES = [
    "Afghanistan", "Albania", "Algeria", "Andorra", "Angola", "Antigua and Barbuda", "Argentina", "Armenia", "Australia", "Austria", "Azerbaijan",
    "Bahamas", "Bahrain", "Bangladesh", "Barbados", "Belarus", "Belgium", "Belize", "Benin", "Bhutan", "Bolivia", "Bosnia and Herzegovina", "Botswana", "Brazil", "Brunei", "Bulgaria", "Burkina Faso", "Burundi",
    "Cote d'Ivoire", "Cabo Verde", "Cambodia", "Cameroon", "Canada", "Central African Republic", "Chad", "Chile", "China", "Colombia", "Comoros", "Congo (Congo-Brazzaville)", "Costa Rica", "Croatia", "Cuba", "Cyprus", "Czechia (Czech Republic)",
    "Democratic Republic of the Congo", "Denmark", "Djibouti", "Dominica", "Dominican Republic",
    "Ecuador", "Egypt", "El Salvador", "Equatorial Guinea", "Eritrea", "Estonia", "Eswatini (fmr. Swaziland)", "Ethiopia",
    "Fiji", "Finland", "France",
    "Gabon", "Gambia", "Georgia", "Germany", "Ghana", "Greece", "Grenada", "Guatemala", "Guinea", "Guinea-Bissau", "Guyana",
    "Haiti", "Holy See", "Honduras", "Hungary",
    "Iceland", "India", "Indonesia", "Iran", "Iraq", "Ireland", "Israel", "Italy",
    "Jamaica", "Japan", "Jordan",
    "Kazakhstan", "Kenya", "Kiribati", "Kuwait", "Kyrgyzstan",
    "Laos", "Latvia", "Lebanon", "Lesotho", "Liberia", "Libya", "Liechtenstein", "Lithuania", "Luxembourg",
    "Madagascar", "Malawi", "Malaysia", "Maldives", "Mali", "Malta", "Marshall Islands", "Mauritania", "Mauritius", "Mexico", "Micronesia", "Moldova", "Monaco", "Mongolia", "Montenegro", "Morocco", "Mozambique", "Myanmar (formerly Burma)",
    "Namibia", "Nauru", "Nepal", "Netherlands", "New Zealand", "Nicaragua", "Niger", "Nigeria", "North Korea", "North Macedonia", "Norway",
    "Oman",
    "Pakistan", "Palau", "Palestine State", "Panama", "Papua New Guinea", "Paraguay", "Peru", "Philippines", "Poland", "Portugal",
    "Qatar",
    "Romania", "Russia", "Rwanda",
    "Saint Kitts and Nevis", "Saint Lucia", "Saint Vincent and the Grenadines", "Samoa", "San Marino", "Sao Tome and Principe", "Saudi Arabia", "Senegal", "Serbia", "Seychelles", "Sierra Leone", "Singapore", "Slovakia", "Slovenia", "Solomon Islands", "Somalia", "South Africa", "South Korea", "South Sudan", "Spain", "Sri Lanka", "Sudan", "Suriname", "Sweden", "Switzerland", "Syria",
    "Tajikistan", "Tanzania", "Thailand", "Timor-Leste", "Togo", "Tonga", "Trinidad and Tobago", "Tunisia", "Turkey", "Turkmenistan", "Tuvalu",
    "Uganda", "Ukraine", "United Arab Emirates", "United Kingdom", "United States of America", "Uruguay", "Uzbekistan",
    "Vanuatu", "Venezuela", "Vietnam",
    "Yemen",
    "Zambia", "Zimbabwe"
]


class LoginPageView(View):
    context={}
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('superadmin:Dashboard')
        else:
            return renderhelper(request,'login','login',self.context)
        
    def post(self, request):
        email = request.POST.get('email', '').lower().strip()
        password = request.POST.get('password', '').strip()
        print(f"DEBUG: Receiving login attempt. Email='{email}', Password='{password}'")

        try:
            user_obj = User.objects.get(email=email)
            user = authenticate(username=user_obj.username, password=password)
            if user is not None and user.is_active:
                login(request, user)
                return redirect('superadmin:Dashboard')
            else:
                messages.info(request, 'Username or Password is Incorrect')
        except User.DoesNotExist:
            messages.info(request, f"Email not found! Tried to search for '{email}'")

        return renderhelper(request, 'login', 'login', self.context)

class Logout(LoginRequiredMixin,View):
    context={}
    def get(self, request):
        logout(request)
        return redirect('superadmin:login')


class Dashboard(LoginRequiredMixin,View):
    login_url = 'superadmin:login'
    def get(self, request):
        context={}
        path="dashboard"
        contact_count = ContactForm.objects.filter(is_active=True).count()
        news_count = Blogs.objects.filter(is_active=True).count()
        category_count = BlogCategory.objects.filter(is_active=True).count()
        career_count = Career.objects.filter(is_active=True).count()
        application_count = CareerApplication.objects.count()

        context["path"] = path
        context["contact_count"] = contact_count
        context["news_count"] = news_count
        context["category_count"] = category_count
        context["career_count"] = career_count
        context["application_count"] = application_count
    
        return renderhelper(request,'layout','index',context)

class Profile(LoginRequiredMixin,View):
    login_url = 'superadmin:login'
    def get(self, request):
        return renderhelper(request, 'layout', 'profile', {'path': 'profile'})

    def post(self, request):
        password_to_check = request.POST['oldpassword']
        newpassword = request.POST['newpassword']
        conpassword = request.POST['conpassword']
        password_matches = check_password(password_to_check, request.user.password)
        if password_matches:
            if newpassword == conpassword:
                user =User.objects.get(id=request.user.id)
                new_password = conpassword  # Replace 'new_password' with the new password
                user.set_password(new_password)
                user.save()
                login(request, user)
                messages.info(request, 'Password changed')
                return renderhelper(request, 'layout', 'profile', {'path': 'profile'})
            else:
                messages.info(request, 'new password not matching')
                context = {'oldpass': password_to_check, 'newpassword': newpassword, 'conpassword': conpassword}
                return renderhelper(request, 'layout', 'profile', context)

        else:
            messages.info(request, 'Your old password is incorrect')
            context = {'oldpass': password_to_check,'newpassword':newpassword,'conpassword':conpassword}
            return renderhelper(request, 'layout', 'profile', context)




# Removed Gallery, Testimonial, and Team views


# ─── Contact Messages Module ────────────────────────────────────────────────

class ContactList(LoginRequiredMixin, View):
    login_url = '/'
    def get(self, request):
        from django.utils import timezone
        import datetime
        qs = ContactForm.objects.all().order_by('-created_at')

        # Search
        search = request.GET.get('search', '').strip()
        if search:
            qs = qs.filter(
                Q(name__icontains=search) |
                Q(email__icontains=search) |
                Q(phone__icontains=search) |
                Q(country_code__icontains=search)
            )

        # Source filter
        source = request.GET.get('source', '').strip()
        if source:
            if source.lower() == 'baharain' or source.lower() == 'bahrain':
                qs = qs.filter(Q(country__iexact='Bahrain') | Q(country__iexact='Baharain'))
            elif source.lower() == 'saudi':
                qs = qs.filter(country__icontains='Saudi')
            else:
                qs = qs.filter(country__iexact=source)

        # Date filter
        date_filter = request.GET.get('date_filter', '')
        now = timezone.now()
        if date_filter == 'today':
            qs = qs.filter(created_at__date=now.date())
        elif date_filter == 'week':
            week_start = now - datetime.timedelta(days=now.weekday())
            qs = qs.filter(created_at__gte=week_start.replace(hour=0, minute=0, second=0))
        elif date_filter == 'month':
            qs = qs.filter(created_at__year=now.year, created_at__month=now.month)

        # Pagination
        paginator = Paginator(qs, 15)
        page = request.GET.get('page', 1)
        try:
            datas = paginator.page(page)
        except (PageNotAnInteger, EmptyPage):
            datas = paginator.page(1)
            
        context = {
            'datas': datas,
            'search': search,
            'date_filter': date_filter,
            'source': source,
            'page': page,
            'path': 'contact',
        }

        if is_ajax(request):
            template = loader.get_template('superadmin/contact/contact-table.html')
            return JsonResponse({'status': True, 'template': template.render(context, request)})

        return renderhelper(request, 'contact', 'contact-list', context)


class ContactDelete(LoginRequiredMixin, View):
    login_url = '/'
    def get(self, request, id):
        try:
            ContactForm.objects.get(id=id).delete()
            messages.success(request, "Contact message deleted successfully.")
        except ContactForm.DoesNotExist:
            messages.error(request, "Message not found.")
        return redirect('superadmin:ContactList')


# Blog Categories
class CategoryList(LoginRequiredMixin, View):
    def get(self, request):
        context = {}
        context['path'] = "blog_category"
        conditions = Q()

        search = request.GET.get('search')
        status = request.GET.get('status', 'True')
        page_num = request.GET.get('page', 1)

        if is_ajax(request):
            type = request.GET.get('type')
            if type == '1':
                id = request.GET.get('id')
                vl = request.GET.get('vl')
                try:
                    obj = BlogCategory.objects.get(id=id)
                    obj.is_active = (vl != '2')
                    obj.save()
                    messages.info(request, 'Successfully Updated')
                except BlogCategory.DoesNotExist:
                    pass
            elif type == '2':
                id = request.GET.get('id')
                BlogCategory.objects.filter(id=id).delete()
                messages.info(request, 'Successfully Deleted')

        if search:
            conditions &= Q(name__icontains=search)
        if status:
            conditions &= Q(is_active=(status == 'True'))
        elif not search and not request.GET.get('page'):
            conditions &= Q(is_active=True)

        data_list = BlogCategory.objects.filter(conditions).order_by('-id')
        paginator = Paginator(data_list, 15)

        try:
            datas = paginator.page(page_num)
        except (PageNotAnInteger, EmptyPage):
            datas = paginator.page(1)
        
        context.update({
            'datas': datas,
            'page': page_num,
        })

        if is_ajax(request):
            template = loader.get_template('superadmin/blogs/category-table.html')
            html_content = template.render(context, request)
            return JsonResponse({'status': True, 'template': html_content})

        return renderhelper(request, 'blogs', 'category-view', context)


class CategoryAdd(LoginRequiredMixin, View):
    def get(self, request, id=None):
        context = {}
        context['path'] = "blog_category"
        if id:
            try:
                context['data'] = BlogCategory.objects.get(id=id)
            except BlogCategory.DoesNotExist:
                context['data'] = None
        else:
            context['data'] = None

        return renderhelper(request, 'blogs', 'category-create', context)

    def post(self, request, id=None):
        try:
            if id:
                try:
                    data = BlogCategory.objects.get(id=id)
                    messages.info(request, 'Category Successfully Updated')
                except BlogCategory.DoesNotExist:
                    data = BlogCategory()
                    messages.info(request, 'Category Successfully Added')
            else:
                data = BlogCategory()
                messages.info(request, 'Category Successfully Added')

            data.name = request.POST.get('name')
            data.name_ar = request.POST.get('name_ar')
            data.save()
            return redirect('superadmin:CategoryList')
        except Exception as e:
            messages.error(request, f"An error occurred: {e}")
            return redirect('superadmin:CategoryList')


# News & Stories
class NewsList(LoginRequiredMixin, View):
    def get(self, request):
        context = {}
        context['path'] = "blogs"
        conditions = Q()

        search = request.GET.get('search')
        status = request.GET.get('status', 'True')
        category = request.GET.get('category')
        page_num = request.GET.get('page', 1)

        if is_ajax(request):
            type = request.GET.get('type')
            if type == '1':
                id = request.GET.get('id')
                vl = request.GET.get('vl')
                try:
                    obj = Blogs.objects.get(id=id)
                    obj.is_active = (vl != '2')
                    obj.save()
                    messages.info(request, 'Successfully Updated')
                except Blogs.DoesNotExist:
                    pass
            elif type == '2':
                id = request.GET.get('id')
                Blogs.objects.filter(id=id).delete()
                messages.info(request, 'Successfully Deleted')

        if search:
            conditions &= Q(title__icontains=search) | Q(content__icontains=search) | Q(tag__icontains=search) | Q(category__name__icontains=search)
        if status:
            conditions &= Q(is_active=(status == 'True'))
        elif not search and not request.GET.get('page'):
            conditions &= Q(is_active=True)

        if category:
            conditions &= Q(category_id=category)

        data_list = Blogs.objects.filter(conditions).order_by('sequence', '-id')
        paginator = Paginator(data_list, 15)

        try:
            datas = paginator.page(page_num)
        except (PageNotAnInteger, EmptyPage):
            datas = paginator.page(1)
        
        total_blogs = Blogs.objects.count()
        
        context.update({
            'datas': datas,
            'page': page_num,
            'categories': BlogCategory.objects.filter(is_active=True),
            'selected_category': category,
            'total_blogs_range': list(range(1, total_blogs + 1)) if total_blogs > 0 else [],
        })

        if is_ajax(request):
            template = loader.get_template('superadmin/blogs/blog-table.html')
            html_content = template.render(context, request)
            return JsonResponse({'status': True, 'template': html_content})

        return renderhelper(request, 'blogs', 'blog-view', context)

class UpdateBlogSequence(LoginRequiredMixin, View):
    def post(self, request):
        try:
            blog_id = request.POST.get('id')
            sequence = int(request.POST.get('sequence'))
            blog = Blogs.objects.get(id=blog_id)
            blog.sequence = sequence
            blog.save()
            messages.info(request, 'Sequence updated successfully.')
            return JsonResponse({'status': True, 'message': 'Sequence updated successfully.'})
        except Exception as e:
            return JsonResponse({'status': False, 'message': str(e)})


class NewsAdd(LoginRequiredMixin, View):
    def get(self, request, id=None):
        context = {}
        context['path'] = "blogs"
        context['categories'] = BlogCategory.objects.filter(is_active=True)
        if id:
            try:
                context['data'] = Blogs.objects.get(id=id)
            except Blogs.DoesNotExist:
                context['data'] = None
        else:
            context['data'] = None

        return renderhelper(request, 'blogs', 'blog-create', context)

    def post(self, request, id=None):
        try:
            if id:
                try:
                    data = Blogs.objects.get(id=id)
                    messages.info(request, 'News & Story Successfully Updated')
                except Blogs.DoesNotExist:
                    data = Blogs()
                    messages.info(request, 'News & Story Successfully Added')
            else:
                data = Blogs()
                messages.info(request, 'News & Story Successfully Added')

            data.title = request.POST.get('title')
            data.title_ar = request.POST.get('title_ar')
            data.date = request.POST.get('date')
            data.content = request.POST.get('content')
            data.content_ar = request.POST.get('content_ar')
            data.time_to_read = request.POST.get('time_to_read') or None
            data.time_to_read_ar = request.POST.get('time_to_read_ar') or None
            data.tag = request.POST.get('tag')
            data.meta_title = request.POST.get('meta_title')
            data.meta_description = request.POST.get('meta_description')

            category_id = request.POST.get('category')
            if category_id:
                data.category = BlogCategory.objects.get(id=category_id)
            else:
                data.category = None

            image = request.FILES.get('image')
            if image:
                data.image = image

            data.save()
            return redirect('superadmin:NewsList')
        except Exception as e:
            messages.error(request, f"An error occurred: {e}")
            return redirect('superadmin:NewsList')


# Removed GlobalStats views

# Careers
class CareerList(LoginRequiredMixin, View):
    def get(self, request):
        context = {}
        context['path'] = "career"
        conditions = Q()
        
        search = request.GET.get('search', '').strip()
        status = request.GET.get('status', 'True').strip()
        page_num = request.GET.get('page', 1)

        if search:
            conditions &= Q(title__icontains=search) | Q(location__icontains=search)
        if status:
            conditions &= Q(is_active=(status == 'True'))

        career_qs = Career.objects.filter(conditions).order_by('-id')
        paginator = Paginator(career_qs, 15)
        
        try:
            datas = paginator.page(page_num)
        except (PageNotAnInteger, EmptyPage):
            datas = paginator.page(1)
            
        context['careers'] = datas
        context['search'] = search
        context['status'] = status

        if is_ajax(request):
            template = loader.get_template('superadmin/career/career-table.html')
            return JsonResponse({'status': True, 'template': template.render(context, request)})

        return renderhelper(request, 'career', 'career-view', context)

class CareerAdd(LoginRequiredMixin, View):
    def get(self, request, id=None):
        context = {}
        context['path'] = "career"
        if id:
            context['data'] = get_object_or_404(Career, id=id)
        return renderhelper(request, 'career', 'career-create', context)

    def post(self, request, id=None):
        try:
            if id:
                data = get_object_or_404(Career, id=id)
            else:
                data = Career()

            data.title = request.POST.get('title')
            data.title_ar = request.POST.get('title_ar')
            data.location = request.POST.get('location')
            data.location_ar = request.POST.get('location_ar')
            data.date = request.POST.get('date') if request.POST.get('date') else None
            data.listing_description = request.POST.get('listing_description')
            data.listing_description_ar = request.POST.get('listing_description_ar')
            data.description = request.POST.get('description')
            data.description_ar = request.POST.get('description_ar')
            if not id:
                data.is_active = True

            data.save()
            messages.info(request, 'Career Successfully Saved')
            return redirect('superadmin:CareerList')
        except Exception as e:
            messages.error(request, f"An error occurred: {e}")
            return redirect('superadmin:CareerList')

class CareerDetail(LoginRequiredMixin, View):
    def get(self, request):
        try:
            id = request.GET.get('id')
            career = Career.objects.get(id=id)
            context = {
                'career': career,
            }
            template_name = 'superadmin/career/career-detail-modal-content.html'
            html_content = render_to_string(template_name, context, request)
            return JsonResponse({'status': True, 'template': html_content})
        except Career.DoesNotExist:
            return JsonResponse({'status': False, 'message': 'Career not found'})
        except Exception as e:
            return JsonResponse({'status': False, 'message': str(e)})


class CareerArabicDetail(LoginRequiredMixin, View):
    def get(self, request):
        try:
            id = request.GET.get('id')
            career = Career.objects.get(id=id)
            context = {
                'career': career,
            }
            template_name = 'superadmin/career/career-arabic-modal-content.html'
            html_content = render_to_string(template_name, context, request)
            return JsonResponse({'status': True, 'template': html_content})
        except Career.DoesNotExist:
            return JsonResponse({'status': False, 'message': 'Career not found'})
        except Exception as e:
            return JsonResponse({'status': False, 'message': str(e)})

class CareerStatus(LoginRequiredMixin, View):
    def post(self, request):
        try:
            id = request.POST.get('id')
            data = Career.objects.get(id=id)
            data.is_active = not data.is_active
            data.save()
            return JsonResponse({'status': True})
        except:
            return JsonResponse({'status': False})

class CareerDelete(LoginRequiredMixin, View):
    def post(self, request):
        try:
            id = request.POST.get('id')
            Career.objects.get(id=id).delete()
            return JsonResponse({'status': True})
        except:
            return JsonResponse({'status': False})

# Career Applications
class CareerApplicationList(LoginRequiredMixin, View):
    def get(self, request):
        context = {}
        context['path'] = "career_application"
        conditions = Q()
        
        search = request.GET.get('search', '').strip()
        career = request.GET.get('career', '').strip()
        page_num = request.GET.get('page', 1)

        if search:
            conditions &= Q(name__icontains=search) | Q(email__icontains=search) | Q(career__title__icontains=search) | Q(location__icontains=search) | Q(phone__icontains=search) | Q(country_code__icontains=search)
        
        if career:
            conditions &= Q(career_id=career)

        application_qs = CareerApplication.objects.filter(conditions).order_by('-id')
        paginator = Paginator(application_qs, 15)
        
        try:
            datas = paginator.page(page_num)
        except (PageNotAnInteger, EmptyPage):
            datas = paginator.page(1)
            
        context['applications'] = datas
        context['search'] = search
        context['careers'] = Career.objects.filter(is_active=True)
        context['selected_career'] = career

        if is_ajax(request):
            template = loader.get_template('superadmin/career/application-table.html')
            return JsonResponse({'status': True, 'template': template.render(context, request)})

        return renderhelper(request, 'career', 'application-view', context)

class CareerApplicationDelete(LoginRequiredMixin, View):
    def post(self, request):
        try:
            id = request.POST.get('id')
            CareerApplication.objects.get(id=id).delete()
            return JsonResponse({'status': True})
        except:
            return JsonResponse({'status': False})
