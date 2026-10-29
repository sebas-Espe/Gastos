"""Ajustes a la carpeta android/ recién creada: permisos, icono y color de la barra."""
import os, re, shutil, subprocess, sys
subprocess.run([sys.executable, '-m', 'pip', 'install', '--quiet', 'pillow'], check=True)
from PIL import Image

root = os.path.join(os.path.dirname(__file__), '..')
android = os.path.join(root, 'android')

# 1) Permisos de cámara (para fotografiar comprobantes)
mp = os.path.join(android, 'app/src/main/AndroidManifest.xml')
s = open(mp, encoding='utf-8').read()
if 'android.permission.CAMERA' not in s:
    s = s.replace('<application', '<uses-permission android:name="android.permission.CAMERA" />\n    <uses-feature android:name="android.hardware.camera" android:required="false" />\n\n    <application', 1)
    open(mp, 'w', encoding='utf-8').write(s)

# 2) Icono de la app
res = os.path.join(android, 'app/src/main/res')
src = Image.open(os.path.join(root, 'icon.png')).convert('RGBA')
sizes = {'mdpi': 48, 'hdpi': 72, 'xhdpi': 96, 'xxhdpi': 144, 'xxxhdpi': 192}
for d, px in sizes.items():
    folder = os.path.join(res, 'mipmap-' + d)
    os.makedirs(folder, exist_ok=True)
    img = src.resize((px, px), Image.LANCZOS)
    for n in ('ic_launcher.png', 'ic_launcher_round.png', 'ic_launcher_foreground.png'):
        img.save(os.path.join(folder, n))
shutil.rmtree(os.path.join(res, 'mipmap-anydpi-v26'), ignore_errors=True)

# 3) Barra de estado con el color de la app
for sp in [os.path.join(res, 'values/styles.xml')]:
    if os.path.exists(sp):
        t = open(sp, encoding='utf-8').read()
        if 'statusBarColor' not in t:
            t = t.replace('<style name="AppTheme.NoActionBar" parent="Theme.AppCompat.DayNight.NoActionBar">',
                          '<style name="AppTheme.NoActionBar" parent="Theme.AppCompat.DayNight.NoActionBar">\n        <item name="android:statusBarColor">#0B3C5D</item>', 1)
            open(sp, 'w', encoding='utf-8').write(t)
print('Android listo')
