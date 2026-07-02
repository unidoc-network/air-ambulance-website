from django.urls import path
from website import views
from django.conf.urls import handler404

app_name = 'website'

urlpatterns = [
    # ── Main Pages ────────────────────────────────────────────────────────────
    path('', views.HomePageView.as_view(), name='home'),
    path('about/', views.AboutPageView.as_view(), name='about'),
    path('contact/', views.ContactPageView.as_view(), name='contactus'),
    path('thank-you/', views.ThankYouView.as_view(), name='thankyou'),
    path('coming-soon/', views.ComingSoonPageView.as_view(), name='coming_soon'),

    # ── Legal ─────────────────────────────────────────────────────────────────
    path('privacy-policy/', views.PrivacyPolicyView.as_view(), name='privacy_policy'),
    path('terms-and-conditions/', views.TermsConditionView.as_view(), name='terms_conditions'),

    # ── Leadership ────────────────────────────────────────────────────────────
    path('leadership/<slug:slug>/', views.LeadershipDetailView.as_view(), name='leadership_detail'),

    # ── Blog / News ───────────────────────────────────────────────────────────
    path('blog/', views.BlogListView.as_view(), name='blogs'),
    path('blog/<slug:slug>/', views.BlogDetailPageView.as_view(), name='blog_detail'),

    # ── Careers ───────────────────────────────────────────────────────────────
    path('careers/', views.CareersPageView.as_view(), name='careers'),
    path('careers/<slug:slug>/', views.CareerDetailView.as_view(), name='career_detail'),

    # ── Services ──────────────────────────────────────────────────────────────
    path('air-ambulance/24-7-air-ambulance/', views.ServiceAirAmbulanceView.as_view(), name='service_air_ambulance'),
    path('air-ambulance/commercial-airline-stretcher-service/', views.ServiceCommercialView.as_view(), name='service_commercial'),
    path('air-ambulance/medical-escort/', views.ServiceMedicalEscortView.as_view(), name='service_medical_escort'),
    path('air-ambulance/Rotary-Wing-Services/', views.ServiceHelicopterView.as_view(), name='service_helicopter'),

    # ── Fleet ────────────────────────────────────────────────────────────────
    path('fleet/', views.FleetSelectView.as_view(), name='fleet_select'),
    path('fleet/overview/', views.FleetView.as_view(), name='fleet'),
    path('fleet/challenger-604/', views.FleetChallenger604View.as_view(), name='fleet_challenger604'),
    path('fleet/challenger-605/', views.FleetChallenger605View.as_view(), name='fleet_challenger605'),
    path('fleet/king-air-b200/', views.FleetKingAirB200View.as_view(), name='fleet_kingair_b200'),
    path('fleet/king-air-c90/', views.FleetKingAirC90View.as_view(), name='fleet_kingair_c90'),

    # ── Regions / Landing Pages ───────────────────────────────────────────────
    path('air-ambulance-bahrain/', views.RegionBahrainView.as_view(), name='region_bahrain'),
    path('air-ambulance-oman/', views.RegionOmanView.as_view(), name='region_oman'),
    path('air-ambulance-qatar/', views.RegionQatarView.as_view(), name='region_qatar'),
    path('air-ambulance-saudi-arabia/', views.RegionSaudiView.as_view(), name='region_saudi'),

    # ── OTP & Enquiry Handling ───────────────────────────────────────────────
    path('send-otp/', views.SendOTPView.as_view(), name='send_otp'),
    path('verify-otp/', views.VerifyOTPView.as_view(), name='verify_otp'),
    path('submit-enquiry/', views.SubmitEnquiryView.as_view(), name='submit_enquiry'),
]

handler404 = views.error_404