# 와디즈 상세페이지 — 세트 2 제작 브리프 (전혀 다른 스타일 3종 · 실서비스 수준)

세트 1(a/b/c)은 셋 다 "미장 아이보리 + 세리프 + 다크 브라운 밴드"라 같은 디자인으로 보였다. 세트 2는 **배경색·서체 조합·사진 처리·포인트색·컴포넌트 형태**를 전부 다르게 해서 썸네일만 봐도 다른 브랜드처럼 보여야 하고, **이소연 대표에게 그대로 보여 주고 고르게 할 완성본**이어야 한다.

산출물: `d-night.html` · `e-editorial.html` · `f-garden.html` (각 단일 HTML, 860px, 외부 JS 없음, CSS 인라인).
카피·순서는 `BRIEF.md` §3(16섹션)을 따르되, **아래 §2의 확정 내용으로 덮어쓴다.** `BRIEF.md` §1 토큰·§5 스타일은 무시.

---

## 1. 실서비스 규칙 (가장 중요)

1. **작업용 표기 전면 금지.** `GIF · 03_창가독서.gif`, `PLACEHOLDER`, `새로 촬영 A-1`, `[최종 확인]`, `[수량]`, `data-gif/data-shot/data-tbd` 라벨, 점선 빈 박스 — 화면에 보이는 것은 전부 금지. 교체가 필요한 지점은 **HTML 주석**(`<!-- TODO: … -->`)으로만 남긴다.
2. **모든 이미지 자리는 실제 이미지로 채운다.** 소재는 §3의 실제 영상 클립·실제 스틸·생성 이미지뿐. 빈 박스를 남기느니 그 요소를 디자인적으로 재구성한다(예: 인물 사진 대신 저서 사진과 서명 타이포).
3. **영상은 `<video autoplay muted loop playsinline preload="metadata" poster="…">`** 로 실제 재생. 와디즈 업로드용 GIF 변환은 나중 공정 — 지금은 HTML에서 실제로 움직여야 한다.
4. 글자는 전부 HTML 텍스트(이미지 안 글자 금지), 숫자·그래프·배지는 CSS/SVG.
5. 폭 860px 고정, 가로 넘침 0, 콘솔 에러 0, 모든 `src` 실존 파일.
6. 표현 가드: "카페인 0" 단정 금지 → "허브와 곡물로만 구성" / "커피 대신·대체" 금지 → "커피를 마시던 시간에 제안하는 새로운 한 잔" / 건강·효능 표현 금지. 판매·회사 언어 금지.
7. 한글 본문 16px 이상, `word-break:keep-all`. 폰트는 Google Fonts(Noto Serif KR 300/400/600 · Noto Sans KR 300/400/500/700 · Cormorant Infant 300/400/500 + italic · Courier Prime).
8. 완료 전: `ls`로 `src` 대조, `grep -c "<section"` 17, `grep -ci "placeholder\|data-gif\|data-shot\|\[수량\]\|최종 확인"` = 0. 보고 10줄 이내.

## 2. 내용 확정값 (BRIEF.md §3 위에 덮어쓰기)

- 제품명: **VER.1 HERB / VER.2 GRAIN / TWO KIT SET** (대표 시안 표기).
- VER.2 원료 6종: **둥굴레 · 찰수수 · 단팥 · 현미 · 민들레 뿌리 · 보리** (통보리 아님). 보태니컬: 현미 = `botanical-clean/brown-rice.png`, 보리 = `barley.png`.
- s04 숫자: **12** 두 버전을 합친 재료 가짓수 / **허브와 곡물로만** 저녁에도 편하게 / **약 27잔** 150ml 기준, 키트 하나로 / **2** HERB와 GRAIN, 두 가지 시작점.
- s08 레시피 카드 3장 (전부 실제 레시피):
  ① `VER.1 · TEA BLENDER'S RECIPE` **로즈가든** — 캐모마일 2 : 장미 1 : 레몬밤 1 — 95~100°C · 150ml · 3~5분
  ② `VER.1 + VER.2 · 교차 블렌드` **유자 로스트** — 유자 1 : 민들레 뿌리 2 : 단팥 1 — 100°C · 150ml · 7~10분 — "유자의 밝은 첫 향 뒤에 깊은 볶음 향과 부드러운 고소함이 이어지는 시트러스 로스트."
  ③ `VER.2 · ROASTER'S RECIPE` **브라질리언 로스트** — 민들레 뿌리 2 : 단팥 2 : 찰수수 1 : 둥굴레 ½ — 100°C · 150ml · 10분 이상 — "깊게 볶은 듯한 첫 향에 단팥과 찰수수의 부드러운 구수함이 이어집니다."
