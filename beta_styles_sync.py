import os
import re
import sys
import subprocess
import time
from bs4 import BeautifulSoup

sys.stdout.reconfigure(encoding='utf-8')

# Directory variables
beta_dir = r"c:\Users\Ruuji\Documents\Ai Store Presentation v1"
print_path = os.path.join(beta_dir, "print.html")
pdf_path = os.path.join(beta_dir, "presentation.pdf")

# Sleek typography and brand styles from remix.html to inject (Cursor None removed)
PREMIUM_STYLING = """
  /* ─── REMIX STYLING INJECTION ─── */
  :root {
    --black: #000000;
    --purple: #9333ea;
    --purple-light: #c084fc;
    --blue: #3b82f6;
    --blue-light: #93c5fd;
    --pink: #ec4899;
    --pink-light: #f9a8d4;
    --white: #ffffff;
    --white-dim: rgba(255,255,255,0.7);
    --card-bg: rgba(255,255,255,0.04);
    --card-border: rgba(255,255,255,0.08);
  }

  body {
    background: var(--black) !important;
    color: var(--white) !important;
    font-family: 'Outfit', sans-serif !important;
    overflow-x: hidden;
  }

  /* ─── NOISE OVERLAY ─── */
  body::before {
    content: '';
    position: fixed; inset: 0;
    background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)'/%3E%3C/svg%3E") !important;
    opacity: 0.022; pointer-events: none; z-index: 1000;
  }

  /* ─── AMBIENT GLOWS (SINGLE RIGHT GLOW) ─── */
  .hero-glow-purple {
    position: absolute; bottom: -100px; right: -5%;
    width: 60vw; height: 60vw; border-radius: 50%;
    background: radial-gradient(circle, rgba(147,51,234,0.22) 0%, transparent 65%) !important;
    filter: blur(50px); pointer-events: none;
    animation: glow-pulse 6s ease-in-out infinite alternate;
    z-index: 2;
  }

  @keyframes glow-pulse {
    from { opacity: 0.8; transform: scale(0.95); }
    to   { opacity: 1.0; transform: scale(1.05); }
  }

  /* ─── SINGLE FLOATING ORB (RIGHT) ─── */
  .orb {
    position: absolute;
    border-radius: 50%;
    background: conic-gradient(from 0deg, #c084fc, #818cf8, #38bdf8, #34d399, #f472b6, #c084fc) !important;
    filter: blur(1px) saturate(1.4) !important;
    animation: float 8s ease-in-out infinite;
    opacity: 0.75 !important;
    z-index: 2;
    pointer-events: none !important;
  }

  .orb::after {
    content: '';
    position: absolute; inset: 5px;
    border-radius: 50%;
    background: radial-gradient(circle at 30% 30%, rgba(255,255,255,0.6), rgba(0,0,0,0.3)) !important;
  }
  .orb-tr { top: 8%; right: 5%; width: 145px; height: 145px; animation-delay: 0s; }

  @keyframes float {
    0%,100% { transform: translateY(0px) rotate(0deg); }
    33%      { transform: translateY(-18px) rotate(6deg); }
    66%      { transform: translateY(10px) rotate(-4deg); }
  }

  /* ─── SLIDE CONTAINER OVERRIDES ─── */
  .slide-container {
    background: #000000 !important;
    border-radius: 20px !important;
    border: 1px solid rgba(255,255,255,0.06) !important;
    box-shadow: 0 40px 100px rgba(0, 0, 0, 0.9), 0 0 60px rgba(147, 51, 234, 0.04) !important;
  }

  .grid-pattern {
    background-image: 
      linear-gradient(rgba(255,255,255,0.015) 1px, transparent 1px),
      linear-gradient(90deg, rgba(255,255,255,0.015) 1px, transparent 1px) !important;
    background-size: 60px 60px !important;
    z-index: 1 !important;
    -webkit-mask-image: radial-gradient(ellipse 70% 80% at 50% 50%, black 50%, transparent 100%) !important;
    mask-image: radial-gradient(ellipse 70% 80% at 50% 50%, black 50%, transparent 100%) !important;
  }

  .content-wrapper {
    z-index: 10 !important;
    opacity: 1 !important;
    transform: none !important;
  }

  /* ─── TYPOGRAPHY OVERRIDES ─── */
  h1 {
    font-family: 'Bebas Neue', sans-serif !important;
    font-size: clamp(80px, 12vw, 110px) !important;
    font-weight: 400 !important;
    letter-spacing: 2px !important;
    line-height: 0.95 !important;
    margin-bottom: 25px !important;
    background: linear-gradient(170deg, #ffffff 0%, #e8d5ff 50%, #c084fc 100%) !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    background-clip: text !important;
  }

  h2 {
    font-family: 'Bebas Neue', sans-serif !important;
    font-size: 52px !important;
    font-weight: 400 !important;
    letter-spacing: 1px !important;
    line-height: 1 !important;
    margin-bottom: 10px !important;
  }

  h3 {
    font-family: 'Bebas Neue', sans-serif !important;
    font-size: 26px !important;
    font-weight: 400 !important;
    letter-spacing: 1.5px !important;
  }

  .subtitle {
    font-family: 'Outfit', sans-serif !important;
    font-weight: 300 !important;
    font-size: 22px !important;
    color: var(--white-dim) !important;
  }

  /* ─── PREMIUM rounded UI widgets ─── */
  .innovation-badge, .page-badge, .date-badge {
    display: inline-flex !important;
    align-items: center !important;
    gap: 10px !important;
    background: rgba(255, 255, 255, 0.04) !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    padding: 8px 20px !important;
    border-radius: 100px !important;
    color: #ffffff !important;
    font-family: 'Outfit', sans-serif !important;
    font-size: 13px !important;
    font-weight: 600 !important;
    letter-spacing: 1.5px !important;
    text-transform: uppercase !important;
    backdrop-filter: blur(10px) !important;
    -webkit-backdrop-filter: blur(10px) !important;
    transition: all 0.3s ease !important;
  }
  
  .innovation-badge:hover, .page-badge:hover, .date-badge:hover {
    background: rgba(255, 255, 255, 0.08) !important;
    border-color: rgba(255, 255, 255, 0.2) !important;
    box-shadow: 0 0 20px rgba(255,255,255,0.05) !important;
  }

  .decorative-line {
    background: linear-gradient(90deg, var(--purple-light), var(--pink-light)) !important;
    border-radius: 100px !important;
    height: 3px !important;
  }

  /* rounded glassmorphism cards */
  .side-card, .agent-card, .trait-card, .pricing-card, .info-card, .audience-card, .metric-card, .compliance-card, .growth-card, .tactic-card, .team-card, .cta-card {
    background: var(--card-bg) !important;
    border: 1px solid var(--card-border) !important;
    border-radius: 16px !important;
    backdrop-filter: blur(10px) !important;
    -webkit-backdrop-filter: blur(10px) !important;
    transition: all 0.4s cubic-bezier(0.165, 0.84, 0.44, 1) !important;
    box-shadow: 0 10px 30px rgba(0,0,0,0.15) !important;
  }
  
  .side-card:hover, .agent-card:hover, .trait-card:hover, .pricing-card:hover, .info-card:hover, .team-card:hover, .cta-card:hover {
    border-color: rgba(147, 51, 234, 0.4) !important;
    transform: translateY(-4px) !important;
    box-shadow: 0 15px 35px rgba(147, 51, 234, 0.18), 0 0 20px rgba(147, 51, 234, 0.05) !important;
  }

  .side-card::before, .agent-card::before {
    display: none !important; /* Hide blocky colored top-borders */
  }

  .featured-badge, .featured-tag, .popular-badge, .agent-badge {
    background: linear-gradient(135deg, var(--pink), var(--purple)) !important;
    border-radius: 100px !important;
    padding: 4px 12px !important;
    font-size: 11px !important;
    font-weight: 700 !important;
    color: white !important;
    letter-spacing: 1px !important;
    text-transform: uppercase !important;
    border: none !important;
  }

  .launch-demo-btn, .btn-primary, .btn-submit {
    background: linear-gradient(135deg, var(--purple), var(--pink)) !important;
    border-radius: 100px !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    color: white !important;
    font-weight: 700 !important;
    font-family: 'Outfit', sans-serif !important;
    box-shadow: 0 0 30px rgba(147, 51, 234, 0.35) !important;
    transition: all 0.3s ease !important;
  }
  
  .launch-demo-btn:hover, .btn-primary:hover {
    box-shadow: 0 0 45px rgba(147, 51, 234, 0.6), 0 0 70px rgba(236,72,153,0.3) !important;
    transform: translateY(-2px) !important;
    border-color: rgba(255,255,255,0.2) !important;
  }

  .btn-ghost {
    border-radius: 100px !important;
    border: 1px solid rgba(255,255,255,0.2) !important;
    font-family: 'Outfit', sans-serif !important;
    transition: all 0.3s ease !important;
  }
  .btn-ghost:hover {
    border-color: rgba(255,255,255,0.5) !important;
    background: rgba(255,255,255,0.05) !important;
  }

  /* Specific visual improvements for lists and connectors */
  .arrow-connector {
    color: var(--purple-light) !important;
    text-shadow: 0 0 15px rgba(168,85,247,0.4);
  }
  
  .result-box {
    border-radius: 12px !important;
  }

  .feature-tag {
    border-radius: 100px !important;
    background: rgba(255, 255, 255, 0.04) !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    font-family: 'Outfit', sans-serif !important;
  }
  
  .user-image {
    border-radius: 16px !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
  }

  /* Screen overrides for fullscreen deck transition */
  .slide-nav-overlay {
    background: rgba(0, 0, 0, 0.65) !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    border-radius: 100px !important;
    backdrop-filter: blur(15px) !important;
    -webkit-backdrop-filter: blur(15px) !important;
    box-shadow: 0 10px 30px rgba(0,0,0,0.5) !important;
  }
"""

