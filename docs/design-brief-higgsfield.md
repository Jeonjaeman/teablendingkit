# 취향의 권리 · tea Apotheca — 패키지 & 홈페이지 디자인 기획서 (힉스필드 실전용)

- 작성일: 2026-07-01
- 작성: 탱탱소프트 (전재만)
- 클라이언트: tea Apotheca · 이소연 명인 (blend since 1975 / 청주 ↔ Chula Vista)
- 신규 라인: **취향의 권리 (The Right to Taste)** — 티 블렌딩 키트
- 목적: `data/` 전 자료를 시간순으로 분석해 담당자 니즈를 확정하고, **패키지 / 홈페이지** 두 축의
  컨셉을 정의한 뒤, **힉스필드(Higgsfield)로 바로 생성 가능한 프롬프트 기획서**를 제공한다.
- 관련 문서: [main-design-spec.md](./main-design-spec.md) (홈페이지 데모 스펙) · 데모 `design/index.html`

---

## 0. 자료 시간순 분석 & 담당자 니즈 파악

### 0-1. 타임라인 (data/ 자료 근거)

| 일시 | 자료 | 핵심 내용 |
|---|---|---|
| 06/20 | KakaoTalk 이미지 20+장 (무드보드/제품/명함) | Pinterest 무드보드(흙·돌·나무결·린넨), 이탈리아 장인 감성, 제품·명함 실물 전달 |
| 06/21 02:00 | `블렌딩키트 브랜드 사이트 디자인 레퍼런스 방향.txt` | **홈페이지** 방향서: 자연주의·명상·여백, MUJI/Apple 레이아웃, 어스톤 팔레트, 세리프 조합 |
| 06/21 02:00 | `의뢰자 성향 분석 및 추천 레퍼런스 사이트.html` | 성향 분석 + 국내외 레퍼런스 30선 (Song Tea·Aesop·Frama·Merchant&Mills 등) |
| 06/23 | 레퍼런스 방향 수정 | 톤 재확인 |
| 06/24 | `main-design-spec.md` + `design/index.html` | **홈페이지 몰입형 데모** 1차 제작 (Immersive×Meditative) |
| 06/28 14:05 | `음성 260628_140505` (첫 대면 미팅) | 제품 실물 시연: **병풍(아코디언) 구조**, 6종 허브, 가이드북/블렌딩노트, 고재 실사 프린팅, "취향의 권리는 tea Apotheca와 별도 브랜드", AI 활용/유튜브·인스타 채널 논의 |
| 06/28 15:26 | `음성 260628_152609` | 브랜드 서사("영혼을 갈아 넣는다"), **"상품이 아닌 경험을 판다"**, 가격 벽 낮추기(3~4만원대), About을 '회사소개'로 부르면 감성이 무너진다 |
| 06/28 | 프로토타입 사진 3장 | 크래프트 골판지 + **칼선 삽입 구조** 실물, 허브 파우치(레몬밤 라벨) |
| 06/29 21:29 | `통화 260629_212916` | 형태 확정(용수철처럼 딸려나오는 병풍), 인쇄 한계(1900mm), **예산: 패키지 300만/출판 400만**, 100개 소량, 역할분담(패키지·출판·마케팅·디자인) |
| 07/01 17:28 | `통화 260701_172803` | 작업 범위 정의: 겉상자 + 병풍 칼선 + 허브카드 + 한글표기 레이블. **"실사 프린팅이라 단순한 작업"**, 브랜딩 전면 재창작 아님 |
| 07/01 17:40 | `통화 260701_174025` | 지역(전주) 디자이너는 미팅 필요·부담 → **크몽 100만 이내 대안**, 톤 리드는 탱탱소프트가 담당 |
| 06/28~07/01 | `KakaoTalk_...129249.png`, `...849837.png` | **힉스필드 1차 시안**: 고재 나무결 패키지 목업 시트 / 취향의 권리 티 블렌딩 노트 표지 |

### 0-2. 담당자(이소연 대표) 니즈 — 확정 정리

