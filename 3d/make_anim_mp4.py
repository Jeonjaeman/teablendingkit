"""3d/anim/<clip>/####.png → wadiz/assets/3d/anim/<clip>.mp4 (+ 포스터 jpg). lid_close 는 lid_open 역재생.
실행: python 3d/make_anim_mp4.py
"""
import os, subprocess, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, '3d', 'anim')
DST = os.path.join(ROOT, 'wadiz', 'assets', '3d', 'anim')
os.makedirs(DST, exist_ok=True)

# (출력명, 소스 클립, 역재생, 포스터 = 소스 프레임 위치 0~1)
# 포스터는 정지 캡처(와디즈 업로드)에 그대로 남으므로 컷을 가장 잘 보여 주는 프레임을 쓴다
JOBS = [
    ('rotate', 'rotate', False, 0.0),
    ('lid_open', 'lid_open', False, 1.0),
    ('lid_close', 'lid_open', True, 1.0),
    ('acc_unfold', 'acc_unfold', False, 1.0),
    ('acc_flip', 'acc_flip', False, 0.62),
    ('note_flip', 'note_flip', False, 1.0),
]
ENC = ['-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '21', '-preset', 'slow', '-movflags', '+faststart', '-an']

for out, clip, rev, pos in JOBS:
    frames = sorted(glob.glob(os.path.join(SRC, clip, '*.png')))
    if not frames:
        print('skip', out); continue
    vf = 'reverse' if rev else 'null'
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-framerate', '24', '-i', os.path.join(SRC, clip, '%04d.png'),
                    '-vf', vf, *ENC, os.path.join(DST, out + '.mp4')], check=True)
    pf = frames[round(pos * (len(frames) - 1))]
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', pf, '-q:v', '3', os.path.join(DST, out + '.jpg')], check=True)
    print('encoded', out, len(frames), 'frames')
