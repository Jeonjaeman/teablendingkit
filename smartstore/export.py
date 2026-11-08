# detail.html을 업로드용 이미지로 내보낸다.
# 688px 레이아웃을 1.25배로 찍어 가로 860px. GIF 자리(.gifslot)에서 끊고 그 자리에 gif/ 원본을 끼운다.
# 정지 구간이 세로 5,000px을 넘으면 섹션 경계에서 나눈다. 쿠팡용 GIF 정지컷은 out/still/.
# 사용: python smartstore/build.py && python smartstore/export.py
import asyncio, shutil, pathlib
from PIL import Image
from playwright.async_api import async_playwright

ROOT = pathlib.Path(__file__).resolve().parent
OUT = ROOT / 'out'
SCALE = 1.25
MAX_H = 5000
Image.MAX_IMAGE_PIXELS = None

async def main():
    (OUT / 'still').mkdir(parents=True, exist_ok=True)
    for f in [*OUT.glob('*.jpg'), *OUT.glob('*.gif'), *(OUT / 'still').glob('*.jpg')]: f.unlink()
    full = OUT / '_full.png'
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={'width': 688, 'height': 1000}, device_scale_factor=SCALE)
        await pg.goto((ROOT / 'detail.html').as_uri())
        await pg.wait_for_load_state('networkidle')
        await pg.evaluate('document.fonts.ready')
        await pg.wait_for_timeout(1000)
        gifs = await pg.evaluate('''[...document.querySelectorAll('.gifslot')].map(e=>{const r=e.getBoundingClientRect();return {top:r.top+scrollY,bottom:r.bottom+scrollY,src:e.dataset.gif}})''')
        secs = await pg.evaluate('''[...document.querySelectorAll('.sec,.foot')].map(e=>e.getBoundingClientRect().top+scrollY)''')
        await pg.screenshot(path=str(full), full_page=True)
        await b.close()

    im = Image.open(full).convert('RGB')
    W, H = im.size
    px = lambda y: round(y * SCALE)
    cuts = sorted({px(y) for y in secs if 0 < px(y) < H})
    seq, y, n = [], 0, 1

    def still(a, b):
        nonlocal n
        while b - a > 0:
            end = b
            if end - a > MAX_H:  # 5,000px 안쪽의 마지막 섹션 경계에서 자른다
                cand = [c for c in cuts if a + 600 < c <= a + MAX_H]
                end = cand[-1] if cand else a + MAX_H
            fn = f'{n:02d}_detail.jpg'
            im.crop((0, a, W, end)).save(OUT / fn, quality=92, optimize=True)
            seq.append((fn, W, end - a)); n += 1; a = end

    for g in gifs:
        still(y, px(g['top']))
        fn = f'{n:02d}_{pathlib.Path(g["src"]).stem}.gif'
        shutil.copy(ROOT / g['src'], OUT / fn)
        gw, gh = Image.open(ROOT / g['src']).size
        im.crop((0, px(g['top']), W, px(g['bottom']))).save(OUT / 'still' / fn.replace('.gif', '_still.jpg'), quality=92)
        seq.append((fn, gw, gh)); n += 1
        y = px(g['bottom'])
    still(y, H)
    full.unlink()
    for fn, w, h in seq:
        print(f'{fn:28s} {w}x{h}  {(OUT / fn).stat().st_size / 1e6:.2f}MB')

asyncio.run(main())