- 원료 12종 향·바디·여운(5점): 레몬밤 4·2·3 / 히비스커스 3·3·4 / 페퍼민트 5·2·4 / 유자 4·2·3 / 장미 5·3·5 / 캐모마일 3·2·3 / 둥굴레 2·4·3 / 찰수수 2·3·3 / 단팥 3·4·4 / 현미 2·3·2 / 민들레 뿌리 4·5·5 / 보리 3·3·3. 원료 한 줄 설명은 `shared/product-data.js`(현미: "볶은 쌀의 담백하고 고소한 향. 바디를 받쳐 줍니다.").
- s08b 레이더(로즈 가든 결과): 향 5 · 바디 2 · 단맛 3 · 고소함 1 · 산뜻함 4.
- s10 만든 사람: 인물 사진 없이 구성. 저서 2권 사진(`stills/still_03.jpg`, `still_04.jpg`) + 이름·경력 + 인용구. 로스터는 이름만.
- s11 체험단 후기: **가짜 후기 문장 금지.** 카드 3장은 "VER.1 HERB / VER.2 GRAIN / SET"를 쓴 세 체험단의 자리로 디자인하고, 카드 본문은 "오픈 전 체험단 20명의 첫 잔 이야기를 이 자리에 싣습니다." 한 줄 + 노트 사진(`gen/notes_three.png`를 3분할 크롭 또는 `stills/still_14.jpg`·`still_15.jpg`·`still_17.jpg`).
- s13 리워드: R1 울트라 얼리버드 · 선착순 100명 · 50,150원(정가 59,000) 15% / R2 슈퍼 얼리버드 · 한정 수량 · 54,870원 7% / R3 얼리버드 · 59,000원 / R4 TWO KIT SET · 한정 수량 · 가격 "오픈 시 공개" · VER.1 + VER.2 + 블렌딩 노트 2권 + 교차 레시피 가이드. 혜택 목록은 BRIEF 그대로. 공통 안내 문장 유지.
- s14 이벤트: 날짜 칸 없이 "참여 기간: 펀딩 기간 중 · 당첨자 발표: 펀딩 종료 후 공식 인스타그램과 개별 DM". 경품: 티아포테카 차 4종 — 단팥차, 골든 모과, 그리고 두 가지(이름은 "두 가지 시그니처"로 표기).
- s15 FAQ 6문항(보관 포함) + 제품 상세정보 표: 값은 "펀딩 오픈 시 표기" 로 통일(빈칸·대괄호 금지).
- s16 QR: OFFICIAL SITE = `assets/qr-site.svg` 실제 QR. YOUTUBE 는 QR 대신 "YouTube · 취향의 권리" 텍스트 버튼.
- s01 이벤트 띠, s01-2 비교 두 잔, s02 공감 3문항, s03 키트, s05 두 버전+SET, s06 3단계, s07 TODAY/SOMEDAY, s09 기록, s12 선물: 카피는 BRIEF §3 그대로.

## 3. 실제 소재 (경로는 `wadiz/` 기준) — 전부 실존

### 영상 클립 (브랜드 필름 2차 편집본에서 추출, 1720×968, 무음, 2~5초, 각 0.2MB) — `assets/video/clips/`
| 파일 | 장면 | 쓰는 곳 |
|---|---|---|
| `c03_window_read.mp4` | 창가 테이블의 여성, 책을 넘김 | **s01 히어로 배경** |
| `c09_pour_water.mp4` | 유리 티팟에 물 붓기 | s01-2 상단 |
| `c02_books.mp4` | 책 2권과 도구 | s03 |
| `c05_jars_spoon.mp4` | 유리병 5개, 스푼으로 원료 담기 | s05 상단 |
| `c01_teapot.mp4` | 손이 티팟을 내려놓음 | s05 SET |
| `c06_smell.mp4` | 병에 코를 대고 향 맡기 | s06 |
| `c08_canister.mp4` | 원료 캐니스터 클로즈업 | s06 |
| `c10_rest.mp4` | 티팟 옆에 엎드려 쉬는 여성 | s07 |
| `c11_brew_closeup.mp4` | 우러나는 차 클로즈업 | s08 |
| `c07_write.mp4` | 노트에 펜으로 쓰기 | s09 |
| `c13_smile.mp4` | 미소 | s12 |
| `c12_window_sit.mp4` | 창가에 앉은 여성 | s16 |
| `c14_ending.mp4` | 빛 번짐 → 로고 등장 | s16 엔딩 |
| `c04_pour_cup.mp4` | 컵에 따르기 | 예비 |
각 클립의 포스터 `assets/video/clips/{같은이름}.jpg`.

