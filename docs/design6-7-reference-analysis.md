# design6 · design7 — 레퍼런스 분석 및 이식 기록

- 작성일: 2026-09-16
- 작성: 탱탱소프트 (전재만)
- 데모: [design6/index.html](../design6/index.html) · [design7/index.html](../design7/index.html) · 공유 페이지 [estimate/design-mockups.html](../estimate/design-mockups.html)

---

## 0. 폴더 이력 요약 (2026-06 ~ 09)

| 시기 | 산출물 | 브랜드 상태 |
|---|---|---|
| 06-24 | `design/` Immersive×Meditative 1차 데모 | tea Apothēca · 세이지/클레이 어스톤 |
| 06-25 | `design2/`, `design3/` (매거진형 · 에디토리얼) + `estimate/design-mockups.html` 공유 | 대표 "1안·2안 좋다" |
| 07-01 | `design4/` 취향의 권리 세계관 데모 + `docs/design-brief-higgsfield.md` | 고재(古材) 은유 · 結/숨 라인 · □+점 엠블럼 |
| 07-04 | `design5/` 시네마틱 프롤로그 + Japandi 에디토리얼 (최종 커밋본) | 고재 축소, "취향이 답" |
| 07-24 ~ 27 | `data/260727/` 수정 원고(docx) · 패키지 방향 3 "탈네모틀" · 핀터레스트 무드 | **미장 아이보리 · 한글×라틴 실험 타이포** |
| 08-12 ~ 19 | 별 엠블럼 로고 시안 3색 · Taste/Depth 12종 보태니컬 카드(수채·동판화) · 박스 칼선 · 병풍 목업 · 책 표지 3면 · 최종 로고 | **로고 확정 · Taste(레몬밤·캐모마일·히비스커스·페퍼민트·유자·장미) / Depth(현미·민들레뿌리·결명자·보리·팥·둥굴레)** |
| 09 | 견적서(탱탱소프트 400만 부가세 별도 · 프린트라인) | 홈페이지 착수 대기 |

> design6/7은 위 8월 확정 요소(별 엠블럼 · Taste/Depth · 12 보태니컬 · 미장 아이보리 · 타자기체 영문 · "Life is an endless blending")를 기준으로 제작. 고재/차콜 톤(design5)은 더 이상 브랜드 현재형이 아님.

### 오고간 이미지 소스 → 에셋 매핑
| 원본 (`data/`) | 용도 | 결과 |
|---|---|---|
| `KakaoTalk_20260814_171714043(_01).png` 동판화 카드 시트 2장 | 12장 크롭 | `design6/assets/cards/*.jpg` (412×670) |
| `KakaoTalk_20260814_195921363.png` 수채 카드 시트 | Higgsfield 4K 업스케일 후 12장 크롭 | `design6/assets/color/*.jpg`, `design7/assets/botanicals/*.jpg` (530×962) |
| `KakaoTalk_20260814_193832786(_01).png` 미장 텍스처 | 배경 | `design7/assets/plaster-1/2.jpg`, `design6/assets/plaster-1.jpg` |
| `KakaoTalk_20260814_193900586.png` 패키지 시트 | 박스 전면·파우치·책갈피 크롭 | `design7/assets/box-front.jpg`, `pouch.jpg`, `bookmark.jpg` |
| `KakaoTalk_20260814_192225297.jpg`, `193641997.jpg`, `20260819_195313376(_01).png` | 책 표지·3면·병풍 목업 | `design7/assets/book-*.jpg`, `accordion.jpg` |
| `KakaoTalk_20260819_120233042/364.jpg` | 최종 로고(정방/가로) | `assets/logo-sq.jpg`, `logo-h.jpg` + SVG 재작화 `design6/assets/emblem.svg` |
| Higgsfield 신규 생성 6컷 (gpt_image_2_5) | 원형 히어로 찻그릇 · 노을 테이블 · Taste 플랫레이 · Depth 접시 · 미장 선반 · 허바리움 책상 | `design7/assets/hero-bowl.jpg`, `sunset-table.jpg`, `taste-flatlay.jpg`, `depth-dishes.jpg`, `plaster-shelf.jpg`, `design6/assets/herbarium-desk.jpg` |
| design3/design5 기존 에셋 | 슬라이더 보조컷 | `design7/assets/m-*.jpg`, `cup-linen.jpg`, `pour.jpg`, `class.jpg` 등 |

