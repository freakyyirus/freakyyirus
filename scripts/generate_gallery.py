import os
import urllib.parse

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
GALLERY_DIR = os.path.join(REPO_ROOT, 'Gallery')
README_PATH = os.path.join(REPO_ROOT, 'README.md')

START_MARKER = '<!-- GALLERY-START -->'
END_MARKER = '<!-- GALLERY-END -->'

import datetime

def get_file_date(filepath):
    fn = os.path.basename(filepath)
    # Try to extract date from WhatsApp filename format: WhatsApp Image YYYY-MM-DD ...
    try:
        if 'Image ' in fn:
            date_str = fn.split('Image ')[1].split(' at')[0]
            return datetime.datetime.strptime(date_str, '%Y-%m-%d').strftime('%B %d, %Y')
    except Exception:
        pass
    
    # Fallback to modification time
    mtime = os.path.getmtime(filepath)
    return datetime.datetime.fromtimestamp(mtime).strftime('%B %d, %Y')

def build_gallery_html(files_with_paths):
    # Group files by date
    groups = {}
    for fn, path in files_with_paths:
        date = get_file_date(path)
        if date not in groups:
            groups[date] = []
        groups[date].append(fn)
    
    # Sort dates newest first
    sorted_dates = sorted(groups.keys(), key=lambda d: datetime.datetime.strptime(d, '%B %d, %Y'), reverse=True)
    
    final_parts = []
    for date in sorted_dates:
        final_parts.append(f'<h4 align="center">📅 {date}</h4>')
        final_parts.append('<div align="center">')
        
        for fn in groups[date]:
            src = 'Gallery/' + urllib.parse.quote(fn)
            caption = os.path.splitext(fn)[0].replace('-', ' ').replace('_', ' ')
            item = (
                '  <figure style="display:inline-block; margin:5px; text-align:center; vertical-align: bottom;">\n'
                f'    <img src="{src}" alt="{caption}" width="120" style="border-radius:8px;" />\n'
                '  </figure>'
            )
            final_parts.append(item)
            
        final_parts.append('</div>\n<br/>')
        
    return '\n\n'.join(final_parts)

def main():
    if not os.path.exists(GALLERY_DIR):
        print('Gallery folder not found:', GALLERY_DIR)
        return

    # Filter for only image extensions
    valid_exts = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
    all_files = [f for f in os.listdir(GALLERY_DIR) if not f.startswith('.')]
    files = [f for f in all_files if os.path.splitext(f)[1].lower() in valid_exts]
    
    if not files:
        print('No files found in Gallery/. README will keep placeholder.')
        return

    # Create tuples of (filename, absolute_path)
    files_with_paths = [(f, os.path.join(GALLERY_DIR, f)) for f in files]
    
    # Sort files overall by modification time (newest first)
    files_with_paths.sort(key=lambda x: os.path.getmtime(x[1]), reverse=True)

    gallery_html = build_gallery_html(files_with_paths)

    with open(README_PATH, 'r', encoding='utf-8') as f:
        content = f.read()

    if START_MARKER in content and END_MARKER in content:
        before, rest = content.split(START_MARKER, 1)
        _, after = rest.split(END_MARKER, 1)
        new_content = before + START_MARKER + '\n\n' + gallery_html + '\n\n' + END_MARKER + after
        with open(README_PATH, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print('README.md gallery updated with', len(files), 'items.')
    else:
        print('Gallery markers not found in README.md. Add', START_MARKER, 'and', END_MARKER)

if __name__ == '__main__':
    main()