**브랜드/철학 니즈**
1. **"경험을 판다"** — 판매가 아닌 취향 발견의 경험. "무언가 사야겠다"보다 "잠시 쉬어가고 싶다".
2. **취향의 권리 서사가 모든 접점에 흐를 것** — `About`을 일반적 '회사소개'로 규정하면 감성이 무너진다. 메뉴 하나라도 "취향의 권리" 맥락으로 연결.
3. **"옛것에 현재를 블렌딩" / 고재(古材)** — 낡음이 아닌 시간의 결. 취향도 시간·경험으로 완성된다.
4. **조용한 럭셔리** — 갤러리·아포테카리·무인양품·일본 북디자인. 과한 연출·상업 광고·화려한 카페 감성 기피.

**실무/제작 니즈 (매우 중요 — 견적·일정 직결)**
5. **실사 프린팅 기반의 단순화** — 일러스트 창작을 최소화하고 고재 텍스처 실사 + 로고/문구 배치 중심. 예산 절감 + 시리즈 확장 시 재사용.
6. **예산 타이트** — 패키지 개발 300만(제작 100개 포함), 출판물 400만 내외, 디자인은 크몽 기준 100만 이내를 압박선으로 인지. → **힉스필드로 촬영·목업·텍스처 비용을 대체**하는 것이 핵심 전략.
7. **톤/무드 리드가 핵심 산출물** — 대표는 "컨셉·무드만 명확히 잡아주면 패키지·출판·홈페이지가 같은 결로 간다"고 반복. 즉 **우리 역할 = 일관된 비주얼 톤의 소스(에셋) 생산자**.
8. **시리즈 확장 전제** — 결(結)/숨(숨) 등 컨셉별 라인. 병풍·겉박스는 공용, 허브 파우치·카드·레이블만 교체. → 에셋도 **모듈형**으로 생성.
9. **채널 순서** — ① 와디즈 펀딩 런칭용 비주얼 → ② 홈페이지 리뉴얼(카페24 커머스 연결) → ③ 인스타/유튜브 콘텐츠.

**제품 사실 관계 (프롬프트에 반영할 근거)**
- 겉포장: **크래프트 골판지 상자**, 겉면 **고재 나무결 실사 프린팅**.
- 내부: **병풍(아코디언) 종이** — 상자에서 용수철처럼 딸려 나오며 칸마다 칼선으로 허브 파우치·엽서를 끼움. 페이지 하단 로고 공용, 뒷면에 한글표기 레이블 칸.
- 구성품: 허브 파우치 6종, **허브 카드**(향·특징), **엽서**(블렌딩 영감 문구), **블렌딩 노트**(기록), **브랜드 북**(철학 에세이), 티백·도구.
- 제품 라인: **결(結)** = 레몬밤·히비스커스·레몬머틀·카모마일·라벤더·장미 / **숨** = 모과·도라지·생강·강황·유자·진피.

---

## 1. 컨셉 — 패키지(확정 기반) · 홈페이지(미확정 제안)

> **상태 구분 (중요)**
> - **A. 패키지 = 확정 기반**: 실물 프로토타입·예산 배정(300만)·벤더 미팅·요청서가 존재 → 이 기획서의 실행 대상.
> - **B. 홈페이지 = 아직 미확정 제안**: 1차 데모(`design/index.html`) 수준이며 방향·IA 미승인 상태. 아래 B와 §4는 **제안(초안)**일 뿐, 패키지 기획의 전제가 아니다.
> - **의존 방향은 단방향**: 공통 스타일 토큰은 홈페이지가 아니라 **확정된 브랜드 톤(고재·어스톤 — 요청서/방향서)**에서 도출된다. 패키지는 홈페이지 확정 여부와 무관하게 독립적으로 진행 가능하다.

### A. 패키지 컨셉 — **「고재, 시간의 결」 (Aged Wood, The Grain of Time)** · ✅ 확정 기반