### 실제 스틸 28장 (2950×1659) — `assets/stills/still_01.jpg` ~ `still_28.jpg`
01 티팟 내려놓는 손 · 02 책 표지 타이포 클로즈업 · 03 책 2권(다크 커버) · 04 책 표지(아이보리) · 05 티팟과 유리병 · 06 창가 테이블 손 · 07 여성 옆모습 · 08 원료를 티백에 담기 · 09 손바닥 위 원료 · 10·11 유리병 5개와 스푼 · 12 향 맡기 · 13 캐니스터에 담기 · 14 노트에 쓰기 · 15 책 넘기기 · 16 창가에서 향 맡기 · 17 티백 들여다보기 · 18 유리병 클로즈업 · 19 물 붓기 · 20 차 클로즈업(아래) · 21 티팟 옆 휴식 · 22 우러나는 차 · 23·24 창가에 앉음 · 25 차 마시기 · 26 옆모습 미소 · 27 빛 번짐 · 28 창가 전경.

### 생성 이미지 (ComfyUI · Flux, 글자 없음) — `assets/gen/`
`cups_two.png`(비교 두 잔, 1200×800) · `grain_closeup.png`(곡물 6종 유리볼) · `kit_flatlay.png`(구성품 플랫레이 1200×900) · `red_bean_tea.png`(단팥차 1000×1000) · `package_gift.png`(크래프트백·박스·엽서·태그) · `prize_teas.png`(차 4종 틴) · `notes_three.png`(노트 3권) · `hero_dark.png`(다크 티팟 1200×1500, D 전용) · `garden_hero.png`(보태니컬 서클 플랫레이 1200×1500, F 전용).

### 기존 에셋
`assets/logo.png`(세로 락업 투명) · `assets/emblem.svg` · `assets/qr-site.svg` · `assets/botanical-clean/{lemon-balm,hibiscus,peppermint,yuza,rose,chamomile,solomons-seal,sorghum,red-bean,brown-rice,dandelion-root,barley}.png`(글자 없는 수채) · `assets/photo/`(box-front, accordion=세워 둔 책, book-standing=책 여러 권, book-3view=원료 카드 시트, jars, hands-herbs, hero-bowl, pour, cup-linen, sunset-table, teapot-flatlay, depth-dishes, pouch, bookmark=노을 풍경 책갈피, m-blend, m-botanical).
**미장 텍스처(`plaster-*`)는 세트 2에서 금지**(F의 크림 쉼 구간 25% 투명만 예외).

---

## 4. 스타일 D · `d-night.html` — "밤의 약방 (Dark Apothecary)"
한밤의 티 아포테카. 어두운 바탕에 촛불 같은 따뜻한 빛. 레퍼런스: 티어 엑스트레 드 파퓸(검정 밴드), 스코르자(다크 브라운 풀블리드), 위스키·향수 상세 문법.
```css
:root{--bg:#15130F;--bg-2:#201C16;--panel:#2A241C;--line:#3B342A;--text:#EFE7D8;--text-2:#B9AE9A;--muted:#7E7465;
--gold:#C9A961;--gold-soft:#8C7445;--ember:#B8653A;--herb:#9DB08F;--grain:#C9A961;
--f-kserif:"Noto Serif KR",serif;--f-kr:"Noto Sans KR",sans-serif;--f-eng:"Cormorant Infant",serif;--f-type:"Courier Prime",monospace;}
```
- 전 구간 다크. 밝은 면은 사진·영상뿐. 영상·사진에 `filter:brightness(.82) contrast(1.06) saturate(.9)` + 위아래 `--bg`로 녹아드는 그라데이션 오버레이.
- 히어로: `hero_dark.png`를 배경으로 쓰거나 `c03_window_read.mp4` 위에 어두운 오버레이 55%. 흰 세리프 카피.
- 보태니컬 수채는 검정 카드 위 **원형 비네트**(원형 마스크, 안쪽 그림자, 골드 0.5px 링). 영문 라벨 골드 이탤릭.
- 헤드라인 Noto Serif KR 300, 40~48px, 자간 -0.02em. 영문 Cormorant 300 이탤릭을 위에 작게(*Same leaves, different cup.*).
- s04 숫자 골드 Cormorant 140px. 구분선 1px `--line` 또는 골드 0.5px. 둥근 모서리 8px 이하.
- 리워드 카드 `--panel`, 가격 골드, % 골드 얇은 원 테두리. 레이더·막대 골드/허브 라인, 채움 15%.
- 금지: 아이보리 섹션, 브라운 밴드, 미장 텍스처.