---

## 1. 100lostspecies.com → design6 「취향의 표본실」

### 1-1. 레퍼런스 정수 (소스 해부 결과)
- **기술**: Vite + Svelte 커스텀 엘리먼트, Three.js 원통형 타일 캐러셀(InstancedBufferGeometry·MSDF 텍스트), GSAP 3.12 + CustomEase. DOM sticky/IntersectionObserver 0건 — wheel/drag를 가로채는 **가상 스크롤**.
- **서체**: Reckless Neue(Thin 100 / Light 300) + Enduro(300/400). 볼드 없음, `letter-spacing:0`, 직각, `box-shadow` 0.
- **색**: 캔버스 `#FFFFFF`, 로더/About `#000`, 다크 UI `#1C1C1C`, 유니버스 3색 Visuals `#92A878` / Names `#5B8CA9` / Extinction `#D6C4A0`, 골드 `#BE9C5D`, 경고 `#970317`.
- **이징**: 위치·스케일 `cubic-bezier(.66,0,.34,1)` / `(.32,.94,.60,1)`, **opacity는 항상 linear**. DOM 0.4~0.8s, 장면 2~3.5s.
- **가상 스크롤**: `target += deltaY*.001; target *= .15; smooth.lerp(target, dt*1.5)`; 열 패럴랙스 `[.8, 1, .6]`.
- **UI**: 검정 pill 탭 3개(활성 시 유니버스 색), 100초 카운트다운 칩 + `i`, 롤링 로고(7s 3프레임), 검정 라벨형 커스텀 커서, 아래서 차오르는 버튼 채움(`:before top:101%`).
- **IA**: Loader(Enter) → 흰 캔버스 아카이브 → 상세(히어로 → 200px 여백 → 20/36px 본문 → 이미지 → 드롭캡 본문 → next 80px 정사각) → Ending(타이머 0) / About(검정, 174px 문장).

### 1-2. 이식 결정
| 레퍼런스 | design6 |
|---|---|
| 100종 멸종 동물 수채 카드 | **12종 보태니컬 카드** (동판화판 = 아카이브, 수채판 = 상세) |
| By Visuals / Names / Extinction Date | 그림으로 / 이름으로 / **맛과 향으로(Taste·Depth)** |
| 100초 카운트다운 = 사라짐 | **3분 우림 타이머** = 차가 우러남 → Ending에서 Taste/Depth 선택 시 시간 리셋 |
| 종 설명 text_1/text_2 | 『취향의 권리』 수정 원고의 **허브 에세이 + 오늘의 허브 노트** |
| WebGL 실린더 | **Three.js r160** — 반지름 10.5 원통 링 3열(패럴랙스 .8/1/.6) 72장 셰이더 타일, 프레임 독립 lerp 가상 스크롤, 속도 기반 타일별 흔들림, 마우스 카메라 패럴랙스, globe/scatter 유니버스 전환(GSAP + CustomEase), 상세 열림 시 다른 타일 축소·현재 타일이 스크롤을 따라 좌상단 대각선 이동/회전(uCurrentTileParallax·uRotationOnScroll 재현), fbm 마블 배경, 3D 다이아몬드 파티클 |
| Reckless/Enduro | Noto Serif KR 200/300 + Cormorant Garamond 300 italic + Noto Sans KR UI + Courier Prime(브랜드 타자기체) |