CURSOR_HTML = ""
BG_GLOW_ORBS_HTML = """
<div class="hero-glow-purple"></div>
<div class="orb orb-tr"></div>
"""
CURSOR_TRACKER_JS = ""

print("=== STARTING STYLES ADAPTATION SCRIPT (NORMAL MOUSE) ===")

# 1. Adapt individual slide files
slide_files = ["index.html"] + [f"slide{i}.html" for i in range(2, 11)]

for filename in slide_files:
    file_path = os.path.join(beta_dir, filename)
    if not os.path.exists(file_path):
        print(f"  Slide File NOT found: {filename}")
        continue
        
    print(f"  Processing {filename}...")
    with open(file_path, "r", encoding="utf-8") as f:
        html = f.read()
        
    soup = BeautifulSoup(html, 'html.parser')
    
    # Update stylesheet link in head
    for link in soup.find_all('link'):
        if link.get('href') and 'fonts.googleapis.com' in link.get('href'):
            link['href'] = "https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Outfit:wght@300;400;500;600;700;800;900&display=swap"
            
    # Inject Premium CSS into style block
    style_tag = soup.find('style')
    if style_tag:
        style_content = style_tag.string or ""
        # Strip old sync injection if it exists, to allow clean overwrite
        if "REMIX STYLING INJECTION" in style_content:
            idx = style_content.find("/* ─── REMIX STYLING INJECTION ─── */")
            style_content = style_content[:idx]
        # Strip duplicate :host blocks left by previous print sync runs
        import re as _re
        style_content = _re.sub(r'\s*/\* Perfect 1080p Landscape Print Resolution \*/\s*\n\s*:host\s*\{[^}]*\}', '', style_content)
        style_tag.string = style_content + PREMIUM_STYLING
            
    # Clean Custom Cursor HTML if it exists
    body = soup.find('body')
    if body:
        for old_cursor in body.find_all(id=["cursor", "cursorRing"]):
            old_cursor.decompose()
            
    # Remove .slide-nav-overlay elements (chevron nav bars) from slide body
    # These are only useful in standalone mode; in slides.html Shadow DOM they are non-functional
    for nav_overlay in soup.find_all(class_='slide-nav-overlay'):
        nav_overlay.decompose()
    # Also remove the inline <style> block for .slide-nav-overlay that precedes it
    for extra_style in soup.find_all('style'):
        if extra_style != style_tag and extra_style.string and 'slide-nav-overlay' in (extra_style.string or ''):
            extra_style.decompose()

    # Inject Ambient Orbs / Glow elements inside .slide-container (Clean old ones first)
    slide_container = soup.find(class_='slide-container')
    if slide_container:
        # Clean old orbs/glows
        for old_el in slide_container.find_all(class_=["hero-glow-blue", "hero-glow-purple", "hero-glow-pink", "orb"]):
            old_el.decompose()
        
        # Inject new single orb and glow on the right
        grid = slide_container.find(class_='grid-pattern')
        orbs_soup = BeautifulSoup(BG_GLOW_ORBS_HTML, 'html.parser')
        if grid:
            grid.insert_after(orbs_soup)
        else:
            slide_container.insert(0, orbs_soup)
                
    # Clean custom cursor script tracking logic from script tag
    script_tag = soup.find('script')
    if script_tag:
        script_content = script_tag.string or ""
        if "High-fidelity cursor tracker" in script_content:
            idx = script_content.find("// High-fidelity cursor tracker")
            if idx != -1:
                script_tag.string = script_content[:idx].rstrip()
                
    # Save slide file
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(str(soup))
        
    print(f"  Completed adaptation of {filename}.")