> 고재의 아름다움은 낡음이 아니라 그 안에 담긴 시간과 이야기에서 비롯된다.
> 사람의 취향 또한 그렇게 완성된다.

- **핵심 오브제**: 오래된 목재의 나뭇결·옹이·못자국·풍화 질감 (실사 프린팅).
- **감정**: 갤러리 전시 카탈로그를 여는 듯한 조용한 격, 손끝의 촉감(크래프트지·먹색 인쇄).
- **차별점**: 화려한 그래픽이 아니라 **소재(고재)와 여백, 각인(刻印)된 로고**로 완성.
- **컬러**: 우드 브라운 / 오트밀 베이지 / 아이보리 / 차콜 · 포인트 **먹색 · 골드**.
- **인쇄 기법 인상**: 나무에 인두로 지진 듯한 **번(burn)/각인 로고**, 종이는 크래프트·재생지.

### B. 홈페이지 컨셉 (초안) — **「고재, 취향을 담는 그릇」 — 취향에 관한 인문학적 에세이** · ⚠️ 미확정 제안

> 아래는 **아직 승인되지 않은 방향 제안**이다. 패키지 진행의 전제가 아니며, 홈페이지 방향이 확정될 때 §4와 함께 재검토·수정 대상이다.

**근본 은유 (클라이언트 확정 정서)**: 고재(古材)는 **시간·기억·취향을 담는 그릇**이다. 나뭇결이 시간을 새기듯, 사람의 취향도 시간과 경험으로 완성된다. → 홈페이지는 상품몰이 아니라 **이 고재 노트(`취향의 권리 티 블렌딩 노트` 표지)를 펼쳐 읽는 듯한 한 편의 에세이**로 설계한다.

- **핵심 원칙 — 세계관 우선, 차는 나중·최소**: 취향의 권리라는 **인문학적 풀이와 공감대 형성이 1순위**. 차/제품은 세계관에 공감한 뒤 후반부에 조용히 등장한다(상단 60~70%는 차 없이 빛·질감·시간·사람의 은유로).
- **화법**: **2인칭("당신")** 에세이. 판매 문구 금지. "무언가 사야겠다"가 아니라 "내 취향이 궁금해졌다 / 위로받았다".
- **담아야 할 뉘앙스(핵심 카피 축)**:
  - "당신의 취향에는, 권리가 있습니다."
  - "정형화된 블렌딩은 정답이 아닙니다."
  - "전문가에게는 원칙이 있지만, 당신에게는 취향의 권리가 있습니다."
  - "취향은 정해지는 것이 아니라 완성되어 갑니다."
- **길이는 제약이 아니다**: 사유의 호흡이 우선 → 여백·인터스티셜 화면을 자유롭게 늘린다.
- **연출**: 풀스크린 스크롤에서 한 화면 = 한 문장/한 호흡. 느린 페이드·시차만(과한 모션 금지).
- **커머스(제안)**: 브랜드 경험은 커스텀 몰입형 페이지, 결제·장바구니는 카페24로 위임(CTA만 연결).

> **톤 공유는 단방향**: 공통 스타일 토큰(자연광·어스톤·필름 그레인·고재 질감)은 **확정된 브랜드 톤에서 도출**된 것이지 홈페이지에서 온 것이 아니다. 따라서 패키지는 홈페이지 확정과 무관하게 진행되고, 홈페이지는 (확정 시) 패키지 에셋·톤을 **재사용**하는 쪽이다. (대표의 8·9번 니즈 — 결과적으로 같은 세계관으로 보이게)

---

## 2. 힉스필드 공통 운용 가이드 (두 축 공통)