2차 보강(영상 비교 후): **① 아카이브 세로 이동** — 드래그 dy / 휠(대각선 드리프트) / ↑↓ 키로 열 전체가 위아래로 움직이고(±0.9 rowGap 클램프) 이동 중 링 반지름이 커져 카드가 살짝 멀어짐(레퍼런스 `y+=deltaY`, `radius+=|deltaY|`). **② 진입 물결** — 타일 평면을 이미지보다 1.5배 크게 두고 프래그먼트에서 레퍼런스 `deformationBarrelScale`을 재현: 우상단 모서리에서 시작한 원형 파동이 3.5s(`slow(0.1,0.1)`) 동안 대각선으로 통과하며 외곽선이 휘고 이미지가 당겨지고 지나간 자리가 하얗게 남음. **③ 상세 대각선 스크롤** — 수채 카드·다음 재료 카드를 GL 타일로 만들어 DOM 스페이서 위치를 따라 우하단→좌상단으로 스크롤보다 1.35배 빠르게 흐르게 하고(진입 시 물결 1회), 마블 배경도 스크롤에 맞춰 대각선 드리프트.

추가 페이지: **키트(The Kit)** — Taste/Depth 구성·병풍/박스/파우치 목업·CTA, **클래스(Class)** — 기관 출강/강사 과정/기업 워크숍 + 관찰·우림·블렌딩·기록 4단계.

검수용 URL 훅: `?enter` `?mode=names|taste` `?open=<id>&p=0.6` `?about` `?ending` `?page=kit|class` `&fast` `&jump`(GSAP 타임라인을 감아 최종 상태 즉시 렌더 — 헤드리스 캡처용). 디버그: `window.__d`.

---

## 2. kr.vendredigourmand.com → design7 (라이트 모드)

### 2-1. 레퍼런스 정수 (소스 해부 결과)
- **기술**: 자체 Spring CMS, jQuery + Bootstrap4 + Swiper + **AOS(전체 리빌)** + GSAP ScrollTrigger(가로 스크롤 1곳). 영상 0, 커서 0, 프리로더 0.
- **토큰**: `--body:#000 --light:#FBF0DA(크림 강조) --primary:#BF9A5A(골드) --line hsla(0,0%,100%,.15) --cont-width:1456px --hd-height:100px`; 라디얼 글로우 `#4D3F21 @.6`.
- **서체 슬롯**: 영문 디스플레이 Cormorant Infant 600/700 uppercase, 한글 세리프 학교안심바른바탕(→ Noto Serif KR 500), 본문 Montserrat→Pretendard.
- **스케일**: display3 150px→50px, h2 60→28, h3 36→24; 히어로 워드마크 `12vw` 그라디언트 리빌 3s; 유동 간격 `clamp(min, calc(N/1200*100vw), N)`, 섹션 230px.
- **구조**: sticky 헤더(투명→그라디언트) · 햄버거 → 860px 우측 패널, `01 ABOUT US … 05 GALLERY` 60px 대문자 + 골드 서브 · 히어로 3열(텍스트·원형 이미지·텍스트) · 콜라주 페이드 스와이퍼(main 1:1 + sub1 250 + sub2 355×226 + 중앙 100px 라벨 + 우측 143×183 썸네일) · 풀블리드 배경 교체 스와이퍼(386×573 세로 + display3 좌우 수렴 + VIEW 썸네일) · sticky 200vh 가로 스크롤(3730px, 3파트) · Contact 콜라주 + 워터마크 · 푸터 밑줄 CTA 220px.
- **모션**: AOS fade-up/left/right `translate3d(±100px)` 800ms ease, once:false; hover `scale(1.2)` .2s; 이징 커스텀 없음.

### 2-2. 라이트 반전 규칙 (구조 100% 유지, 색 슬롯 4개만 반전)
| 슬롯 | 다크 원본 | design7 라이트 |
|---|---|---|
| 배경 | `#000` | `#F5F1E9` 아이보리 + 미장 텍스처 multiply .18 |
| 크림 강조(`--light`) | `#FBF0DA` | `#2B2622` 잉크 |
| 골드(`--primary`) | `#BF9A5A` | `#8C6B3E` 브론즈 |
| 헤어라인 | 백색 15% | 잉크 12% (`rgba(43,38,34,.12)`) |
| 글로우 | `#4D3F21 @.6` | `rgba(140,107,62,.16)` |
| 헤더 그라디언트 | 검정→투명 | 아이보리→투명 |
| 썸네일 | grayscale+luminosity | multiply + opacity .6 |
| 위계 opacity .5/.8 | — | 실제 그레이 `#6B655E` |

