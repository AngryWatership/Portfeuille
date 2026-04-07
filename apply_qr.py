"""
Run this from inside your Portfeuille project folder:

    python3 apply_qr.py

It will:
1. Generate all 22 QR PNG files into /qr/
2. Update the CSS and HTML in each numbered subfolder's index.html

Prerequisites:
    pip install qrcode[pil]
"""

import os
import qrcode

BASE = 'https://angrywatership.github.io/Portfeuille'

# ── STEP 1: Generate QR PNGs ─────────────────────────
os.makedirs('qr', exist_ok=True)

pages = []
for i in range(1, 12):
    pages.append((f'qr-{i}',    f'{BASE}/{i}/'))
    pages.append((f'qr-{i}-fr', f'{BASE}/{i}-fr/'))

for name, url in pages:
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=2,
    )
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color='black', back_color='white')
    img.save(f'qr/{name}.png')
    print(f'✓ qr/{name}.png  →  {url}')

print(f'\n{len(pages)} QR codes generated in /qr/\n')

# ── STEP 2: CSS + HTML replacements ──────────────────

CSS_OLD = """.qr-placeholder {
  position:absolute;
  top:1.5mm;
  right:1.5mm;
  width:22.5mm;
  height:22.5mm;
  background:var(--ph);
  border:1.5px dashed #bbb;
  border-radius:1.5mm;
  display:flex;
  flex-direction:column;
  align-items:center;
  justify-content:center;
  gap:1mm;
  z-index:20;
}
.qr-placeholder span {
  font-family:'DM Mono',monospace;
  font-size:5pt;
  color:#aaa;
  letter-spacing:.12em;
  text-transform:uppercase;
  text-align:center;
  line-height:1.6;
}"""

CSS_NEW = """.qr-placeholder {
  position:absolute;
  top:1.5mm;
  right:1.5mm;
  width:19mm;
  z-index:20;
}
.qr-placeholder img {
  width:100%;height:auto;display:block;
}"""

HTML_OLD = '  <div class="qr-placeholder"><span>QR<br>Code</span></div>'

# Map folder -> qr filename
folder_to_qr = {}
for i in range(1, 12):
    folder_to_qr[str(i)]    = f'qr-{i}.png'
    folder_to_qr[f'{i}-fr'] = f'qr-{i}-fr.png'

updated = []
skipped = []

for folder, qr_file in folder_to_qr.items():
    path = os.path.join(folder, 'index.html')
    if not os.path.exists(path):
        skipped.append(path)
        continue

    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()

    html = html.replace(CSS_OLD, CSS_NEW)
    html = html.replace(
        HTML_OLD,
        f'  <div class="qr-placeholder"><img src="../qr/{qr_file}" alt="QR"></div>'
    )

    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)

    updated.append(path)
    print(f'✓ {path}  →  ../qr/{qr_file}')

print(f'\n{len(updated)} files updated.')
if skipped:
    print(f'Skipped (not found): {skipped}')

print('\nNow run:')
print('  git add qr/ */index.html')
print('  git commit -m "add qr codes"')
print('  git push origin main')