### 2-1. 모델 선택
- **정물/제품 목업·질감·인물 컷(사실적)**: 최고급 사실계 image 모델 (예: GPT Image 계열 / Seedream 계열). 확신 안 서면 `models_explore(action:'recommend')`로 목적·레퍼런스 넣고 추천받기.
- **영상(Hero·Journal 루프)**: image_to_video 계열(Seedance 등)로 정지컷을 6~8초 느린 루프로.
- **3D(선택)**: 회전 오브제가 필요할 때만 `generate_3d`(image_to_3d)로 GLB 생성 → `<model-viewer>`. ※ 세계관 우선 방향에서는 제품(찻잔) 회전컷을 전면에 쓰지 않음 — 남용 시 상품 느낌이 강해져 지양.
- **후처리 전용 툴 우선 사용**: 재생성보다 `upscale_image`(2K/4K), `outpaint_image`(웹 배경 확장), `remove_background`(제품 컷아웃), `reframe`(영상 비율).

### 2-2. 공통 스타일 토큰 (모든 프롬프트에 접미로 append)
```
STYLE TOKEN (append to every prompt):
soft natural window light, long gentle shadows, muted earth tones
(ivory #F4F1E9, oatmeal beige #E2D8C6, sage #7E8B6E, olive #5E6447,
clay #B07D5B, charcoal #2C2B24, ink-black, matte gold #E9C9A8),
fine 35mm film grain, low saturation, calm and meditative mood,
generous negative space, MUJI x apothecary x gallery-catalog aesthetic,
photographic realism, no gloss, no vibrant colors
```
```
NEGATIVE (공통):
oversaturated, neon, HDR, glossy plastic, busy background, cluttered,
harsh flash, cartoon, 3d render look, watermark, text artifacts,
lens flare, commercial ad vibe, stock-photo cliché
```

### 2-3. 일관성 규칙
- **시드 고정**: 채택 컷의 seed를 기록해 시리즈(결/숨)·리사이즈 변형 때 재사용.
- **로고 텍스트는 후보정**: AI 생성 이미지에 한글/영문 로고를 직접 새기면 깨짐 → **로고·한글표기·문구는 벡터로 실사 위에 합성**. 프롬프트에는 "빈 여백(clean empty space for logo)"을 요청.
- **비율**: 패키지 목업 4:3 / 5:4, 웹 풀스크린(S0/S5) 16:9·21:9, 모바일 9:16, 카드/엽서 3:4.
- **해상도**: 최종 채택본은 반드시 `upscale_image`로 인쇄용(300dpi 환산) 확보.

---

## 3. 패키지 디자인 기획서 (힉스필드용)

### 3-1. 구성품 & 산출 에셋 목록

| # | 구성품 | 디자인 포인트 | 힉스필드 산출물 | 실사프린팅 반영 |
|---|---|---|---|---|
| P1 | 겉박스 (닫힌 상태) | 고재 나무결 실사 + 각인 로고 | 목업 사진 1컷 | ✅ 겉면 전체 |
| P2 | 겉박스 (열린 상태 / 전체 구성) | 병풍·구성품 배치 오버뷰 | 목업 사진 1컷 | — |
| P3 | 병풍(아코디언) 펼침 | 용수철처럼 늘어나는 칸·칼선 | 목업 사진 1~2컷 | ✅ 칸 하단 로고 |
| P4 | 허브 파우치 (6종) | 크래프트 파우치 + 미니 레이블 | 정물 세트컷 1 + 개별 | 레이블만 교체 |
| P5 | 허브 카드 (6종) | 향·특징, 보태니컬 원물 사진 | 카드 앞/뒤 목업 | ✅ 카드 표면 |
| P6 | 엽서 | 블렌딩 영감 문구 여백 | 엽서 목업 | ✅ |
| P7 | 블렌딩 노트 표지 | 고재 각인 "취향의 권리" (기제작본 톤) | 표지 목업 | ✅ 표지 |
| P8 | 브랜드 북 표지 | 에세이집 톤, 조용한 격 | 표지 목업 | ✅ 표지 |
| P9 | 고재 텍스처 원판 (소재) | 인쇄 입힐 원본 나뭇결 텍스처 | seamless 텍스처 다수 | ✅ 소스 |

> 기제작 시안(`KakaoTalk_...129249.png` / `...849837.png`)이 이미 P1·P2·P7 톤을 잘 잡았음 → **그 톤을 기준 시드로 고정**하고 나머지 컷을 같은 결로 확장.

