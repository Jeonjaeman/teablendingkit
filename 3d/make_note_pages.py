"""블렌딩 노트 내지 텍스처(애니메이션용). 실물 내지 원고가 없어 촬영본(s002–s021) 구성을 따라 재구성:
에세이 본문 면 · 괘선 질문 면 · 사진 면 · 제목 면. 뒷면용은 좌우 반전 저장(넘긴 뒤 왼쪽에 놓일 때 바로 보이도록).
실행: python 3d/make_note_pages.py
"""
import os
from PIL import Image, ImageDraw, ImageFont, ImageOps

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEX = os.path.join(ROOT, '3d', 'tex')
PX = 8                                  # px/mm
W, H = 126 * PX, 174 * PX
PAPER = (246, 243, 236)
INK = (52, 44, 38)
GREY = (120, 112, 104)
F = 'C:/Windows/Fonts/'
serif = lambda s: ImageFont.truetype(F + 'HANBatang.ttf', s)
serif_b = lambda s: ImageFont.truetype(F + 'HANBatangB.ttf', s)
mono = lambda s: ImageFont.truetype(F + 'cour.ttf', s)

BODY = ('좋아하는 것을 안다는 건 생각보다 어려운 일입니다. 오늘 마신 한 잔이 어땠는지, 어떤 향이 오래 남았는지, '
        '그 맛이 어떤 기억을 데려왔는지 천천히 적어 보면 조금씩 보이기 시작합니다. 취향은 정답이 아니라 '
        '나에게 맞는 배합을 찾아가는 과정입니다. 같은 원료라도 비율이 달라지면 전혀 다른 차가 되듯이, '
        '같은 하루라도 무엇을 곁에 두느냐에 따라 다른 하루가 됩니다. 이 노트는 그 배합을 기록하는 자리입니다. '
        '좋아하는 것이 더 좋은 일상이 되는 삶, 그 시작은 한 잔을 천천히 들여다보는 일에서 출발합니다.')


def wrap(d, text, font, width):
    lines, cur = [], ''
    for ch in text:
        if d.textlength(cur + ch, font=font) > width:
            lines.append(cur); cur = ch.lstrip()
        else:
            cur += ch
    if cur:
        lines.append(cur)
    return lines


def page(fn):
    im = Image.new('RGB', (W, H), PAPER)
    fn(ImageDraw.Draw(im), im)
    return im


def folio(d, n, right=True):
    f = serif(44)
    d.text(((W - 14 * PX) if right else 14 * PX, H - 12 * PX), str(n), font=f, fill=GREY, anchor='mm')
    d.text((W // 2, H - 12 * PX), '취향의 권리', font=serif(38), fill=GREY, anchor='mm')


def essay(title_no, title):
    def f(d, im):
        m = 16 * PX
        d.text((m, 22 * PX), title_no, font=serif(46), fill=GREY)
        d.text((m + 14 * PX, 22 * PX), title, font=serif_b(62), fill=INK)
        y = 46 * PX
        for ln in wrap(d, BODY * 2, serif(34), W - 2 * m)[:17]:
            d.text((m, y), ln, font=serif(34), fill=INK)
            y += int(6.4 * PX)
        folio(d, title_no.strip('() '), right=False)
    return f


def question(q1, q2):
    def f(d, im):
        m = 16 * PX
        for qy, q in ((22 * PX, q1), (96 * PX, q2)):
            d.ellipse((m, qy + 10, m + 22, qy + 32), fill=INK)
            d.text((m + 6 * PX, qy), q, font=serif(44), fill=INK)
            for k in range(8):
                ly = qy + 14 * PX + k * 8 * PX
                d.line((m, ly, W - m, ly), fill=(196, 190, 180), width=3)
        folio(d, '', right=True)
    return f


def title_page(d, im):
    lines = ['Life', 'is', 'Also', 'a Personal', 'Blend']
    y = 30 * PX
    for ln in lines:
        d.text((W // 2, y), ln, font=mono(78), fill=INK, anchor='mm')
        y += 15 * PX
    d.text((W // 2, H - 40 * PX), '삶이라는 블렌딩', font=serif_b(56), fill=INK, anchor='mm')
    d.text((W // 2, H - 30 * PX), 'The Right To Taste', font=mono(40), fill=GREY, anchor='mm')


def photo_page(src):
    def f(d, im):
        ph = Image.open(src).convert('RGB')
        ph = ImageOps.fit(ph, (W, H), method=Image.LANCZOS, centering=(0.5, 0.5))
        im.paste(ph, (0, 0))
    return f


def blank(d, im):
    d.text((W // 2, H // 2), 'The Right To Taste', font=mono(40), fill=(170, 162, 150), anchor='mm')


pages = {
    'note_in_cover': blank,                                              # 앞표지 안쪽
    'note_p1_front': title_page,
    'note_p1_back': photo_page(os.path.join(ROOT, 'wadiz', 'assets', 'stills', 'still_05.jpg')),
    'note_p2_front': essay('(1) ', '취향은 어디에서 오는가'),
    'note_p2_back': question('오늘 마신 차는 어떤 맛이었나요?', '그 맛이 떠올리게 한 장면은 무엇인가요?'),
    'note_p3_front': essay('(2) ', '천천히 들여다보는 일'),
    'note_p3_back': question('가장 오래 남은 향은 무엇이었나요?', '다음에는 무엇을 더하고 싶나요?'),
    'note_p4_front': essay('(3) ', '나만의 배합'),
}
for name, fn in pages.items():
    im = page(fn)
    if name.endswith('_back') or name == 'note_in_cover':
        im = ImageOps.mirror(im)
    im.save(os.path.join(TEX, name + '.png'))
    print('saved', name)
