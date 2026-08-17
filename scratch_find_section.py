import os
import glob
import re

base_dir = '/Users/thahir/Documents/bludont-py/Bluedot/templates/website'
files = glob.glob(base_dir + '/**/*.html', recursive=True)

# Skip certain directories
skip_dirs = ['/home/', '/layout/', '/emails/', '/error_404.html', 'thankyou', '/news/']
# Wait, news details can have breadcrumbs. I'll include them.

for file in files:
    skip = False
    for d in skip_dirs:
        if d in file:
            skip = True
    if skip:
        continue
        
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find the first </section> tag
    match = re.search(r'</section>', content, re.IGNORECASE)
    if match:
        end_pos = match.end()
        print(f"File: {os.path.relpath(file, base_dir)} - First section ends at index {end_pos}")
    else:
        print(f"File: {os.path.relpath(file, base_dir)} - NO SECTION FOUND")