### 3-2. 컷별 힉스필드 프롬프트

**P1 — 겉박스(닫힌 상태)**
```
A closed premium tea gift box photographed top-down on a dark aged
wooden table. The box surface is a photo-real print of weathered
reclaimed wood grain (고재), with visible knots, nail holes and time-worn
texture. A small minimal engraved/burned logo mark and thin serif
wordmark centered, lots of empty space around it. Kraft corrugated
edges. Editorial still-life, gallery-catalog calm.
+ [STYLE TOKEN] | ratio 4:3
```

**P2 — 겉박스(열린 상태, 전체 구성 오버뷰)**
```
An open tea blending kit box seen from a slight top angle. Inside, from
left to right: a small kraft herb pouch with a tiny white label, a
"guide book" and a "blending note" with aged-wood-grain covers standing
in fitted compartments. Natural kraft cardboard padding. A sprig of
eucalyptus resting beside the box on a walnut table. Warm window light,
long soft shadow.
+ [STYLE TOKEN] | ratio 5:4
```

**P3 — 병풍(아코디언) 펼침 — 대표가 가장 헷갈려한 핵심 구조**
```
A long accordion-folded (byeongpung / concertina) kraft paper strip
being pulled out of a tea box like a spring, unfolding into several
equal panels. Each panel has a die-cut slot holding a translucent herb
pouch and a small postcard. A minimal engraved logo repeats at the
bottom of every panel. Photographed at an angle showing the folds and
depth, soft natural light, clean neutral background.
+ [STYLE TOKEN] | ratio 16:9
```
> ⚠️ 이 컷은 실물 프로토타입(`KakaoTalk_20260628_122126232/127681.jpg`)을 참조 이미지로 첨부해 image-to-image로 생성하면 구조 정확도가 크게 오른다.

**P4 — 허브 파우치 6종 세트컷**
```
Six small translucent/kraft herb pouches arranged in a calm grid on an
oatmeal linen cloth, each filled with dried botanicals (lemon balm,
hibiscus, lemon myrtle, chamomile, lavender, rose). Each pouch has a
tiny minimal white label with clean empty space (no readable text).
Loose dried petals and leaves scattered sparingly. Top-down, soft light.
+ [STYLE TOKEN] | ratio 4:3
```

**P5 — 허브 카드 (원물 보태니컬)**
```
A minimal herb information card lying on aged wood. Left side: a
photo-real close-up of a single dried botanical (e.g. lavender sprig)
on a cream paper; right side: generous empty space reserved for text.
Letterpress / kraft paper feel, subtle deckled edge. Gallery herbarium
mood.
+ [STYLE TOKEN] | ratio 3:4
```

**P6 — 엽서 (블렌딩 영감 문구용)**
```
A single cream postcard with heavy deckled-edge cotton paper texture,
resting on a wood surface with a dried leaf shadow across it. Vast empty
center for a short poetic line (leave blank). Ink-black thin serif
accent only. Quiet, contemplative.
+ [STYLE TOKEN] | ratio 3:4
```

**P7 / P8 — 노트 & 브랜드 북 표지** (기제작 `...849837.png` 톤 계승)
```
A book cover printed with photo-real aged reclaimed-wood grain, worn and
weathered with tiny insect holes and cracks, exposed thread binding on
the spine. A minimal engraved square emblem centered, thin serif line
beneath it, large empty space. Placed on rough old wooden planks, top
lit, deep contemplative shadow.
+ [STYLE TOKEN] | ratio 3:4
```
> 표지 위 "취향의 권리 / TEA BLENDING NOTE / 나만의 취향을 발견하는 시간" 등 **글자는 벡터 합성** (기제작본과 동일 방식).

