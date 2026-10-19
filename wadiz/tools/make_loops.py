"""GIF 변환용 '이음새 없는 짧은 루프' 영상 만들기 → wadiz/assets/loop/

규칙: 모든 루프 길이는 4초 기준(2·4·8초)이라 CSS 모션(4초 주기)과 함께 캡처해도 이음새가 없다.
- 3D 클립: 렌더 프레임(3d/anim/)으로 왕복 루프 (열림→닫힘, 펼침→접힘, 넘김→되돌림, 회전 8초)
- 실사 클립: 컷이 섞인 클립은 가장 긴 단일 샷만 쓰고, 끝 F초를 처음과 크로스페이드해 이음새 제거(2·4초)
실행: python wadiz/tools/make_loops.py
"""
import os, glob, shutil, subprocess, tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ANIM = os.path.join(ROOT, '3d', 'anim')
CLIPS = os.path.join(ROOT, 'wadiz', 'assets', 'video', 'clips')
OUT = os.path.join(ROOT, 'wadiz', 'assets', 'loop')
FPS = 24
W = 1280
ENC = ['-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '21', '-preset', 'slow', '-movflags', '+faststart', '-an']


def res(a, b, n):
    """프레임 a..b(포함)를 n장으로 고르게 리샘플."""
    if n == 1:
        return [a]
    return [round(a + (b - a) * i / (n - 1)) for i in range(n)]


# 3D 왕복 루프: (이름, 소스 클립, 프레임 순서, 포스터 프레임 위치 0~1)
def plan_3d():
    return {
        # 닫힘 유지 → 열림 → 열린 채 유지 → 닫힘   (4초 = 96f)
        'lid_loop': ('lid_open', [1] * 8 + res(15, 76, 34) + [108] * 20 + res(76, 15, 34), 0.55),
        # 접힘 → 펼침 → 펼친 채 → 접힘            (4초)
        'acc_unfold_loop': ('acc_unfold', [1] * 6 + res(15, 106, 42) + [132] * 12 + res(106, 15, 36), 0.55),
        # 한 장씩 넘김 → 되돌림                     (8초 = 192f)
        'acc_flip_loop': ('acc_flip', res(1, 216, 108) + res(216, 1, 84), 0.40),
        # 표지 열고 세 장 넘김 → 되돌려 덮음         (8초)
        'note_flip_loop': ('note_flip', res(1, 190, 120) + res(178, 1, 72), 0.60),
        # 360° 회전                               (8초, 마지막→처음 이어짐)
        'rotate_loop': ('rotate', [1 + (i * 144) // 192 for i in range(192)], 0.0),
    }


def build_3d(name, clip, seq, poster):
    frames = sorted(glob.glob(os.path.join(ANIM, clip, '*.png')))
    assert frames, clip
    tmp = tempfile.mkdtemp()
    try:
        for i, f in enumerate(seq):
            shutil.copy(frames[f - 1], os.path.join(tmp, f'{i:04d}.png'))
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-framerate', str(FPS), '-i', os.path.join(tmp, '%04d.png'),
                        '-vf', f'scale={W}:-2', *ENC, os.path.join(OUT, name + '.mp4')], check=True)
        pf = os.path.join(tmp, f'{round(poster * (len(seq) - 1)):04d}.png')
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', pf, '-vf', f'scale={W}:-2', '-q:v', '3',
                        os.path.join(OUT, name + '.jpg')], check=True)
    finally:
        shutil.rmtree(tmp)
    print(f'{name:18s} {len(seq) / FPS:.1f}s')


def dur(path):
    return float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
                                          '-of', 'csv=p=0', path]).strip())


def longest_shot(path, thr=30.0):
    """장면 전환(컷)을 찾아 가장 긴 단일 샷의 프레임 구간 [a, b) 를 돌려준다."""
    import numpy as np
    w, h = 320, 180
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', path, '-vf', f'scale={w}:{h}', '-f', 'rawvideo',
                          '-pix_fmt', 'gray', '-'], capture_output=True).stdout
    f = np.frombuffer(raw, np.uint8).reshape(-1, h, w).astype(np.float32)
    d = np.abs(np.diff(f, axis=0)).mean(axis=(1, 2))
    cuts = [0] + [i + 1 for i, v in enumerate(d) if v > thr] + [len(f)]
    segs = [(cuts[i] + (1 if i else 0), cuts[i + 1] - (1 if i + 2 < len(cuts) else 0)) for i in range(len(cuts) - 1)]
    a, b = max(segs, key=lambda s: s[1] - s[0])
    return a, b, len(f)


def build_clip(path):
    """가장 긴 단일 샷만 잘라 크로스페이드 루프(2·4초)로. 많이 늘려야 하면 움직임 보간으로 끊김 완화."""
    name = os.path.splitext(os.path.basename(path))[0]
    a, b, n = longest_shot(path)
    src_fps = 24000 / 1001
    L = (b - a) / src_fps
    T, F = (4.0, 0.4) if L >= 3.0 else (2.0, 0.3)
    s = L / (T + F)                     # 재생 속도(1 미만 = 느리게)
    interp = f',minterpolate=fps={FPS}:mi_mode=mci:mc_mode=aobmc:me_mode=bidir' if s < 0.8 else f',fps={FPS}'
    fc = (f'[0:v]trim=start_frame={a}:end_frame={b},setpts=PTS-STARTPTS,setpts=PTS/{s:.6f}{interp},'
          f'scale={W}:-2,split[a][b];'
          f'[a]trim=0:{T},setpts=PTS-STARTPTS[m];'
          f'[b]trim={T}:{T + F},setpts=PTS-STARTPTS[t];'
          f'[t][m]xfade=transition=fade:duration={F}:offset=0,format=yuv420p')
    out = os.path.join(OUT, name + '.mp4')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', path, '-filter_complex', fc, *ENC, out], check=True)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{T / 2}', '-i', out, '-frames:v', '1', '-q:v', '3',
                    os.path.join(OUT, name + '.jpg')], check=True)
    print(f'{name:18s} {T:.1f}s  shot {a}-{b}/{n}f ({L:.2f}s) speed x{s:.2f}{" +interp" if s < 0.8 else ""}')


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    for n, (clip, seq, poster) in plan_3d().items():
        build_3d(n, clip, seq, poster)
    for p in sorted(glob.glob(os.path.join(CLIPS, 'c*.mp4'))):
        build_clip(p)
