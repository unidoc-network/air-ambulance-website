def canonical_url(request):
    # Default global/assistance numbers
    phone_number = "+919745410000"
    mobile_assistance = "+971551881441"
    whatsapp_number = "+971551881441"
    
    # Custom contact info if on Saudi Arabia landing page
    if "air-ambulance-saudi-arabia" in request.path:
        phone_number = "+966538855753"
        mobile_assistance = "+966538855753"
        whatsapp_number = "966538855753"
        
    return {
        "canonical_url": request.build_absolute_uri(request.path),
        "global_phone_number": phone_number,
        "mobile_assistance_number": mobile_assistance,
        "global_whatsapp_number": whatsapp_number,
    }