**P9 — 고재 seamless 텍스처 (실사 프린팅 소스)**
```
A seamless flat-lay texture of weathered reclaimed barn wood, greyish
warm brown, fine grain, knots and nail holes, evenly lit with no strong
shadow, tileable, high resolution, suitable as a print background.
+ low saturation, matte, no objects | ratio 1:1
```
> 톤 편차용으로 **밝은/중간/어두운 3종**을 뽑아 두면 시리즈별로 골라 쓸 수 있다(대표가 "밝게/어둡게 조절" 언급). 채택본은 `upscale_image` 4K.

### 3-3. 시리즈 확장(결/숨) 운용
- 겉박스·병풍·노트/북 = **공용 에셋 재사용**.
- 교체 항목만 재생성: 허브 파우치 라벨(원물 변경), 허브 카드 6종, 엽서 문구, 라인 컬러 포인트(결=그린 계열, 숨=클레이/골드 계열 강조).

---

## 4. 홈페이지 디자인 기획서 (힉스필드용) · ⚠️ 미확정 제안 (방향 승인 전 초안)

> 본 §4는 홈페이지 방향이 **확정되기 전 초안**이다. 아래 IA·프롬프트는 승인 후 변경될 수 있으며, **패키지(§3) 진행에는 영향을 주지 않는다.** 홈페이지가 확정되면 패키지에서 만든 에셋(P1~P3 등)과 공통 톤을 재사용한다.

### 4-0. 디자인 원칙 — 인문학적 접근 (세계관 우선 · 차는 나중)

이 사이트는 **상품 소개가 아니라 '취향'에 관한 한 편의 에세이**다. 방문자는 스크롤을 따라 사유를 경험하고, **공감대가 형성된 뒤에야** 차/제품이 조용히 등장한다.

1. **차 노출 지연·최소** — 상단 흐름(S0~S4)은 차 없이 **빛·나뭇결·시간·사람의 은유**로만. 차/제품은 S5부터.
2. **2인칭 화법** — "당신"에게 말을 건다. 판매 문구·CTA 남발 금지.
3. **한 화면 = 한 문장/한 호흡** — 타이포 중심, 압도적 여백. 길이는 제약이 아니다.
4. **"정답 없음"을 레이아웃으로** — 비대칭·불완결·여백으로 정형화된 정답의 부재를 시각화.
5. **사이트 = 고재 노트를 읽는 경험** — 각인체(engraved) 세리프, 고재 질감, 느린 페이드. 표지 이미지(`...849837.png`)의 정서를 UI 전체로 확장.
6. **엠블럼(□ + 점) 재사용** — 빈 사각(모든 가능한 취향의 여백) 안의 한 점(= 당신). "정답은 격자가 아니라, 당신이라는 한 점"을 상징하며 스크롤 진행 표시·섹션 마커로 사용.

### 4-1. 정보구조 — 세계관 에세이 흐름 (제품 후치)

> 번호는 스크롤 순서. **S0~S4 = 세계관/공감(차 없음)**, **S5~S6 = 차·제품의 조용한 등장**, **S7~S8 = 확장·연결**.

- **S0. 표지 / Prologue** — 고재 질감 풀스크린 + 각인 엠블럼. 브랜드명조차 크게 내세우지 않음.
  카피: *"당신의 취향에는, 권리가 있습니다."* (느린 fade-in) · 하단 scroll 큐. **차 없음.**