print("\n=== RE-SYNCHRONIZING SLIDES WITH PRINT.HTML SHADOW DOM ROOTS ===")

# Process print.html Shadow DOM sync
if os.path.exists(print_path):
    with open(print_path, "r", encoding="utf-8") as f:
        print_content = f.read()
        
    soup_print = BeautifulSoup(print_content, 'html.parser')
    
    # Update print.html font link
    for link in soup_print.find_all('link'):
        if link.get('href') and 'fonts.googleapis.com' in link.get('href'):
            link['href'] = "https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Outfit:wght@300;400;500;600;700;800;900&display=swap"
            
    # Update print.html master styles
    style_tags = soup_print.find_all('style')
    if style_tags:
        master_style_content = style_tags[0].string or ""
        if "REMIX STYLING INJECTION" in master_style_content:
            idx = master_style_content.find("/* ─── REMIX STYLING INJECTION ─── */")
            master_style_content = master_style_content[:idx]
        style_tags[0].string = master_style_content + PREMIUM_STYLING
            
    # Clean Custom Cursor HTML in print body level
    body_print = soup_print.find('body')
    if body_print:
        for old_cursor in body_print.find_all(id=["cursor", "cursorRing"]):
            old_cursor.decompose()

    print_content = str(soup_print)
    
    # Helper to extract updated styles & content of slides
    def extract_slide_content(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            html = f.read()
        soup = BeautifulSoup(html, 'html.parser')
        styles = soup.find_all('style')
        container = soup.find(class_='slide-container')
        if not container:
            return None
        parts = []
        for style in styles:
            parts.append(str(style))
        parts.append(str(container))
        combined = "\n\n".join(parts)
        combined = combined.replace("`", "\\`").replace("${", "\\${")
        # Escape </script> to prevent early script closing in slides.html template literal
        combined = combined.replace("</script>", "<\\/script>")
        return combined

    # Re-sync shadow DOM slots (1 to 10)
    for i in range(1, 11):
        filename = "index.html" if i == 1 else f"slide{i}.html"
        slide_path = os.path.join(beta_dir, filename)
        new_content = extract_slide_content(slide_path)
        if not new_content:
            print(f"  Shadow DOM Sync: Slide {i} extraction failed.")
            continue
            
        start_pattern = rf"const\s+root{i}\s*=\s*document\.getElementById\('slide-wrapper-{i}'\)\.attachShadow\({{mode:\s*'open'}}\);\s*root{i}\.innerHTML\s*=\s*`"
        start_match = re.search(start_pattern, print_content)
        if not start_match:
            print(f"  Shadow DOM Sync: Slide {i} pattern NOT found in print.html.")
            continue
            
        start_idx = start_match.end()
        end_idx = print_content.find("`;", start_idx)
        if end_idx == -1:
            print(f"  Shadow DOM Sync: Slide {i} closing pattern NOT found in print.html.")
            continue
            
        print_content = print_content[:start_idx] + "\n" + new_content + "\n        " + print_content[end_idx:]
        print(f"  Shadow DOM Sync: Slide {i} re-synced successfully in print.html.")
        
    # Save print.html
    with open(print_path, "w", encoding="utf-8") as f:
        f.write(print_content)
    print("  Completed print.html Shadow DOM sync.")
else:
    print("  Warning: print.html NOT found.")

# 2. Process demo.html adaptation
demo_path = os.path.join(beta_dir, "demo.html")
if os.path.exists(demo_path):
    print("\n=== PROCESSING INTERACTIVE PROTOTYPE DEMO.HTML ===")
    with open(demo_path, "r", encoding="utf-8") as f:
        demo_html = f.read()
        
    soup_demo = BeautifulSoup(demo_html, 'html.parser')
    
    # Font import update
    for link in soup_demo.find_all('link'):
        if link.get('href') and 'fonts.googleapis.com' in link.get('href'):
            link['href'] = "https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Outfit:wght@300;400;500;600;700;800;900&display=swap"
            
    # Clean Custom Cursor HTML elements in body
    body_demo = soup_demo.find('body')
    if body_demo:
        for old_cursor in body_demo.find_all(id=["cursor", "cursorRing"]):
            old_cursor.decompose()
        
        # Clean old dashboard orbs/glows from body direct children
        for old_el in body_demo.find_all(class_=["hero-glow-blue", "hero-glow-purple", "hero-glow-pink", "orb"], recursive=False):
            old_el.decompose()
            
        # Inject new single orb and glow on body level as dashboard background (behind content)
        bg_orbs_soup = BeautifulSoup(BG_GLOW_ORBS_HTML, 'html.parser')
        body_demo.insert(0, bg_orbs_soup)
            
    # Onboarding overlay chrome float orb (single right orb)
    onboarding_overlay = soup_demo.find(id="onboarding-overlay")
    if onboarding_overlay:
        # Clean old ones first
        for old_el in onboarding_overlay.find_all(class_=["hero-glow-blue", "hero-glow-purple", "hero-glow-pink", "orb"]):
            old_el.decompose()
        # Inject new single orb and glow on the right
        orbs_soup = BeautifulSoup(BG_GLOW_ORBS_HTML, 'html.parser')
        onboarding_overlay.insert(0, orbs_soup)
            
    # Style block modification (Root variables + noise + rounded glass cards)
    style_demo = soup_demo.find('style')
    if style_demo:
        style_content = style_demo.string or ""
        if "REMIX STYLING INJECTION" in style_content:
            idx = style_content.find("/* ─── REMIX STYLING INJECTION ─── */")
            style_content = style_content[:idx]
            
        # Aggressive typography, layout and design overrides (Cursor: None completely removed)
        style_demo.string = style_content + PREMIUM_STYLING + """
            /* ─── AGGRESSIVE DEMO INTERACTIVE OVERRIDES ─── */
            :root {
                --bg-deep: #000000 !important;
                --bg-card: rgba(0, 0, 0, 0.6) !important;
                --bg-nav: rgba(0, 0, 0, 0.9) !important;
                --border-glow: rgba(255, 255, 255, 0.08) !important;
                --border-glow-active: rgba(147, 51, 234, 0.5) !important;
                --purple-neon: #9333ea !important;
                --purple-light: #c084fc !important;
                --pink-neon: #ec4899 !important;
                --pink-light: #f9a8d4 !important;
                --glass-grad: linear-gradient(135deg, rgba(255, 255, 255, 0.03) 0%, rgba(255, 255, 255, 0.01) 100%) !important;
                --accent-grad: linear-gradient(135deg, var(--purple-neon) 0%, var(--pink-neon) 100%) !important;
            }

            body {
                font-family: 'Outfit', sans-serif !important;
                background: #000000 !important;
                overflow: hidden !important;
            }

            /* ─── FLOATING GLASS SIDEBAR CAPSULE ─── */
            sidebar {
                position: fixed !important;
                left: 20px !important;
                top: 20px !important;
                bottom: 20px !important;
                width: 280px !important;
                height: calc(100vh - 40px) !important;
                background: rgba(0, 0, 0, 0.6) !important;
                border: 1px solid rgba(255, 255, 255, 0.08) !important;
                border-radius: 24px !important;
                padding: 30px 20px !important;
                backdrop-filter: blur(30px) !important;
                -webkit-backdrop-filter: blur(30px) !important;
                box-shadow: 0 30px 70px rgba(0, 0, 0, 0.8), inset 0 0 20px rgba(255, 255, 255, 0.02) !important;
                z-index: 100 !important;
                display: flex !important;
                flex-direction: column !important;
                justify-content: space-between !important;
                transition: all 0.3s cubic-bezier(0.165, 0.84, 0.44, 1) !important;
            }

            .nav-group {
                gap: 12px !important;
            }

            .nav-title {
                font-family: 'Outfit', sans-serif !important;
                font-size: 11px !important;
                color: rgba(255, 255, 255, 0.3) !important;
                letter-spacing: 2px !important;
                text-transform: uppercase !important;
                font-weight: 700 !important;
                margin-bottom: 8px !important;
                padding-left: 12px !important;
            }

            .nav-link {
                border-radius: 100px !important; /* Spacious Rounded Pills */
                padding: 14px 20px !important;
                font-size: 14px !important;
                color: rgba(255, 255, 255, 0.5) !important;
                border: 1px solid transparent !important;
                transition: all 0.3s cubic-bezier(0.165, 0.84, 0.44, 1) !important;
            }
            
            .nav-link:hover {
                background: rgba(255, 255, 255, 0.03) !important;
                color: #ffffff !important;
                transform: translateX(4px) !important;
                border-color: rgba(255, 255, 255, 0.08) !important;
            }

            .nav-link.active {
                background: linear-gradient(135deg, rgba(147, 51, 234, 0.2), rgba(236, 72, 153, 0.1)) !important;
                border-color: rgba(147, 51, 234, 0.4) !important;
                color: #ffffff !important;
                font-weight: 600 !important;
                box-shadow: 0 8px 24px rgba(147, 51, 234, 0.15) !important;
                transform: translateX(4px) !important;
            }

            .nav-footer-promo {
                background: rgba(255, 255, 255, 0.02) !important;
                border: 1px solid rgba(255, 255, 255, 0.06) !important;
                border-radius: 20px !important;
                padding: 20px !important;
            }

            /* ─── FLOATING GLASS HEADER ─── */
            header {
                position: fixed !important;
                top: 20px !important;
                left: 320px !important;
                right: 20px !important;
                height: 70px !important;
                background: rgba(0, 0, 0, 0.6) !important;
                border: 1px solid rgba(255, 255, 255, 0.08) !important;
                border-radius: 20px !important;
                padding: 0 30px !important;
                backdrop-filter: blur(30px) !important;
                -webkit-backdrop-filter: blur(30px) !important;
                box-shadow: 0 20px 40px rgba(0,0,0,0.5) !important;
                z-index: 99 !important;
                display: flex !important;
                align-items: center !important;
                justify-content: space-between !important;
            }

            .header-logo span {
                font-family: 'Bebas Neue', sans-serif !important;
                font-size: 28px !important;
                letter-spacing: 1px !important;
                font-weight: 400 !important;
                background: linear-gradient(135deg, var(--white), var(--purple-light)) !important;
                -webkit-background-clip: text !important;
                -webkit-text-fill-color: transparent !important;
            }

            /* ─── FLOATING CONTENT VIEWPORT ─── */
            .app-body {
                background: transparent !important;
                border: none !important;
                box-shadow: none !important;
                overflow: visible !important;
            }

            main {
                position: absolute !important;
                top: 110px !important;
                left: 320px !important;
                right: 20px !important;
                bottom: 20px !important;
                padding: 0 10px 0 0 !important;
                overflow-y: auto !important;
                background: transparent !important;
            }

            /* ─── EDITORIAL PAGE HEADERS ─── */
            .page-header {
                margin-bottom: 40px !important;
            }

            .page-title {
                font-family: 'Bebas Neue', sans-serif !important;
                font-size: 56px !important;
                letter-spacing: 2px !important;
                font-weight: 400 !important;
                background: linear-gradient(170deg, #ffffff 0%, #e8d5ff 50%, #c084fc 100%) !important;
                -webkit-background-clip: text !important;
                -webkit-text-fill-color: transparent !important;
                background-clip: text !important;
                margin-bottom: 8px !important;
                text-transform: uppercase !important;
            }

            .page-subtitle {
                font-size: 16px !important;
                color: var(--white-dim) !important;
                font-weight: 300 !important;
            }

            /* ─── OBSIDIAN GLASS CARDS & AUDIT PANELS ─── */
            .agent-card, .chat-layout, .chat-action-card, .vault-card, .onboarding-card, .gdpr-audit-panel, .credit-plan-card, .referral-card {
                border-radius: 24px !important;
                background: rgba(0, 0, 0, 0.6) !important;
                border: 1px solid rgba(255, 255, 255, 0.08) !important;
                backdrop-filter: blur(20px) !important;
                -webkit-backdrop-filter: blur(20px) !important;
                box-shadow: 0 20px 50px rgba(0, 0, 0, 0.7), 0 0 35px rgba(147, 51, 234, 0.03) !important;
                transition: all 0.4s cubic-bezier(0.165, 0.84, 0.44, 1) !important;
            }

            .agent-card:hover, .credit-plan-card:hover, .referral-card:hover {
                border-color: rgba(147, 51, 234, 0.5) !important;
                transform: translateY(-6px) scale(1.01) !important;
                box-shadow: 0 25px 60px rgba(147, 51, 234, 0.22), 0 0 30px rgba(147, 51, 234, 0.08) !important;
            }

            .agent-name {
                font-family: 'Outfit', sans-serif !important;
                font-size: 22px !important;
                font-weight: 700 !important;
                color: #ffffff !important;
            }

            /* ─── CHAT INTERFACE OVERHAUL ─── */
            .chat-layout {
                max-width: 1000px !important;
                margin: 0 auto !important;
            }

            .chat-header-bar {
                padding: 20px 30px !important;
                border-bottom: 1px solid rgba(255, 255, 255, 0.06) !important;
            }

            .chat-messages-box {
                padding: 35px 30px !important;
                gap: 24px !important;
            }

            .chat-bubble {
                font-family: 'Outfit', sans-serif !important;
                font-size: 14.5px !important;
                line-height: 1.6 !important;
                padding: 18px 24px !important;
                max-width: 75% !important;
                box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15) !important;
            }

            .chat-bubble.coordinator {
                background: rgba(255, 255, 255, 0.03) !important;
                border: 1px solid rgba(255, 255, 255, 0.06) !important;
                border-radius: 20px !important;
                border-top-left-radius: 4px !important;
                color: var(--white) !important;
            }

            .chat-bubble.user {
                background: linear-gradient(135deg, var(--purple), var(--pink)) !important;
                border-radius: 20px !important;
                border-top-right-radius: 4px !important;
                color: #ffffff !important;
                box-shadow: 0 8px 30px rgba(147, 51, 234, 0.3) !important;
            }

            .chat-input-bar {
                padding: 20px 30px !important;
                background: rgba(0, 0, 0, 0.4) !important;
                border-top: 1px solid rgba(255, 255, 255, 0.06) !important;
                border-bottom-left-radius: 24px !important;
                border-bottom-right-radius: 24px !important;
            }

            .chat-input-field {
                border-radius: 100px !important;
                background: rgba(255, 255, 255, 0.03) !important;
                border: 1px solid rgba(255, 255, 255, 0.08) !important;
                padding: 16px 28px !important;
                color: #ffffff !important;
                font-family: 'Outfit', sans-serif !important;
                font-size: 14.5px !important;
                transition: all 0.3s ease !important;
            }

            .chat-input-field:focus {
                border-color: rgba(147, 51, 234, 0.5) !important;
                background: rgba(255, 255, 255, 0.06) !important;
                box-shadow: 0 0 20px rgba(147, 51, 234, 0.1) !important;
            }

            .chat-send-btn {
                width: 50px !important;
                height: 50px !important;
                border-radius: 50% !important;
                background: linear-gradient(135deg, var(--purple), var(--pink)) !important;
                box-shadow: 0 4px 15px rgba(147, 51, 234, 0.25) !important;
                transition: all 0.3s ease !important;
            }

            .chat-send-btn:hover {
                transform: scale(1.05) !important;
                box-shadow: 0 4px 20px rgba(147, 51, 234, 0.45) !important;
            }

            /* ─── ONBOARDING OVERLAY REDESIGN ─── */
            #onboarding-overlay {
                background: radial-gradient(circle at center, #000000 0%, #050209 100%) !important;
            }

            .onboarding-card {
                max-width: 650px !important;
                padding: 60px 50px !important;
                background: rgba(0, 0, 0, 0.65) !important;
                border: 1px solid rgba(255, 255, 255, 0.08) !important;
                border-radius: 32px !important;
                backdrop-filter: blur(30px) !important;
                -webkit-backdrop-filter: blur(30px) !important;
                box-shadow: 0 40px 100px rgba(0,0,0,0.9), 0 0 60px rgba(147, 51, 234, 0.1) !important;
                position: relative !important;
            }

            .onboarding-card::before {
                display: none !important;
            }

            .onboarding-title {
                font-family: 'Bebas Neue', sans-serif !important;
                font-size: 64px !important;
                letter-spacing: 2.5px !important;
                font-weight: 400 !important;
                background: linear-gradient(170deg, #ffffff 0%, #e8d5ff 50%, #c084fc 100%) !important;
                -webkit-background-clip: text !important;
                -webkit-text-fill-color: transparent !important;
                background-clip: text !important;
                margin-bottom: 12px !important;
            }

            /* ─── SAFE SANDBOX INTERFACE ─── */
            #sandbox-workspace {
                position: fixed !important;
                top: 110px !important;
                left: 320px !important;
                right: 20px !important;
                bottom: 20px !important;
                width: auto !important;
                height: auto !important;
                background: rgba(0, 0, 0, 0.6) !important;
                border: 1px solid rgba(255, 255, 255, 0.08) !important;
                border-radius: 24px !important;
                padding: 30px !important;
                box-shadow: 0 30px 80px rgba(0, 0, 0, 0.8), inset 0 0 20px rgba(255, 255, 255, 0.01) !important;
                backdrop-filter: blur(20px) !important;
                -webkit-backdrop-filter: blur(20px) !important;
                overflow-y: auto !important;
            }
            
            .sandbox-header {
                border-bottom: 1px solid rgba(255, 255, 255, 0.06) !important;
                padding-bottom: 20px !important;
                margin-bottom: 25px !important;
            }
            
            .terminal-panel, .browser-panel {
                background: rgba(0, 0, 0, 0.75) !important;
                border: 1px solid rgba(255, 255, 255, 0.08) !important;
                border-radius: 20px !important;
                overflow: hidden !important;
                box-shadow: 0 15px 45px rgba(0, 0, 0, 0.5) !important;
            }

            .terminal-body {
                background: #000000 !important;
                color: #c084fc !important;
                font-family: 'Fira Code', 'Courier New', monospace !important;
                padding: 20px !important;
                font-size: 13px !important;
                line-height: 1.6 !important;
            }
            
            .browser-toolbar {
                background: rgba(255, 255, 255, 0.02) !important;
                border-bottom: 1px solid rgba(255, 255, 255, 0.06) !important;
                padding: 12px 20px !important;
                display: flex !important;
                align-items: center !important;
                gap: 15px !important;
            }
            
            .browser-address-bar {
                background: rgba(0, 0, 0, 0.4) !important;
                border: 1px solid rgba(255, 255, 255, 0.06) !important;
                border-radius: 100px !important;
                padding: 8px 20px !important;
                font-family: 'Outfit', sans-serif !important;
                color: rgba(255, 255, 255, 0.6) !important;
                font-size: 13px !important;
                display: flex !important;
                align-items: center !important;
                gap: 10px !important;
                flex: 1 !important;
            }

            .status-item {
                background: rgba(255, 255, 255, 0.03) !important;
                border: 1px solid rgba(255, 255, 255, 0.08) !important;
                border-radius: 100px !important;
                padding: 8px 16px !important;
                font-family: 'Outfit', sans-serif !important;
                color: #ffffff !important;
                font-size: 12px !important;
                font-weight: 500 !important;
                display: inline-flex !important;
                align-items: center !important;
                gap: 8px !important;
            }

            .back-slides-btn {
                background: linear-gradient(135deg, rgba(255, 255, 255, 0.05), rgba(255, 255, 255, 0.02)) !important;
                border: 1px solid rgba(255, 255, 255, 0.1) !important;
                border-radius: 100px !important;
                padding: 10px 22px !important;
                font-family: 'Outfit', sans-serif !important;
                color: #ffffff !important;
                font-size: 13px !important;
                font-weight: 600 !important;
                transition: all 0.3s ease !important;
            }

            .back-slides-btn:hover {
                background: rgba(255, 255, 255, 0.1) !important;
                border-color: rgba(255, 255, 255, 0.3) !important;
                box-shadow: 0 0 20px rgba(255, 255, 255, 0.05) !important;
            }

            /* Tables and other panels */
            .audit-logs-table th {
                font-family: 'Outfit', sans-serif !important;
                text-transform: uppercase !important;
                font-size: 12px !important;
                letter-spacing: 1px !important;
                color: rgba(255, 255, 255, 0.4) !important;
                border-bottom: 1px solid rgba(255, 255, 255, 0.06) !important;
                padding: 16px 20px !important;
            }

            .audit-logs-table td {
                padding: 16px 20px !important;
                border-bottom: 1px solid rgba(255, 255, 255, 0.04) !important;
                font-size: 13.5px !important;
            }

            .gdpr-audit-panel {
                padding: 30px !important;
            }

            .audit-header {
                margin-bottom: 30px !important;
                border-bottom: 1px solid rgba(255, 255, 255, 0.06) !important;
                padding-bottom: 20px !important;
            }

            .audit-header h2 {
                font-family: 'Outfit', sans-serif !important;
                font-size: 24px !important;
                font-weight: 700 !important;
            }
            """
            
    # Clean Custom Cursor script tracking logic from demo script tag
    script_demo_tag = soup_demo.find('body').find('script')
    if script_demo_tag:
        script_demo_content = script_demo_tag.string or ""
        if "High-fidelity cursor tracker" in script_demo_content:
            idx = script_demo_content.find("// High-fidelity cursor tracker")
            if idx != -1:
                script_demo_tag.string = script_demo_content[:idx].rstrip()
            
    # Save demo.html
    with open(demo_path, "w", encoding="utf-8") as f:
        f.write(str(soup_demo))
    print("  Completed adaptation of demo.html.")
else:
    print("  Warning: demo.html NOT found.")

# 3. Create/Compile single-page slides presenter slides.html
slides_path = os.path.join(beta_dir, "slides.html")
print("\n=== COMPILING SINGLE-PAGE INTERACTIVE PRESENTATION SLIDES.HTML ===")

shadow_slots = []
for i in range(1, 11):
    filename = "index.html" if i == 1 else f"slide{i}.html"
    slide_path = os.path.join(beta_dir, filename)
    new_content = extract_slide_content(slide_path)
    if new_content:
        shadow_slots.append(f"""
        const root{i} = document.getElementById('slide-wrapper-{i}').attachShadow({{mode: 'open'}});
        root{i}.innerHTML = `{new_content}`;
        """)
    else:
        print(f"  Single-Page Compiler: Slide {i} extraction failed.")

shadow_slots_js = "\n".join(shadow_slots)

slides_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>The AI Store - Complete Presentation Slide Deck</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Outfit:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
  <style>
    :root {{
      --black: #000000;
      --purple: #9333ea;
      --purple-light: #c084fc;
      --blue: #3b82f6;
      --pink: #ec4899;
      --pink-light: #f9a8d4;
      --white: #ffffff;
    }}
    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }}
    body {{
      background: var(--black) !important;
      color: var(--white) !important;
      font-family: 'Outfit', sans-serif !important;
      overflow: hidden !important;
      width: 100vw !important;
      height: 100vh !important;
      display: flex !important;
      justify-content: center !important;
      align-items: center !important;
    }}
    
    /* Cinematic Background Noise */
    body::before {{
      content: '' !important;
      position: fixed !important; inset: 0 !important;
      background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)'/%3E%3C/svg%3E") !important;
      opacity: 0.022 !important; pointer-events: none !important; z-index: 1000 !important;
    }}
    
    /* Top-level Ambient Glows and Orb */
    .hero-glow-purple {{
      position: absolute !important; bottom: -100px !important; right: -5% !important;
      width: 60vw !important; height: 60vw !important; border-radius: 50% !important;
      background: radial-gradient(circle, rgba(147,51,234,0.18) 0%, transparent 65%) !important;
      filter: blur(50px) !important; pointer-events: none !important;
      animation: glow-pulse 6s ease-in-out infinite alternate !important;
      z-index: 2 !important;
    }}
    @keyframes glow-pulse {{
      from {{ opacity: 0.8; transform: scale(0.95); }}
      to   {{ opacity: 1.0; transform: scale(1.05); }}
    }}
    
    .orb {{
      position: absolute !important;
      border-radius: 50% !important;
      background: conic-gradient(from 0deg, #c084fc, #818cf8, #38bdf8, #34d399, #f472b6, #c084fc) !important;
      filter: blur(1px) saturate(1.4) !important;
      animation: float 8s ease-in-out infinite !important;
      opacity: 0.65 !important;
      z-index: 2 !important;
      pointer-events: none !important;
    }}
    .orb::after {{
      content: '' !important;
      position: absolute !important; inset: 5px !important;
      border-radius: 50% !important;
      background: radial-gradient(circle at 30% 30%, rgba(255,255,255,0.6), rgba(0,0,0,0.3)) !important;
    }}
    .orb-tr {{ top: 8% !important; right: 5% !important; width: 145px; height: 145px; }}
    @keyframes float {{
      0%, 100% {{ transform: translateY(0px) rotate(0deg); }}
      33%      {{ transform: translateY(-18px) rotate(6deg); }}
      66%      {{ transform: translateY(10px) rotate(-4deg); }}
    }}

    /* Presentation Deck Viewport */
    .presentation-viewport {{
      width: 1280px !important;
      height: 720px !important;
      position: relative !important;
      z-index: 10 !important;
      display: flex !important;
      justify-content: center !important;
      align-items: center !important;
      transform-origin: center center !important;
    }}

    /* Slide Wrappers and Transitions */
    .slide-wrapper {{
      position: absolute !important;
      inset: 0 !important;
      width: 1280px !important;
      height: 720px !important;
      opacity: 0 !important;
      pointer-events: none !important;
      transform: scale(0.96) translate3d(0, 20px, 0) !important;
      transition: opacity 0.5s cubic-bezier(0.16, 1, 0.3, 1), transform 0.5s cubic-bezier(0.16, 1, 0.3, 1) !important;
      z-index: 1 !important;
    }}

    .slide-wrapper.active {{
      opacity: 1 !important;
      pointer-events: auto !important;
      transform: scale(1) translate3d(0, 0, 0) !important;
      z-index: 2 !important;
    }}

    .slide-wrapper.exit-left {{
      opacity: 0 !important;
      transform: scale(0.96) translate3d(-30px, 0, 0) !important;
    }}
    .slide-wrapper.exit-right {{
      opacity: 0 !important;
      transform: scale(0.96) translate3d(30px, 0, 0) !important;
    }}
  </style>
</head>
<body>
  <div class="hero-glow-purple"></div>
  <div class="orb orb-tr"></div>

  <div class="presentation-viewport">
    <div class="slide-wrapper" id="slide-wrapper-1"></div>
    <div class="slide-wrapper" id="slide-wrapper-2"></div>
    <div class="slide-wrapper" id="slide-wrapper-3"></div>
    <div class="slide-wrapper" id="slide-wrapper-4"></div>
    <div class="slide-wrapper" id="slide-wrapper-5"></div>
    <div class="slide-wrapper" id="slide-wrapper-6"></div>
    <div class="slide-wrapper" id="slide-wrapper-7"></div>
    <div class="slide-wrapper" id="slide-wrapper-8"></div>
    <div class="slide-wrapper" id="slide-wrapper-9"></div>
    <div class="slide-wrapper" id="slide-wrapper-10"></div>
  </div>

  <script>
    // 1. Mount Slides Shadow DOM roots
    {shadow_slots_js}

    // 2. Setup presentation slide transitions
    let currentSlide = 1;
    const totalSlides = 10;
    
    function showSlide(index, direction) {{
      if (index < 1 || index > totalSlides) return;
      
      const prevActive = document.querySelector('.slide-wrapper.active');
      if (prevActive) {{
        prevActive.classList.remove('active', 'exit-left', 'exit-right');
        if (direction === 'next') {{
          prevActive.classList.add('exit-left');
        }} else if (direction === 'prev') {{
          prevActive.classList.add('exit-right');
        }}
      }}
      
      currentSlide = index;
      const activeSlide = document.getElementById(`slide-wrapper-${{currentSlide}}`);
      activeSlide.classList.remove('exit-left', 'exit-right');
      activeSlide.classList.add('active');
      
      // Update browser history hash
      history.replaceState(null, null, `#slide-${{currentSlide}}`);
    }}
    
    // Keyboard keydown navigator
    document.addEventListener('keydown', e => {{
      if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA' || e.target.isContentEditable) {{
        return; 
      }}
      
      if (e.key === 'ArrowRight' || e.key === ' ' || e.key === 'PageDown' || e.key === 'Enter') {{
        e.preventDefault();
        showSlide(currentSlide + 1, 'next');
      }} else if (e.key === 'ArrowLeft' || e.key === 'PageUp' || e.key === 'Backspace') {{
        e.preventDefault();
        showSlide(currentSlide - 1, 'prev');
      }} else if (e.key === 'Home') {{
        e.preventDefault();
        showSlide(1, 'prev');
      }} else if (e.key === 'End') {{
        e.preventDefault();
        showSlide(totalSlides, 'next');
      }}
    }});

    // Listen for custom slide redirection messages or internal page actions
    function bindNavigationInterceptors() {{
      for (let i = 1; i <= totalSlides; i++) {{
        const shadowRoot = document.getElementById(`slide-wrapper-${{i}}`).shadowRoot;
        if (!shadowRoot) continue;

        // Redirect standard buttons inside slide 4, etc. to launch dashboard demo
        shadowRoot.querySelectorAll('.launch-demo-btn').forEach(btn => {{
          btn.addEventListener('click', (e) => {{
            e.preventDefault();
            window.location.href = 'demo.html';
          }});
        }});

        // Support clicking nav chevrons inside individual slide files
        shadowRoot.querySelectorAll('.slide-nav-btn').forEach(btn => {{
          btn.addEventListener('click', (e) => {{
            e.preventDefault();
            const isPrev = btn.querySelector('.fa-chevron-left') || btn.classList.contains('prev-slide');
            if (isPrev) {{
              showSlide(currentSlide - 1, 'prev');
            }} else {{
              showSlide(currentSlide + 1, 'next');
            }}
          }});
        }});
      }}
    }}

    // Dynamic fullscreen scaling to preserve 16:9 ratio and fit any window perfectly
    const resizeDeck = () => {{
      const baseWidth = 1280;
      const baseHeight = 720;
      const winWidth = window.innerWidth;
      const winHeight = window.innerHeight;
      
      const scaleX = winWidth / baseWidth;
      const scaleY = winHeight / baseHeight;
      const scale = Math.min(scaleX, scaleY);
      
      const viewport = document.querySelector('.presentation-viewport');
      if (viewport) {{
        viewport.style.transform = `scale(${{scale}})`;
      }}
    }};
    
    window.addEventListener('resize', resizeDeck);
    window.addEventListener('DOMContentLoaded', () => {{
      resizeDeck();
      
      const hash = window.location.hash;
      const slideMatch = hash.match(/#slide-(\\d+)/);
      if (slideMatch) {{
        const slideNum = parseInt(slideMatch[1], 10);
        if (slideNum >= 1 && slideNum <= totalSlides) {{
          showSlide(slideNum, 'next');
          setTimeout(bindNavigationInterceptors, 200);
          return;
        }}
      }}
      showSlide(1, 'next');
      setTimeout(bindNavigationInterceptors, 200);
    }});
  </script>
</body>
</html>"""
with open(slides_path, "w", encoding="utf-8") as f:
    f.write(slides_template)
print("  Successfully compiled slides.html!")

print("\n=== STYLES ADAPTATION SCRIPT COMPLETED (NORMAL MOUSE) ===")

