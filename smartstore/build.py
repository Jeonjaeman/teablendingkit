# detail.html 조립: 와디즈 E안(e-editorial.html)의 <head>·CSS를 그대로 가져오고, 본문은 body.html을 붙인다.
# E안 CSS를 고치면 다시 실행하면 된다. 사용: python smartstore/build.py
import re, pathlib

R = pathlib.Path(__file__).resolve().parent.parent
e = (R / 'wadiz/e-editorial.html').read_text(encoding='utf-8').split('\n')
end = next(i for i, l in enumerate(e) if l.strip() == '</style>')
head = '\n'.join(e[:end])  # <!DOCTYPE> ~ 마지막 CSS 규칙까지 (</style> 앞)
head = re.sub(r'<title>.*?</title>', '<title>취향의 권리 티블렌딩 키트 · 스마트스토어 상세</title>', head, flags=re.S)
head = head.replace('<head>', '<head>\n<!-- 스마트스토어 상세 — 와디즈 E안 CSS 그대로 + 대표 원고(11/6) 순서. 가격·펀딩·인물 소개 없음, Taste/Depth, 효능 문구 없음. 본문은 body.html, 조립은 build.py -->', 1)

over = '''
/* ───────── 스마트스토어용 덧붙임 (E안 CSS는 위에 그대로) ─────────
   688px로 짜고 1.25배(device scale)로 찍어 가로 860px 이미지를 만든다 → 본문 16px이 20px로 읽힌다. */
.page{width:688px;padding:0 32px}
:root{--col:144px}
.bleed{margin:0 -32px}
.gifslot img{width:100%;height:auto}
.url{font:700 34px/1.15 var(--f-sans);letter-spacing:-.04em}
.links .url{font-size:30px}
.rows .p2{margin-top:4px;font-size:15px;line-height:1.7}
.howto td{font-size:17px}
.ingtbl td.art img{width:56px;height:56px;object-fit:cover}
.ver .vn{font-size:24px}
</style>
</head>
<body>
'''
body = (R / 'smartstore/body.html').read_text(encoding='utf-8')
(R / 'smartstore/detail.html').write_text(head + over + body + '\n</body>\n</html>\n', encoding='utf-8')
print('detail.html built')