- **S1. 질문** — *"언젠가부터, 우리는 '정답'을 배웠습니다."* 정형화된 정답·전문가 권위에 대한 잔잔한 의심. 빛/그림자/손의 은유. **차 없음.**
- **S2. 고재의 은유 (핵심)** — *"고재의 아름다움은 낡음이 아니라, 그 안에 담긴 시간과 이야기에서 비롯됩니다. 사람의 취향도, 그렇게 완성됩니다."* 나뭇결·옹이 매크로로 '시간을 담는 그릇'을 시각화. **차 없음.**
- **S3. 선언 (감정 절정 · 공감대)** — *"전문가에게는 원칙이 있지만, 당신에게는 취향의 권리가 있습니다."* / *"정형화된 블렌딩은, 정답이 아닙니다."* 엠블럼의 점이 화면 중앙에서 커짐(= 당신).
- **S4. (인터랙션) "정답 없는 블렌딩"** — 방문자가 지금의 기분·계절·순간을 나타내는 단어 몇 개를 고르면, **채점 없이** 자기만의 한 문장/결이 생성된다. "정답이 없다"를 몸으로 체감시키는 공감 장치. (선택 구현)
- **S5. 그리고, 차 (첫 등장)** — *"우리는 이 믿음을 담는 하나의 방식으로, 차를 블렌딩합니다."* 여기서 처음으로 차가 조용히 등장. `blend since 1975`(청주 ↔ Chula Vista)는 판매가 아닌 **철학의 오랜 실천**으로 은근히 삽입.
- **S6. 취향을 담는 그릇 (키트 = 도구, 상품 아님)** — 고재 노트(표지 이미지) 그대로 등장. *"당신의 취향의 시간을 담는 노트."* 키트를 상품이 아니라 **취향을 발견·기록하는 도구**로 제시. (패키지 P1·P3·P7 재사용)
- **S7. 함께 걷기** — 클래스(출강/강사/워크숍)·Journal을 '사유의 연장'으로. "가르침"이 아니라 "함께 발견".
- **S8. Footer** — *"Stay a while."* 조용한 커머스 연결(카페24 CTA는 여기서만, 절제). teablendingkit.kr / 취향의권리.com

### 4-2. 섹션별 힉스필드 에셋 & 프롬프트 (은유·인간 중심, 차는 S5부터)

**S0 — 표지/Prologue (고재 풀스크린)** — 표지 이미지 톤 계승, 각인 자리 여백
```
Full-frame macro of weathered reclaimed wood (고재), soft warm greyish
brown, fine grain with knots, tiny worm holes and time cracks, lit by
gentle raking window light casting long quiet shadow. A large calm empty
area in the center reserved for an engraved emblem and a single line of
text. Contemplative, gallery-like, almost silent.
+ [STYLE TOKEN] | ratio 21:9  (모바일 9:16 별도)
→ image_to_video 옵션: light very slowly shifting across the grain, 10s loop, no camera move
```

**S1 — 질문 (손·빛의 은유, 차 없음)**
```
A single human hand resting open on an aged wooden surface, soft daylight
from a window, long shadow, dust motes floating. Quiet, introspective,
no product, lots of empty space. A moment of doubt and reflection.
+ [STYLE TOKEN] | ratio 16:9
```

**S2 — 고재의 은유 (나뭇결 = 시간을 담는 그릇 · 핵심)**
```
Extreme close-up of an old wood grain surface where growth rings and
cracks look like layers of accumulated time and memory. Warm earthy
tones, side light revealing texture depth. Metaphor of time held inside
material. No objects, no tea.
+ [STYLE TOKEN] | ratio 16:9
```

**S3 — 선언 (엠블럼 모멘트)** — 대부분 타이포로 처리, 배경만 생성
```
A near-empty ivory-to-sand textured paper background with a faint aged
paper grain, extremely minimal, soft vignette, designed as a calm canvas
for a single centered engraved square emblem with one small dot inside.
Meditative negative space.
+ [STYLE TOKEN] | ratio 16:9
→ 엠블럼(□+점)·문구는 벡터 합성
```

**S4 — 인터랙션 배경 (정답 없는 블렌딩)**
```
Softly lit flat-lay of loose dried herbs and petals scattered freely
(not arranged in a grid) on cream handmade paper, asymmetric, incomplete,
plenty of empty space — visualizing "there is no single correct blend".
Gentle shadow, muted tones.
+ [STYLE TOKEN] | ratio 16:9
```

**S5 — 그리고, 차 (첫 등장, 조용히)**
```
A quiet still life: a hand gently cupping a handmade ceramic bowl of
freshly blended tea on an aged wood table by a window, soft steam, warm
side light, sheer linen nearby. Understated, devotional, not a product
shot — tea as the practice of a belief. Empty space for text.
+ [STYLE TOKEN] | ratio 16:9
→ image_to_video: very slow steam drift, 8s loop, no camera shake
```

