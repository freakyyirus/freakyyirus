import os
import urllib.parse

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
GALLERY_DIR = os.path.join(REPO_ROOT, 'Gallery')
README_PATH = os.path.join(REPO_ROOT, 'README.md')

START_MARKER = '<!-- GALLERY-START -->'
END_MARKER = '<!-- GALLERY-END -->'

def build_gallery_html(files):
    parts = ['<div align="center">']
    
    # Configuration
    MAX_ITEMS = 7
    total_files = len(files)
    display_files = files[:MAX_ITEMS]
    
    # Base URL for Raw content on GitHub to improve video playback reliably
    RAW_BASE_URL = "https://raw.githubusercontent.com/freakyyirus/freakyyirus/main/"
    
    for fn in display_files:
        if fn.startswith('.'):
            continue
            
        # Use relative path for images (works fine), but absolute raw for videos
        rel_src = 'Gallery/' + urllib.parse.quote(fn)
        abs_src = RAW_BASE_URL + rel_src
        
        caption = os.path.splitext(fn)[0].replace('-', ' ').replace('_', ' ')
        
        ext = os.path.splitext(fn)[1].lower()
        if ext in ['.mp4', '.webm', '.ogg', '.mov']:
            # Using absolute raw URL for videos to help with Autoplay/Loop
            media_tag = f'<video src="{abs_src}" width="130" height="130" style="border-radius:10px; object-fit: cover;" autoplay loop muted playsinline aria-label="{caption}"></video>'
        else:
            # Images work well with relative paths
            media_tag = f'<img src="{rel_src}" alt="{caption}" width="130" height="130" style="border-radius:10px; object-fit: cover;" />'
            
        item = (
            '  <figure style="display:inline-block; margin:5px; text-align:center; vertical-align: top;">\n'
            f'    {media_tag}\n'
            '  </figure>'
        )
        parts.append(item)
        
    if total_files > MAX_ITEMS:
        remaining = total_files - MAX_ITEMS
        view_more_url = f"https://placehold.co/130x130/161b22/58a6ff?text=%2B{remaining}%0AView%20More"
        view_more_item = (
            '  <figure style="display:inline-block; margin:5px; text-align:center; vertical-align: top;">\n'
            f'    <a href="https://github.com/freakyyirus/freakyyirus/tree/main/Gallery">\n'
                f'      <img src="{view_more_url}" alt="View {remaining} more" width="130" height="130" style="border-radius:10px; border: 1px solid #30363d;" />\n'
            f'    </a>\n'
            '  </figure>'
        )
        parts.append(view_more_item)
        
    parts.append('</div>')
    return '\n\n'.join(parts)

def main():
    if not os.path.exists(GALLERY_DIR):
        print('Gallery folder not found:', GALLERY_DIR)
        return

    # Sort files by modification time (newest first)
    files = [f for f in os.listdir(GALLERY_DIR) if not f.startswith('.')]
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
