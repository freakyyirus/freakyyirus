import datetime
import random
import os

def generate_vintage_monitor():
    # 90s Replica Dimensions
    width = 900
    height = 900 
    
    # Palette: 90s PC Beige
    c_light = "#E8E4D9"   # Main Plastic
    c_mid = "#D0CCC0"     # Shadow/Side
    c_dark = "#A8A499"    # Deep Shadow/Vents
    c_screen_border = "#908C85"
    c_screen_bg = "#050505"
    
    # Phosphor
    text_green = "#39ff14"
    text_dim = "#28b410"
    text_amber = "#ffb000"

    svg = f'<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">\n'
    
    # --- DEFS ---
    svg += '<defs>\n'
    svg += '  <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">\n'
    svg += '    <feGaussianBlur stdDeviation="2" result="coloredBlur" />\n'
    svg += '    <feMerge><feMergeNode in="coloredBlur" /><feMergeNode in="SourceGraphic" /></feMerge>\n'
    svg += '  </filter>\n'
    svg += '  <linearGradient id="bezelGradient" x1="0%" y1="0%" x2="100%" y2="100%">\n'
    svg += f'    <stop offset="0%" stop-color="{c_light}" />\n'
    svg += f'    <stop offset="100%" stop-color="{c_mid}" />\n'
    svg += '  </linearGradient>\n'
    svg += '</defs>\n'

    # --- 1. MONITOR STAND ---
    # Base
    svg += f'<path d="M250 850 L650 850 L680 880 L220 880 Z" fill="{c_dark}" />\n'
    svg += f'<path d="M250 840 L650 840 L660 860 L240 860 Z" fill="{c_mid}" />\n'
    # Neck / Swivel
    svg += f'<rect x="350" y="780" width="200" height="70" fill="{c_dark}" />\n'
    svg += f'<path d="M350 780 L550 780 L530 840 L370 840 Z" fill="{c_mid}" />\n'

    # --- 2. MONITOR CHASSIS ---
    # Main Shell (Back)
    svg += f'<rect x="50" y="50" width="800" height="730" rx="20" fill="{c_mid}" />\n'
    
    # Front Bezel (The Face)
    # Beveled effect using path
    svg += f'<rect x="50" y="50" width="800" height="730" rx="20" fill="url(#bezelGradient)" />\n'
    
    # Screen Recession (Inset)
    svg += f'<rect x="100" y="100" width="700" height="550" rx="5" fill="{c_screen_border}" />\n'
    svg += f'<rect x="110" y="110" width="680" height="530" rx="15" fill="#1a1a1a" stroke="#000" stroke-width="2" />\n'
    
    # Actual Screen Area (4:3)
    # x=110, width=680 -> Center roughly
    screen_x = 120
    screen_y = 120
    screen_w = 660
    screen_h = 510
    svg += f'<rect x="{screen_x}" y="{screen_y}" width="{screen_w}" height="{screen_h}" rx="2" fill="{c_screen_bg}" />\n'

    # --- 3. CONTROLS (Bottom Panel) ---
    panel_y = 680
    
    # Vents (Side)
    for i in range(15):
        vy = 150 + i*30
        svg += f'<rect x="60" y="{vy}" width="20" height="10" rx="2" fill="{c_dark}" opacity="0.5" />\n'
        svg += f'<rect x="820" y="{vy}" width="20" height="10" rx="2" fill="{c_dark}" opacity="0.5" />\n'

    # Brand Logo
    svg += f'<text x="450" y="740" font-family="sans-serif" font-weight="bold" font-style="italic" font-size="20" fill="{c_dark}" text-anchor="middle" letter-spacing="2">SyncMaster 9000</text>\n'

    # Buttons
    btn_y = 730
    btn_x_start = 650
    for i in range(4):
        bx = btn_x_start + i*40
        svg += f'<rect x="{bx}" y="{btn_y}" width="30" height="15" rx="2" fill="{c_dark}" />\n' # Button
        svg += f'<rect x="{bx}" y="{btn_y+15}" width="30" height="5" rx="1" fill="{c_mid}" opacity="0.5" />\n' # Shadow

    # Power Button (Big)
    svg += f'<circle cx="150" cy="{btn_y+10}" r="15" fill="{c_mid}" stroke="{c_dark}" stroke-width="2" />\n'
    svg += f'<path d="M150 {btn_y} L150 {btn_y+12}" stroke="{c_dark}" stroke-width="3" />\n'
    svg += f'<circle cx="150" cy="{btn_y+10}" r="8" fill="none" stroke="{c_dark}" stroke-width="3" stroke-dasharray="30 15" transform="rotate(-90 150 {btn_y+10})" />\n'
    
    # Power LED
    svg += f'<circle cx="180" cy="{btn_y+10}" r="4" fill="{text_green}">\n'
    svg += '  <animate attributeName="opacity" values="1;0.4;1" dur="4s" repeatCount="indefinite" />\n'
    svg += '</circle>\n'

    # --- 4. SCREEN CONTENT (The Pulse Loop) ---
    total_dur = 8
    start_x = screen_x + 40
    start_y = screen_y + 50
    line_h = 30
    
    svg += f'<g filter="url(#glow)" font-family="monospace" font-size="20" fill="{text_green}">\n'
    
    # Prompt
    svg += f'<text x="{start_x}" y="{start_y}" fill="{text_dim}">guest@portfolio:~$</text>\n'
    
    # Command
    cmd = "npm install freakyyirus"
    cx = start_x + 220
    for i, char in enumerate(cmd):
        delay = 0.5 + (i * 0.1)
        k1 = delay / total_dur
        k2 = 0.9
        svg += f'<text x="{cx + (i*12)}" y="{start_y}" opacity="0">{char}'
        svg += f'<animate attributeName="opacity" values="0;0;1;1;0" keyTimes="0;{k1};{k1+0.01};{k2};1" dur="{total_dur}s" repeatCount="indefinite" />'
        svg += '</text>\n'

    # Load Phase
    load_y = start_y + line_h*2
    load_start = 3.0
    k_load = load_start / total_dur
    
    svg += f'<g opacity="0">\n'
    svg += f'  <text x="{start_x}" y="{load_y}" fill="{text_amber}">[ INSTALLING PACKAGES... ]</text>\n'
    svg += f'  <animate attributeName="opacity" values="0;0;1;1;0" keyTimes="0;{k_load};{k_load+0.01};0.9;1" dur="{total_dur}s" repeatCount="indefinite" />\n'
    svg += f'</g>\n'

    # Progress Bar
    bar_len = 30
    for i in range(bar_len):
        bd = load_start + 0.5 + (i * 0.05)
        bk = bd / total_dur
        svg += f'<text x="{start_x + (i*12)}" y="{load_y+line_h}" fill="{text_amber}" opacity="0">█'
        svg += f'<animate attributeName="opacity" values="0;0;1;1;0" keyTimes="0;{bk};{bk+0.01};0.9;1" dur="{total_dur}s" repeatCount="indefinite" />'
        svg += '</text>\n'

    # Result Phase
    res_y = load_y + line_h*4
    res_start = 5.5
    k_res = res_start / total_dur
    
    svg += f'<g opacity="0">\n'
    svg += f'  <text x="{start_x}" y="{res_y}" fill="{text_green}">> Payload Extracted.</text>\n'
    svg += f'  <text x="{start_x}" y="{res_y+line_h}" fill="{text_dim}">+ Role: Full Stack Architect</text>\n'
    svg += f'  <text x="{start_x}" y="{res_y+line_h*2}" fill="{text_dim}">+ Spec: AI/ML Researcher</text>\n'
    svg += f'  <text x="{start_x}" y="{res_y+line_h*3}" fill="{text_dim}">+ Status: OPEN_TO_WORK</text>\n'
    svg += f'  <animate attributeName="opacity" values="0;0;1;1;0" keyTimes="0;{k_res};{k_res+0.01};0.9;1" dur="{total_dur}s" repeatCount="indefinite" />\n'
    svg += f'</g>\n'

    svg += '</g>\n'

    # --- 5. OVERLAYS ---
    # Scanlines
    svg += f'<pattern id="scanlines" x="0" y="0" width="100" height="4" patternUnits="userSpaceOnUse">\n'
    svg += f'  <rect x="0" y="0" width="100" height="2" fill="#000" opacity="0.3" />\n'
    svg += f'</pattern>\n'
    svg += f'<rect x="{screen_x}" y="{screen_y}" width="{screen_w}" height="{screen_h}" fill="url(#scanlines)" pointer-events="none" />\n'
    
    # Reflection/Glare
    svg += f'<path d="M{screen_x} {screen_y} L{screen_x+screen_w} {screen_y} L{screen_x+screen_w} {screen_y+screen_h} Z" fill="#fff" opacity="0.05" pointer-events="none" />\n'

    svg += '</svg>'
    return svg

if __name__ == "__main__":
    if not os.path.exists("assets"): os.makedirs("assets")
    with open("assets/vintage-monitor.svg", "w", encoding="utf-8") as f:
        f.write(generate_vintage_monitor())
    print("Generated 90s Replica Monitor")
