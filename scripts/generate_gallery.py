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
        item = (
            '  <figure style="display:inline-block; margin:10px; text-align:center;">\n'
            f'    <img src="{src}" alt="{caption}" width="280" style="border-radius:8px;" />\n'
            '  </figure>'
        )
        parts.append(item)
    parts.append('</div>')
    return '\n\n'.join(parts)

def main():
    if not os.path.exists(GALLERY_DIR):
        print('Gallery folder not found:', GALLERY_DIR)
        return

    files = sorted(os.listdir(GALLERY_DIR))
    if not files:
        print('No files found in Gallery/. README will keep placeholder.')

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
