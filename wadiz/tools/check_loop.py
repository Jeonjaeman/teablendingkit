"""GIF 루프 점검: 단락마다 모든 CSS 애니메이션을 t=0 과 t=주기(4초)로 맞춰 찍어 같은지 비교한다.
영상은 멈추고 가린다(영상 루프는 make_loops.py 가 따로 보장, 재생 시점 흔들림이 판정에 끼지 않게). 주기를 4초 배수로 안 맞춘 모션이 있으면 '불일치'.
실행: python wadiz/tools/check_loop.py d-night.html [--out 폴더]   (로컬 서버 http://localhost:8777 필요)
"""
import sys, io, os, json
import numpy as np
from PIL import Image
from playwright.sync_api import sync_playwright

page = sys.argv[1]
out = sys.argv[sys.argv.index('--out') + 1] if '--out' in sys.argv else None
PERIOD = 4000
SET = '''(t) => { document.querySelectorAll('video').forEach(v => { v.pause(); v.style.visibility = 'hidden'; });
  for (const a of document.getAnimations()) { a.pause(); a.currentTime = t; } return document.getAnimations().length; }'''
with sync_playwright() as p:
    br = p.chromium.launch(); pg = br.new_page(viewport={'width': 860, 'height': 1200})
    pg.goto(f'http://localhost:8777/wadiz/{page}', wait_until='load'); pg.wait_for_timeout(1500)
    info = pg.evaluate('''() => { const s=[...document.querySelectorAll('section, .hero, header')].filter(e=>e.offsetHeight>40);
      const durs=[...new Set(document.getAnimations().map(a=>a.effect && a.effect.getComputedTiming().duration))];
      return {n:s.length, durs, sw:document.documentElement.scrollWidth}; }''')
    print('animations durations(ms):', info['durs'], '| scrollWidth', info['sw'])
    bad = []
    secs = pg.query_selector_all('section')
    for i, el in enumerate(secs):
        if not el.bounding_box() or el.bounding_box()['height'] < 40:
            continue
        el.scroll_into_view_if_needed()
        n = pg.evaluate(SET, 0); a = np.asarray(Image.open(io.BytesIO(el.screenshot())).convert('L'), np.float32)
        pg.evaluate(SET, PERIOD); b = np.asarray(Image.open(io.BytesIO(el.screenshot())).convert('L'), np.float32)
        same = a.shape == b.shape and np.abs(a - b).mean() < 0.3
        # 움직임: 주기 안 여러 시점(0.5·1·1.5·2·3초)과 비교해 가장 큰 차이
        moving, c = False, None
        for t in (500, 1000, 1500, 2000, 3000):
            pg.evaluate(SET, t); im = Image.open(io.BytesIO(el.screenshot())).convert('RGB')
            if t == 2000: c = im
            g = np.asarray(im.convert('L'), np.float32)
            if g.shape == a.shape and np.abs(a - g).mean() > 0.02: moving = True
        sid = el.get_attribute('id') or f'#{i}'
        print(f'{sid:10s} loop {"OK " if same else "MISMATCH"}  motion {"yes" if moving else "no"}')
        if not same: bad.append(sid)
        if out:
            os.makedirs(out, exist_ok=True); c.save(os.path.join(out, f'{page}_{i:02d}_{sid}.jpg'), quality=80)
    br.close()
print("MISMATCH sections:", bad or "none")