콘텐츠 매핑: The Art of / Korean Fermentation → "The Right to Taste" / "Life is an endless blending"; Special Sauce → **Taste**(6종 콜라주); Seasonal Dishes → **Depth**(6종 풀블리드); VENDREDI GOURMAND 가로 스크롤 → THE RIGHT TO TASTE + 프롤로그 5행 계단 인용 + Tea Apothēca 서명; Reservation → **키트 만나기**; 메뉴 01 THE STORY / 02 BOTANICALS / 03 THE KIT / 04 JOURNAL / 05 CONTACT.

검수용 URL 훅: `?shot` (vh 고정) `?only=<section id>` `?p=<0..1>` `?menu`.

---

## 4. 2026-09-16 판매 설계서 반영 (design6·7 공통)
출처 `data/20260916.txt` — 취향 테스트·판매 설계서.

- **라인 명칭**: Taste/Depth → **VER.1 아로마 티 블렌딩** / **VER.2 루트 앤드 그레인 로스트** / **TWO KIT SET 프리미엄 아로마 로스트**.
- **원료 교체**: 현미 → **찰수수(sorghum)**, 결명자 → **통보리(whole-barley)**. 카드 2종(수채 컬러판·동판화판)을 기존 카드 톤으로 새로 생성해 `design6/assets/{color,cards}`, `design7/assets/botanicals` 에 배치, 구 파일 삭제.
- **공용 취향 테스트 모듈** `shared/taste-test.js` + `shared/taste-test.css`: 8문항·4결과 유형(A 꽃이 머무는 정원 / B 햇살을 머금은 허브 / C 깊은 뿌리의 로스트 / D 향이 피어나는 로스트) · 기본 레시피 1 + 교차 레시피 1 · 다시 하기 · `?result=` 공유. 호스트 토큰(`--ink --ink-mute --serif-kr --serif-en --sans --u --mono`)만 맞추면 어느 시안에도 마운트.
- **표현 가드(설계서 §18)**: "커피처럼 즐기는 / 커피를 연상시키는 / 커피를 마시던 시간에 제안하는" 만 사용. "커피와 같은 맛·커피보다 건강·완벽 대체·건강/치료/다이어트·카페인" 표현 없음(전 파일 grep 확인).

### 4-1. design6 적용
- 게이트 카피(§16 메인 화면), 헤더 `Taste Test` 버튼 → `#test` 라이트 페이지, `#kit` 페이지를 VER.1/VER.2/SET 비교 + VER.2 레시피 5 + 교차 레시피 5 + 상품 구성 9 + 구매 버튼(§15)으로 재작성, 상세 페이지에 원료별 "향미·역할·주의" 블록(`#pRole`), 엔딩 버튼 → `openKit()`.
- **라운드 4 조작 수정(대표 요청)**: 휠 = 좌우 이동만, **마우스 Y 위치가 윗열/아랫열 조향**(`steerY = -mouse.y·rowGap·.95` → `rowsY` 러프, 이동 속도에 비례해 링 반경 살짝 후퇴), 터치는 드래그 dy가 조향, ↑↓ 키는 열 단위 이동.
- 상세 **대각선 이동 취소**: 히어로 타일은 페이지 스크롤과 1:1로 위로만 이동(`x=0, ry=0`), GL 여행 이미지 제거 → DOM `.fig` 배경 이미지(컬러판 / 다음 카드 동판화) 복원, 배경 드리프트 제거.
- **유럽 미장 배경**: 게이트 `plaster-eu-1.jpg`(텍스트는 잉크색, 파편 밀도 .6 + 텍스트 뒤 미장색 글로우), 상세 GL 배경은 fbm 마블 → `plaster-eu-2.jpg` 텍스처 cover 셰이더(`uCover`로 화면 비율 보정).
- **아카이브(카드 링) 바탕도 미장**(2026-09-17 추가 요청): WebGL 캔버스를 `alpha:true` 투명으로 바꾸고 `#canvas-wrapper` 배경에 `plaster-eu-2.jpg`를 깔아 링 뒤가 미장이 되게 함. 상하 페이드는 흰색 → 미장색(rgba 236,231,221), 엔딩 시 타일 바램 목표색도 미장 톤. 상세의 GL 미장 쿼드는 같은 텍스처·cover 매핑이라 이어져 보임.

