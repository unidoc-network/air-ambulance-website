import os
import glob

base_dir = '/Users/thahir/Documents/bludont-py/Bluedot/templates/website'
files = glob.glob(base_dir + '/**/*.html', recursive=True)

for file in files:
    if '/home/' in file or '/layout/' in file:
        continue
    
    rel_path = os.path.relpath(file, base_dir)
    parts = rel_path.replace('.html', '').split('/')
    
    breadcrumb = ['Home']
    for p in parts:
        if p == 'index':
            continue
        # Title case and replace hyphens
        name = p.replace('-', ' ').title()
        breadcrumb.append(name)
    
    print(f"{rel_path}: {' > '.join(breadcrumb)}")
