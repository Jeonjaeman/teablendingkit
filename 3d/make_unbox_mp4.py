"""3d/anim/unbox_<ver>/####.png(4초) → 앞으로 + 거꾸로 이어 8초 끊김 없는 루프 mp4 + 포스터(마지막 = 플랫레이).
실행: python 3d/make_unbox_mp4.py [taste|depth]
출력: wadiz/assets/loop/unbox_<ver>.mp4, .jpg
"""
import os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ver = sys.argv[1] if len(sys.argv) > 1 else 'taste'
src = os.path.join(ROOT, '3d', 'anim', f'unbox_{ver}')
dst = os.path.join(ROOT, 'wadiz', 'assets', 'loop')
os.makedirs(dst, exist_ok=True)
frames = sorted(f for f in os.listdir(src) if f.endswith('.png'))
# 앞으로(1~97) + 거꾸로(96~2) = 192프레임 = 8초. 양 끝 프레임은 한 번씩만 → 이음매 없음
fc = '[0:v]split[a][b];[b]reverse,trim=start_frame=1:end_frame=%d,setpts=PTS-STARTPTS[r];[a][r]concat=n=2:v=1[v]' % (len(frames) - 1)
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-framerate', '24', '-i', os.path.join(src, '%04d.png'),
                '-filter_complex', fc, '-map', '[v]', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '21',
                '-preset', 'slow', '-movflags', '+faststart', '-an', os.path.join(dst, f'unbox_{ver}.mp4')], check=True)
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', os.path.join(src, frames[-1]), '-q:v', '3',
                os.path.join(dst, f'unbox_{ver}.jpg')], check=True)
print('encoded', ver, len(frames), '→', 2 * len(frames) - 2, 'frames')