### 4-2. design7 적용
- 히어로 사이드 카피(§16), 헤더 CTA `취향 테스트`(모달), GNB 02 Botanicals(VER.1/VER.2) · 03 The Kit(#kit-ver1/ver2/set) · 04 Taste Test.
- SECT1 → VER.1 아로마(아이브로 + "오늘의 기분을 닮은 향을 골라보세요." + 원료 역할 카피, 라벨 *Aroma*), SECT4 → VER.2 로스트(백워드 *Roast/로스트*, 헤드라인 "커피의 분위기는 남기고…", 둥굴레·찰수수·단팥·통보리·민들레 뿌리·보리).
- 신규 섹션: `#test` 테스트 밴드(미장 텍스처) · `#kit` 세 키트 카드(태그·소개·원료·핵심 가치·핵심 카피·§15 버튼) + 확장 문구 + 이유 3열 + 상품 구성 + VER.2 레시피/교차 레시피 2열. 스토리 인용은 §13 개발 이야기, part3 포지셔닝 문장, 푸터 CTA "내 취향의 한 잔, 가장 먼저 만나보기".
- 테스트 모달 `#ttModal`(paper 패널 + 미장 텍스처, ESC/배경 클릭 닫기, `?test`·`?result=` 자동 오픈). 결과의 "추천 키트 자세히 보기" → 모달 닫고 해당 키트 카드 하이라이트(`.hl`) + 스크롤.

### 4-3. 검증 (2026-09-17)
- Browser pane: design6 게이트 → 진입 → 마우스 상/하 호버로 열 전환 확인, 휠 시 `IN.target.y === 0`, 카드 클릭 → 상세(타일 x=0·ry=0, 미장 배경, DOM 이미지) 콘솔 오류 0. design7 테스트 모달 8문항(D) → 유형 D → 키트 버튼 → `#kit-set.hl` 스크롤, 콘솔 오류 0, 에셋 90건 전부 200.
- Headless Chrome(d3d11) 캡처: `docs/preview-round4-2026-09-17.jpg`, `docs/preview-shop-2026-09-17.jpg`.

## 5. 구매 버튼 → 상품 상세 (카페24 관례형) `design6/product.html` · `design7/product.html`
2026-09-17 대표 요청: "구매버튼 실제 카페24 상품상세화면 조사해서 보편적인 상품 상세 화면으로 링크".

### 5-1. 조사 요약
- **카페24 스마트디자인 `product/detail.html` 모듈 순서**(sdsupport.cafe24.com/module/product/detail.html): `product_headcategory`(경로) → `product_detail`[`product_image`+`product_addimage`(대표+확대 썸네일 최대 20) → `product_detaildesign`(어드민 설정 상품정보 표: 상품명·판매가·적립금·배송방법·배송비·원산지…) → `product_option`(옵션 select, "(최소주문수량 N개 이상 / 최대주문수량 N개 이하)") → 선택 상품 목록(상품명/상품수/가격, 수량증가·감소) → "총 상품금액(수량)" → `product_action`(**바로구매하기·장바구니 담기·관심상품등록**, SOLD OUT)] → 상세정보/구매안내/후기/문의 탭 → `product_relation`(관련상품) → 최근 본 상품.
- **실제 티 쇼핑몰(아망티, 카페24)**: 기본 정보 표에 식품 항목(식품의 유형·용량,수량·원재료명 및 함량·수입신고)이 흡수, 옵션은 용량 버튼형, 탭 = 상품상세정보/상품구매안내/관련상품/상품후기 0/상품문의 0, 구매안내는 배송안내·주문 안내·교환/반품 안내("맛, 향 등 개인취향에 따른 교환 및 반품 불가")·상담 문의, 게시판은 "게시물이 없습니다" + 후기작성하기/모두보기.
- **상품정보제공고시 (21) 가공식품 11항목**(guide.godo.co.kr): 제품명 / 식품의 유형 / 생산자 및 소재지 / 제조연월일·소비기한 / 포장단위별 용량·수량 / 원재료명 및 함량 / 영양성분 / 유전자변형식품 표시 / 소비자 안전 주의사항 / 수입식품 문구 / 소비자 상담 전화번호.

### 5-2. 구현
- 시안별 페이지 `design6/product.html?p=…`(표본 라벨 문법: 동판화 카드 표본 프레임·호버 시 수채판, 타자기체 번호 탭, 헤어라인 리스트, `.cta` 채움 호버) · `design7/product.html?p=…`(라이트 에디토리얼: 카페24 기본 스킨에 가장 가까운 표 형태). 데이터는 `shared/product-data.js`(PRODUCTS·OPTIONS·PACK), 흐름은 `shared/product-core.js`(`ProductPage.mount` — 같은 id 훅에 각 시안이 자기 CSS/마크업을 입힘). 위 모듈 순서를 그대로 따른다. 상단 **DEMO 바**(가격·배송비·표시사항은 운영 정보 확정 후 교체), 판매가는 **예시가 칩**, 표시사항 표의 미확정 항목은 "확정 예정/확인 중" 주석.
- 동작: 썸네일 전환, 옵션 select → 선택 상품 행 추가·수량 ±·삭제 → 총 상품금액 합산, 바로구매/장바구니/관심상품(데모 토스트, 장바구니 카운트), 링크 복사, 탭 스크롤스파이, 관련상품(다른 두 키트), 모바일 하단 고정 구매바.
- 연결: design7 키트 카드 버튼 3개 → `product.html?p=…`, design6 키트 페이지 CTA 3개 → `product.html?p=…`(표본실 헤더의 Close는 `index.html?enter&page=kit`). 취향 테스트 결과의 "추천 키트 자세히 보기"는 키트 섹션으로 가고, 그 안의 버튼이 상품 상세로 이어짐. 상품 페이지의 "시안으로 돌아가기"는 진입한 시안으로 복귀.
- 표현 가드: 상세 하단 법적 고지 "본 제품은 차(침출차)이며 커피가 아닙니다 … 커피와 동일한 제품이 아니며 건강·치료 효과를 표방하지 않습니다."
- 옛 패키지 목업(`box-front.jpg`, TASTE/DEPTH 문구)은 상품 이미지에서 제외 — 새 패키지 촬영본으로 교체 필요.

## 3. 남은 작업
- [ ] 대표 확인: 시안 6(아카이브형) vs 시안 7(에디토리얼형) 방향 선택 → 선택안에 카페24 CTA·Journal·클래스 페이지 확장
- [ ] design6 카드 12장 실사 스캔본 교체(현재 시트 크롭 + 4K 업스케일, 찰수수·통보리는 생성 이미지), 모바일 드래그 감도 튜닝
- [ ] 설계서 §3·§18 "시음 후 확정" 항목(비율 단위·물양·온도·레시피명·통보리 표시 명칭) 확정되면 두 시안 + `shared/taste-test.js` 동시 갱신
- [ ] `design6/7 product.html` → 실제 카페24 상품 URL(`/product/detail.html?product_no=`)로 교체, 판매가·배송비·표시사항·고객센터 번호 확정 입력, 새 패키지 촬영본 교체
- [ ] design7 EN/FR 언어 슬롯 실제 연결, 슬라이더 자동재생 접근성(pause on hover)
- [ ] 폰트 서브셋 · webp 변환 · OG 메타

### 5-3. 배포
- GitHub Pages(main, `/`): https://jeonjaeman.github.io/teablendingkit/ — design6/design7/product 페이지는 각 폴더 아래 `product.html?p=ver1|ver2|set`.
