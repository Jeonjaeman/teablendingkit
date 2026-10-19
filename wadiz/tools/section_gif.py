"""단락(또는 임의 선택자)을 GIF 로 — CSS 애니메이션 시간과 영상 재생 시간을 프레임마다 직접 맞춰 찍는다.

실행 예:
  python wadiz/tools/section_gif.py d-night.html "#s03" --sec 4 --fps 12
  python wadiz/tools/section_gif.py g-wadiz.html "#g05 .photo" --sec 8
옵션: --sec 길이(4초 배수 권장) · --fps 프레임 · --width 출력 폭(기본 860) · --once (1회 재생 GIF) · --out 경로
출력 기본: docs/wadiz-drafts-preview/gif/<파일>_<선택자>.gif
영상 탐색(seek)이 되도록 Range 지원 정적 서버를 직접 띄운다(python http.server 는 Range 미지원).
"""
import os, re, sys, io, shutil, subprocess, tempfile, threading
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from functools import partial
from PIL import Image
from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class RangeHandler(SimpleHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def send_head(self):
        rng = self.headers.get('Range')
        path = self.translate_path(self.path)
        if not rng or not os.path.isfile(path):
            return super().send_head()
        size = os.path.getsize(path)
        m = re.match(r'bytes=(\d*)-(\d*)', rng)
        start = int(m.group(1) or 0); end = int(m.group(2)) if m.group(2) else size - 1
        end = min(end, size - 1)
        f = open(path, 'rb'); f.seek(start)
        self.send_response(206)
        self.send_header('Content-Type', self.guess_type(path))
        self.send_header('Accept-Ranges', 'bytes')
        self.send_header('Content-Range', f'bytes {start}-{end}/{size}')
        self.send_header('Content-Length', str(end - start + 1))
        self.end_headers()
        self._remain = end - start + 1
        return f

    def copyfile(self, src, dst):
        n = getattr(self, '_remain', None)
        if n is None:
            return super().copyfile(src, dst)
        while n > 0:
            b = src.read(min(65536, n))
            if not b:
                break
            dst.write(b); n -= len(b)


def serve():
    srv = ThreadingHTTPServer(('127.0.0.1', 0), partial(RangeHandler, directory=ROOT))
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv


SET = '''async (t) => {
  for (const a of document.getAnimations()) { a.pause(); a.currentTime = t * 1000; }
  const vs = [...document.querySelectorAll('video')];
  await Promise.all(vs.map(v => new Promise(res => {
    v.pause();
    if (!v.duration || isNaN(v.duration)) return res();
    const tt = v.loop ? (t % v.duration) : Math.min(t, v.duration - 0.04);
    if (Math.abs(v.currentTime - tt) < 0.001) return res();
    const done = () => { v.removeEventListener('seeked', done); requestAnimationFrame(() => res()); };
    v.addEventListener('seeked', done); v.currentTime = tt; setTimeout(res, 4000);
  })));
}'''


def main():
    page, sel = sys.argv[1], sys.argv[2]
    opt = lambda k, d: type(d)(sys.argv[sys.argv.index(k) + 1]) if k in sys.argv else d
    sec, fps, width = opt('--sec', 4.0), opt('--fps', 12), opt('--width', 860)
    once = '--once' in sys.argv
    slug = re.sub(r'[^0-9A-Za-z_-]+', '_', sel).strip('_')
    out = opt('--out', os.path.join(ROOT, 'docs', 'wadiz-drafts-preview', 'gif', f'{page.split(".")[0]}_{slug}.gif'))
    os.makedirs(os.path.dirname(out), exist_ok=True)
    srv = serve(); port = srv.server_address[1]
    tmp = tempfile.mkdtemp()
    try:
        with sync_playwright() as p:
            br = p.chromium.launch(); pg = br.new_page(viewport={'width': 860, 'height': 1400}, device_scale_factor=1)
            pg.goto(f'http://127.0.0.1:{port}/wadiz/{page}', wait_until='load')
            el = pg.locator(sel).first
            # 움직이는 요소는 '안정' 대기에서 막히므로 애니메이션을 먼저 멈추고 JS 로 스크롤
            pg.evaluate("document.getAnimations().forEach(a => a.pause())")
            el.evaluate("e => e.scrollIntoView({block: 'center'})"); pg.wait_for_timeout(800)
            # 영상 전부 메타데이터·데이터 확보
            pg.evaluate('''() => Promise.all([...document.querySelectorAll('video')].map(v => { v.preload = 'auto'; v.removeAttribute('autoplay'); v.pause();
                return v.readyState >= 2 ? 0 : new Promise(r => { v.addEventListener('loadeddata', r, {once:true}); v.load(); setTimeout(r, 6000); }); }))''')
            n = int(round(sec * fps))
            # 캡처 영역은 0초에 한 번만 잡아 고정(떠오르는 요소는 프레임마다 상자 크기가 달라져 GIF 인코딩이 깨진다)
            pg.evaluate(SET, 0); bb = el.bounding_box()
            clip = {'x': max(0, round(bb['x'])), 'y': max(0, round(bb['y'])), 'width': round(bb['width']), 'height': round(bb['height'])}
            for i in range(n):
                pg.evaluate(SET, i / fps)
                Image.open(io.BytesIO(pg.screenshot(clip=clip))).convert('RGB').save(os.path.join(tmp, f'{i:04d}.png'))
            br.close()
        vf = f'scale={width}:-2:flags=lanczos'
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-framerate', str(fps), '-i', os.path.join(tmp, '%04d.png'),
                        '-vf', f'{vf},palettegen=max_colors=192:stats_mode=full', os.path.join(tmp, 'pal.png')], check=True)
        # sierra2_4a 디더가 일부 화면에서 ffmpeg 내부 오류를 내면 bayer 로 다시 시도
        for dither in ('sierra2_4a', 'bayer:bayer_scale=4', 'none'):
            r = subprocess.run(['ffmpeg', '-v', 'error', '-y', '-framerate', str(fps), '-i', os.path.join(tmp, '%04d.png'),
                                '-i', os.path.join(tmp, 'pal.png'), '-lavfi', f'{vf}[x];[x][1:v]paletteuse=dither={dither}',
                                '-loop', '-1' if once else '0', out], capture_output=True)
            if r.returncode == 0:
                break
        else:
            raise RuntimeError(r.stderr.decode(errors='ignore')[-400:])
        print(out, f'{os.path.getsize(out) / 1e6:.2f}MB', f'{n}f@{fps}fps')
    finally:
        shutil.rmtree(tmp); srv.shutdown()


if __name__ == '__main__':
    main()
