import os
import re
from datetime import datetime
from difflib import SequenceMatcher
from django.core.files import File
from superadmin.models import Blogs, BlogCategory
from numbers_parser import Document

print("Starting import from Numbers file...")

# 1. Category
category, _ = BlogCategory.objects.get_or_create(name='News')

# 2. Read Numbers
# UPDATE THESE PATHS WHEN RUNNING ON LIVE SERVER
NUMBERS_PATH = '/Users/jaseemrahman/Documents/Projects/Blue Dot/bluedot/Bluedot_Blogs_edited.numbers'
IMAGES_DIR = '/Users/jaseemrahman/Documents/Projects/Blue Dot/bluedot/blogimages'

doc = Document(NUMBERS_PATH)
sheets = doc.sheets
tables = sheets[0].tables
rows = tables[0].rows()

# Helper for string similarity
def similarity(a, b):
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()

def clean_text(text):
    if not isinstance(text, str):
        text = str(text)
    # Remove multiple spaces between words
    text = re.sub(r' {2,}', ' ', text)
    return text.strip()

def format_html(text):
    if not text: return ""
    # Split by newlines, ignore empty lines, wrap in <p>
    paragraphs = [p.strip() for p in text.split('\n') if p.strip()]
    return ''.join(f'<p>{p}</p>' for p in paragraphs)

images = [f for f in os.listdir(IMAGES_DIR) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp'))]

count = 0
for idx, row in enumerate(rows):
    # Skip header
    if idx == 0:
        continue
        
    title_cell = row[0].value
    published_cell = row[1].value
    content_cell = row[3].value
    arabic_cell = row[4].value

    title = clean_text(title_cell if title_cell else '')
    if not title:
        continue
        
    if Blogs.objects.filter(title=title).exists():
        print(f"Skipping '{title}' (already exists)")
        continue
        
    # Published date
    published_raw = str(published_cell) if published_cell else ''
    date_obj = None
    if published_raw:
        try:
            # Simple date parsing
            if isinstance(published_cell, datetime):
                date_obj = published_cell.date()
            else:
                date_obj = datetime.strptime(published_raw.split(' ')[0], '%Y-%m-%d').date()
        except:
            pass

    content_en = format_html(content_cell if content_cell else '')
    
    arabic_raw = clean_text(arabic_cell if arabic_cell else '')
    title_ar = ''
    content_ar = ''
    if arabic_raw:
        lines = [line.strip() for line in arabic_raw.split('\n') if line.strip()]
        if len(lines) > 0:
            title_ar = lines[0]
        if len(lines) > 2:
            # Skip index 1 (2nd line), take index 2 onwards
            content_ar = ''.join(f'<p>{p}</p>' for p in lines[2:])
    
    # Create blog
    blog = Blogs(
        category=category,
        title=title,
        title_ar=title_ar,
        date=date_obj,
        content=content_en,
        content_ar=content_ar,
        is_active=False,
        time_to_read="3 min read",
        time_to_read_ar="مدة القراءة: 3 دقائق. "
    )
    blog.save()
    
    # Image Matching
    if images:
        # Find best image match based on similarity to title
        best_image = None
        best_score = -1
        
        # Clean title for matching (remove punctuation, lower)
        match_title = re.sub(r'[^\w\s]', '', title.lower())
        
        for img in images:
            img_name_no_ext = os.path.splitext(img)[0]
            match_img = re.sub(r'[^\w\s]', '', img_name_no_ext.lower().replace('-', ' ').replace('_', ' '))
            score = similarity(match_title, match_img)
            if score > best_score:
                best_score = score
                best_image = img
                
        if best_image:
            img_path = os.path.join(IMAGES_DIR, best_image)
            try:
                with open(img_path, 'rb') as f:
                    blog.image.save(best_image, File(f), save=True)
            except Exception as e:
                print(f"Error saving image {best_image}: {e}")
            
    count += 1
            
print(f"Successfully imported {count} blogs.")
