"""
Run from inside your Portfeuille project folder:
    pip install qrcode[pil] --break-system-packages
    python3 generate_main_qr.py
"""
import qrcode

qr = qrcode.QRCode(
    version=None,
    error_correction=qrcode.constants.ERROR_CORRECT_M,
    box_size=10,
    border=2,
)
qr.add_data('https://angrywatership.github.io/Portfeuille/')
qr.make(fit=True)
img = qr.make_image(fill_color='black', back_color='white')
img.save('qr-main.png')
print('✓ qr-main.png  →  https://angrywatership.github.io/Portfeuille/')