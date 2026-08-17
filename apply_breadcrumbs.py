import os
import glob
import re

base_dir = '/Users/thahir/Documents/bludont-py/Bluedot/templates/website'
files = glob.glob(base_dir + '/**/*.html', recursive=True)

skip_dirs = ['/home/', '/layout/', '/emails/', 'error_404.html', 'thankyou', '/news/_news_grid.html', '/fleet/select.html']

translations = {
    'about': ('About Us', 'معلومات عنا'),
    'contact': ('Contact Us', 'اتصل بنا'),
    'services': ('Services', 'الخدمات'),
    'regions': ('Regions', 'المناطق'),
    'fleet': ('Fleet', 'الأسطول'),
    'leadership': ('Leadership', 'القيادة'),
    'news': ('News', 'الأخبار'),
    'legal': ('Legal', 'قانوني'),
    'careers': ('Careers', 'الوظائف'),
    'oman': ('Oman', 'عمان'),
    'bahrain': ('Bahrain', 'البحرين'),
    'qatar': ('Qatar', 'قطر'),
    'kuwait': ('Kuwait', 'الكويت'),
    'saudi-arabia': ('Saudi Arabia', 'المملكة العربية السعودية'),
    'air-ambulance': ('Air Ambulance', 'الإسعاف الجوي'),
    'medical-escort': ('Medical Escort', 'المرافقة الطبية'),
    'helicopter-air-ambulance': ('Helicopter Air Ambulance', 'هليكوبتر الإسعاف الجوي'),
    'commercial-airline-transfer': ('Commercial Airline Transfer', 'النقل عبر الخطوط التجارية'),
    'privacy-policy': ('Privacy Policy', 'سياسة الخصوصية'),
    'terms-and-condition': ('Terms & Conditions', 'الشروط والأحكام')
}

css_code = """
/* Hero Breadcrumb Styles */
.hero-breadcrumb {
    color: rgba(255, 255, 255, 0.8);
    font-size: 14px;
    margin-bottom: 15px;
    font-weight: 500;
}
.hero-breadcrumb a {
    color: rgba(255, 255, 255, 0.8);
    text-decoration: none;
    transition: color 0.3s ease;
}
.hero-breadcrumb a:hover {
    color: #fff;
}
.hero-breadcrumb span.separator {
    margin: 0 8px;
    color: rgba(255, 255, 255, 0.5);
}
.hero-breadcrumb .active {
    color: #fff;
}
"""

css_file = '/Users/thahir/Documents/bludont-py/Bluedot/static/website/css/style.css'
with open(css_file, 'r', encoding='utf-8') as f:
    css_content = f.read()

if '/* Hero Breadcrumb Styles */' not in css_content:
    with open(css_file, 'a', encoding='utf-8') as f:
        f.write(css_code)
    print("Added Hero Breadcrumb CSS.")

for file in files:
    skip = False
    for d in skip_dirs:
        if d in file:
            skip = True
    if skip:
        continue
        
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if '<div class="hero-breadcrumb">' in content:
        print(f"Skipping {file} - Breadcrumbs already exist")
        continue

    # Generate Breadcrumb HTML
    rel_path = os.path.relpath(file, base_dir)
    parts = rel_path.replace('.html', '').split('/')
    
    bc_html = """
<div class="hero-breadcrumb">
    <span class="en-content">
        <a href="{% url 'website:home' %}">Home</a>"""
    
    bc_html_ar = """
    <span class="ar-content">
        <a href="{% url 'website:home' %}">الرئيسية</a>"""
    
    for i, p in enumerate(parts):
        if p == 'index':
            continue
            
        en_text, ar_text = translations.get(p, (p.replace('-', ' ').title(), p.replace('-', ' ').title()))
        
        is_last = (i == len(parts) - 1) or (i == len(parts) - 2 and parts[i+1] == 'index')
        
        if is_last:
            bc_html += f"""
        <span class="separator">/</span>
        <span class="active">{en_text}</span>"""
            bc_html_ar += f"""
        <span class="separator">/</span>
        <span class="active">{ar_text}</span>"""
        else:
            bc_html += f"""
        <span class="separator">/</span>
        <a href="#">{en_text}</a>"""
            bc_html_ar += f"""
        <span class="separator">/</span>
        <a href="#">{ar_text}</a>"""
                
    bc_html += """
    </span>"""
    bc_html_ar += """
    </span>
</div>"""
    
    full_bc_html = bc_html + bc_html_ar

    # Strategy: Find first <section...>, then inside that section, find first <div class="container...">
    section_match = re.search(r'<section[^>]*>', content, re.IGNORECASE)
    if section_match:
        # Search for first container AFTER section starts
        # actually, just find the first <div class="container... in the whole file is usually correct
        # but let's be safe and search from section start
        container_match = re.search(r'<div[^>]*class="container[^"]*"[^>]*>', content[section_match.start():], re.IGNORECASE)
        if container_match:
            insert_pos = section_match.start() + container_match.end()
            new_content = content[:insert_pos] + full_bc_html + content[insert_pos:]
            with open(file, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Updated {rel_path}")
        else:
            print(f"WARNING: No container found inside section in {rel_path}")
    else:
        print(f"WARNING: No <section> found in {rel_path}")