**S6 — 취향을 담는 그릇 (고재 노트 = 도구)** → **기제작 노트 시안(`...849837.png`) + 패키지 P1/P3/P7 재사용.** 필요 시 아래로 보강:
```
The aged-wood-grain "tea blending note" lying open on rough old planks,
a pressed leaf and a pencil beside it, a few handwritten-looking marks
(no readable text) on the cream inner page. Framed as a personal journal
of taste, not merchandise. Warm top light.
+ [STYLE TOKEN] | ratio 3:4
```

**S7 — 함께 걷기 (클래스 · Journal, 사람 중심·비상업)**
```
(class) Hands of a few people around a long wooden table with small bowls
of dried herbs and open notebooks, soft daylight from above, faces not
emphasized, warm documentary feel — discovering together, not a lecture.
(journal) A person seen from behind sitting quietly by a window, a bowl
of tea in hand, leaf shadows on the wall.
+ [STYLE TOKEN] | class 16:9 / journal 3:4
```

**S8 — Footer 배경 텍스처**
```
A soft botanical footer band: pressed dried flowers and herb sprigs laid
flat on cream handmade paper, faint, low-contrast, wide and short, lots
of breathing room.
+ [STYLE TOKEN] | ratio 21:9 (short)
```

### 4-3. 타이포 & UI 시그니처 (인문학적 톤 유지 장치)
- **각인체 인상의 세리프**: 한글 Noto Serif KR(300/400)·MaruBuri, 영문 Cormorant Garamond(이탤릭 강조). 본문은 큰 자간·행간으로 '읽는 호흡'.
- **엠블럼(□+점)**: 로고·스크롤 진행·섹션 구분에 반복. 점의 위치가 스크롤에 따라 사각 안을 미세 이동 → "당신의 자리"를 은유.
- **모션**: IntersectionObserver 기반 문장 페이드+상승만. `prefers-reduced-motion` 대응.

### 4-4. 모바일/반응형 & 런칭 에셋
- S0·S5 주요 컷은 **9:16 세로 버전** 별도 생성(`reframe`/재생성 권장, 단순 크롭 지양).
- **와디즈 상세페이지**(런칭 우선순위 1): 동일 세계관 톤의 **세로 롱폼 에세이 컷**을 확보 — 홈페이지 S0~S6 흐름을 세로로 압축 재사용.

---

## 5. 산출·전달 워크플로 (권장)

1. **텍스처 원판(P9) 먼저** 3종 생성 → 톤 기준선 확정 → seed 고정.
2. 패키지 목업 P1→P2→P3 순으로 생성(구조 정확도 위해 실물 프로토타입 image-to-image 활용).
3. (홈페이지 확정 시) **S0 표지 → S2 고재 은유** 확정 → 세계관 톤 기준선 잡고 나머지 섹션 확장. 차 등장 컷(S5~)은 후반에 생성.
4. 채택본 전량 `upscale_image`(인쇄 4K / 웹 2K) → `remove_background` 필요분 컷아웃.
5. 로고·한글표기·문구는 **벡터 합성**(AI 텍스트 사용 금지).
6. 대표 확인 루프: 무드/톤 먼저 승인 → 세부 조정 1~2회(대표가 선호하는 빠른 의사결정 방식).

## 6. 리스크 / 메모
- **AI 텍스트 각인 깨짐** → 문구·로고는 반드시 후합성.
- **인쇄 물리 한계**(병풍 1900mm 초과 시 분할 인쇄) → 목업은 이상적 형태로, 실제 칼선·분할은 패키지 업체 샘플과 대조.
- **예산 방어** → 힉스필드가 촬영/일러스트/목업 비용을 대체함을 견적서에 명시(대표의 예산 압박 니즈 대응).
- **시리즈 일관성** → seed·스타일 토큰·텍스처 원판을 자산으로 관리(결/숨 및 향후 라인 재사용).