## 5. 스타일 E · `e-editorial.html` — "화이트 에디토리얼 (Swiss Grid Magazine)"
순백 종이 위 잡지 레이아웃. 타이포·그리드가 주인공, 사진은 큰 직각 블록. 레퍼런스: 홈콕(단일 시스템 컬러), 미꽃체(정보 설계), Kinfolk·Cereal 매거진.
```css
:root{--bg:#FFFFFF;--bg-2:#F3F3F1;--ink:#111111;--ink-2:#555555;--rule:#111111;--rule-soft:#DDDDDD;--accent:#1F4D3A;--accent-soft:#E6EEE9;
--f-sans:"Noto Sans KR",sans-serif;--f-eng:"Cormorant Infant",serif;--f-type:"Courier Prime",monospace;}
```
- 바탕 흰색. 섹션은 **검정 2px 괘선 + 좌상단 섹션 번호 `01`~`16` Noto Sans 700 72px**로 시작.
- 좌 3/우 9 또는 6/6 그리드. 모든 텍스트 **왼쪽 정렬**(가운데 정렬 금지).
- 헤드라인 Noto Sans KR 700 34~44px 자간 -0.03em, 본문 400 16px/1.8. Cormorant 이탤릭은 섹션당 1곳.
- 사진·영상 모서리 직각, 테두리·필터 없음. 캡션 타자기체 11px 왼쪽.
- 표는 진짜 `<table>`: 원료 표(12행: 번호/영문/학명/한글/설명/향·바디·여운 바), 레시피 표, 리워드 표(리워드/구성/가격/혜택). 막대는 `--accent` 단색 얇은 바.
- 강조는 `--accent-soft` 면 또는 검정 굵은 줄. 다크 밴드 없음.
- 금지: 세리프 한글 헤드라인, 종이 질감, 가운데 정렬, 그라데이션.

## 6. 스타일 F · `f-garden.html` — "보태니컬 가든 저널 (Watercolor & Color Fields)"
컬러풀하고 따뜻한 일러스트 중심. 원료 하나마다 색 하나. 레퍼런스: 티앤영(향마다 컬러 블록), 니들북(파스텔), 자스민영(파스텔 레이더), 보태니컬 도감.
```css
:root{--cream:#FBF6EC;--ink:#3A3129;--ink-2:#6B5F54;
--blush:#F2D9D5;--blush-d:#C9867E; --sage:#DCE6D3;--sage-d:#6F8B63; --citrus:#F7E6B8;--citrus-d:#C9A23A; --oat:#EFE3CC;--oat-d:#A98654; --cocoa:#E3D2C6;--cocoa-d:#7E5A44;
--f-head:"Noto Serif KR",serif;--f-kr:"Noto Sans KR",sans-serif;--f-eng:"Cormorant Infant",serif;--f-type:"Courier Prime",monospace;}
```
- **색면 블록이 섹션을 나눈다**: 섹션마다 배경을 blush/sage/citrus/oat/cocoa 중 하나로 통째로 칠한다(크림은 쉼 구간에만). 16섹션이 색 리듬으로 읽히게.
- 히어로는 `garden_hero.png`(보태니컬 서클) 위 또는 옆에 헤드라인. 영상은 **아치형(상단 반원) 또는 둥근 모서리 24px 마스크**로 색면 위에 띄움. 풀블리드는 s16만.
- 원료 카드: 큰 일러스트(카드 높이 60%) + 색면 배경 + 둥근 모서리 20px. 장미·히비스커스 blush / 레몬밤·페퍼민트·캐모마일 sage / 유자 citrus / 보리·현미·찰수수·둥굴레 oat / 민들레 뿌리·단팥 cocoa.
- 헤드라인 Noto Serif KR 600 32~40px, 색은 해당 색면의 `*-d`. 번호·단계는 원형 배지(`*-d` 배경 + 크림 글자). 레이더 파스텔 채움 60%.
- 리워드 카드: 크림 카드 + 상단 색 띠(R1 blush, R2 sage, R3 oat, R4 cocoa), % 원형 배지.
- 금지: 다크 밴드, 검정 괘선, 헤어라인만 있는 카드.

---

## 7. 세 파일을 1/3 크기로 나란히 놓았을 때 **배경색만으로 구분**되어야 한다: D 검정 / E 흰색 / F 파스텔 색면.
