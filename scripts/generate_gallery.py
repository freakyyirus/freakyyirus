import os
import urllib.parse

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
GALLERY_DIR = os.path.join(REPO_ROOT, 'Gallery')
README_PATH = os.path.join(REPO_ROOT, 'README.md')

START_MARKER = '<!-- GALLERY-START -->'
END_MARKER = '<!-- GALLERY-END -->'

def build_gallery_html(files):
    parts = ['<div align="center">']
    
    for fn in files:
        if fn.startswith('.'):
            continue
            
        src = 'Gallery/' + urllib.parse.quote(fn)
        caption = os.path.splitext(fn)[0].replace('-', ' ').replace('_', ' ')
        
        # Display images with natural aspect ratio but shrunken width
        # This ensures no part of the image is compromised (no object-fit: cover)
        item = (
            '  <figure style="display:inline-block; margin:5px; text-align:center; vertical-align: bottom;">\n'
            f'    <img src="{src}" alt="{caption}" width="120" style="border-radius:8px;" />\n'
            '  </figure>'
        )
        parts.append(item)
        
    parts.append('</div>')
    return '\n\n'.join(parts)

def main():
    if not os.path.exists(GALLERY_DIR):
        print('Gallery folder not found:', GALLERY_DIR)
        return

    # Sort files by modification time (newest first)
    files = [f for f in os.listdir(GALLERY_DIR) if not f.startswith('.')]
    
    # Filter for only image extensions just in case
    valid_exts = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
    files = [f for f in files if os.path.splitext(f)[1].lower() in valid_exts]
    
    files.sort(key=lambda x: os.path.getmtime(os.path.join(GALLERY_DIR, x)), reverse=True)
    
    if not files:
        print('No files found in Gallery/. README will keep placeholder.')
        return

    gallery_html = build_gallery_html(files)

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
