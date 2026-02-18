import datetime

def generate_monitor_svg():
    width = 800
    height = 500
    
    # Palette: Dark Professional
    bg_color = "#000000"
    monitor_frame = "#161b22"
    screen_bg = "#0d1117"
    screen_border = "#30363d"
    text_color = "#c9d1d9"
    cmd_color = "#58a6ff"
    success_color = "#3fb950"
    error_color = "#ff5f56"
    warning_color = "#d29922"
    
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    
    svg = f'<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">\n'
    
    # MONITOR STAND
    svg += f'<rect x="{width/2 - 60}" y="{height - 50}" width="120" height="50" fill="{monitor_frame}" rx="5" />\n'
    svg += f'<path d="M{width/2 - 20} {height - 50} L{width/2 - 20} {height - 120} L{width/2 + 20} {height - 120} L{width/2 + 20} {height - 50} Z" fill="{monitor_frame}" />\n'
    
    # MONITOR FRAME
    svg += f'<rect x="25" y="25" width="{width-50}" height="{height-140}" fill="{monitor_frame}" rx="15" />\n'
    
    # SCREEN AREA (Inner Bezel)
    screen_width = width - 80
    screen_height = height - 170
    start_x = 40
    start_y = 40
    
    svg += f'<rect x="{start_x}" y="{start_y}" width="{screen_width}" height="{screen_height}" fill="{screen_bg}" stroke="{screen_border}" stroke-width="2" />\n'
    
    # WINDOW TITLE BAR
    svg += f'<rect x="{start_x}" y="{start_y}" width="{screen_width}" height="30" fill="{screen_border}" />\n'
    svg += f'<circle cx="{start_x + 20}" cy="{start_y + 15}" r="6" fill="#ff5f56" />\n'
    svg += f'<circle cx="{start_x + 40}" cy="{start_y + 15}" r="6" fill="#ffbd2e" />\n'
    svg += f'<circle cx="{start_x + 60}" cy="{start_y + 15}" r="6" fill="#27c93f" />\n'
    svg += f'<text x="{width/2}" y="{start_y + 20}" font-family="monospace" font-size="12" fill="{text_color}" text-anchor="middle">root@freakyyirus: ~</text>\n'
    
    # TERMINAL CONTENT
    term_x = start_x + 20
    term_y = start_y + 60
    line_height = 25
    
    # Command list with (Prompt?, Text, ColorOverride?, DelaySec)
    sequence = [
        (True, 'npm install alive-baddies', None, 0),
        (False, '[INFO] Fetching packages from registry...', None, 1.5),
        (False, '[INFO] Verifying integrity...', None, 2.5),
        (False, '[SUCCESS] Installed "alive-baddies" v1.0.0 🔥', success_color, 3.5),
        (True, 'git commit -m "Legacy code deleted"', None, 5.0),
        (False, '[main 8f3a1b] Legacy code deleted', None, 6.0),
        (False, ' 1 file changed, 1024 deletions(-)', warning_color, 6.5),
        (True, 'deploy --target=production --force', None, 8.0),
        (False, '🚀 Deploying to edge network...', None, 9.0),
        (False, '✔ Build completed in 420ms', success_color, 10.5),
        (False, '✔ Uploading assets...', success_color, 11.0),
        (False, '✨ Deployed successfully to https://freakyyirus.dev', success_color, 12.0),
        (True, '', None, 13.0) # Empty prompt at the end
    ]
    
    for i, (is_prompt, text, color, delay) in enumerate(sequence):
        y_pos = term_y + (i * line_height)
        line_color = color if color else text_color
        
        # Group for animation
        svg += f'<g opacity="0">\n'
        
        if is_prompt:
            svg += f'  <text x="{term_x}" y="{y_pos}" font-family="monospace" font-weight="bold" font-size="14" fill="{text_color}">'
            svg += f'<tspan fill="{success_color}">➜</tspan> <tspan fill="{cmd_color}">~</tspan> '
            if text:
                svg += f'{text}'
            else:
                # Blinking cursor for the last empty prompt
                svg += f'<tspan fill="{text_color}"><animate attributeName="opacity" values="1;0;1" dur="1s" repeatCount="indefinite">_</animate></tspan>'
            svg += f'</text>\n'
        else:
            svg += f'  <text x="{term_x}" y="{y_pos}" font-family="monospace" font-size="14" fill="{line_color}">{text}</text>\n'
            
        # Animation: Fade in instantly at delay time
        svg += f'  <animate attributeName="opacity" from="0" to="1" begin="{delay}s" dur="0.1s" fill="freeze" />\n'
        svg += f'</g>\n'

    # GLOSS/REFLECTION
    svg += f'<path d="M{start_x} {start_y} L{start_x + screen_width} {start_y} L{start_x + screen_width} {start_y + screen_height} Z" fill="white" opacity="0.03" pointer-events="none" />\n'
    
    svg += '</svg>'
    return svg

import os

if __name__ == "__main__":
    output_dir = "assets"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    svg_content = generate_monitor_svg()
    
    with open(f"{output_dir}/omni-monitor.svg", "w", encoding="utf-8") as f:
        f.write(svg_content)
        
    print(f"Generated animated omni-monitor.svg in {output_dir}")
