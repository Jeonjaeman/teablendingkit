# site2 — 취향의 권리 공식 홈페이지 (v1.1)

레퍼런스: https://chiran-omoiire.com/en/ (お茶のはまだ, Awwwards SOTD 2018)의 분위기·스타일·단락 구성을 인용해 만든 두 번째 시안이 공식 홈페이지가 됐다(10/25 대표 결정). `site/`(상자 열어보기 3D 연출)는 와디즈 상세페이지용으로 두고, 둘은 서로 링크하지 않는다.

버전 기록은 [CHANGELOG.md](CHANGELOG.md), 수정 요청서 원본은 `docs/수정요청/`. git 태그 `site2-vX.Y`.

## 페이지

| 메뉴 | 파일 | 내용 |
|---|---|---|
| 홈 | `index.html` | 히어로(작은 문구 → 메인 카피 「직접 고르고 섞는 차, 취향의 권리」 → 서브 카피 → 키트 보기/원료 보기) → 판매 품목 4칸 → 브랜드 한 줄 |
| 원료 | `ingredients.html` | 허브 6 + 곡물·뿌리 6 단품 목록. 상태 배지(오픈 예정/판매 중/품절) · 중량 10g~1kg · 버전/상태 필터 · 입고 알림 신청 |
| 원료 상세 | `ingredient.html?id=<key>` | 한 장으로 12종 모두. 사진 · 향·바디·여운 · 중량별 가격표(소비자가 + 강사 등급가 미리 보기) · 우리는 온도·시간 · 추천 블렌드 · 이전/다음 |
| 키트 | `products.html` | VER.1 Taste · VER.2 Depth · 세트 → 「고르기 어려우신가요?」 1분 취향 찾기(보조 도구) → 즐기는 법(우리는 법 · 보관법 · 차 이야기) |
| 교육 | `education.html` | 교육 재료·자료 품목(수업용 키트 · 노트 · 교재 · 원료 리필) — 품목·가격 대표 제공 예정 |
| 강사 | `partners.html` | 파트너 혜택 → 가입 신청 폼(검토 후 승인) / 강의 의뢰 문의 폼(기관·개인) |
| 브랜드 이야기 | `about.html` | Point 1~4 + 만든 사람(이소연, 작게) + 마무리 |
| 블렌딩 (보조) | `blends.html` | 비율 → 원칙 → 고르기·담기·붓기·우리기·기록하기 → 레시피 9종(`#r-<id>`) |
| 구매 안내 (보조) | `shop.html` | 구매처 → 주문(키트 3종) → 티아포테카 → 연혁(책은 표지 전체) → Outline |
| 문의 (보조) | `contact.html` | 4칸 폼(접수 서버 없음 → mailto, 주소 교체 필요) |
| 옛 주소 | `guide.html`, `enjoy.html` | 각각 원료·키트 페이지로 자동 이동 |

공통 틀(`omoiire.js`): 왼쪽 엠블럼 · 오른쪽 레일(Shop · 메뉴 · Page top) · 햄버거 메뉴(상단 5 + 보조 3, 브랜드 무비) · 빵부스러기 · 푸터(정방형 로고 + 메뉴 5).

## 데이터 — `catalog.js`
원료·레시피·교육 품목은 모두 여기. **원료 추가·품절·가격 변경은 이 파일만 고친다.**
- `ingredients[]`: `key no kr en sci ver(taste|depth) a b f(향·바디·여운 5점) liq brew status(soon|open|soldout) price{10,50,100,200,1000} feat bio`. 가격 `null` → 「가격 미정」. 효능 문구는 넣지 않는다.
- `tiers[]`: 소비자가 / 강사 1·2·3등급(30·40·50% 할인). 지금은 단품 페이지 「가격 보기」로 미리 보기(localStorage `rtt_tier`). 실제 회원 등급·결제는 쇼핑몰 연동 때.
- `recipes[]`: 이름 · 버전(VER.1/VER.2/교차) · `items[[key, 비율]]` · brew · note. 출처·제안자는 적지 않는다.
- `education[]`: 품목 · 가격(미정) · 상태.
- 입고 알림 신청: 접수 서버가 없어 브라우저(localStorage `rtt_notify`)에 기억하고 메일 신청 링크를 준다. 연동 때 교체.

## 로고 (10/24)
- 가로형 `img/logo.svg`(로고 PDF 벡터) — 홈 히어로, 취향 테스트 창 머리.
- 정방형 `img/logo-sq.png` — 푸터.
- 가로 띠형 `img/logo-wide.png`(496px JPG 원본) — 햄버거 메뉴 머리.
- 왼쪽 위 고정 버튼은 엠블럼만(`wadiz/assets/emblem.svg`).

## 취향 테스트
`quiz.js`(8문항, 결과 A~D, site2 디자인 문법). 10/25부터는 키트 페이지의 보조 도구(`products.html#find`)에서만 연다. `?result=A`로 결과 화면 공유 가능. 결과 → `products.html?pick=ver1|ver2|set`.

## 자산
- 새로 만든 것(GPT Image 2.5 via Higgsfield): `img/hero.jpg`, `img/enjoy_top.png`·`img/enjoy_01~04.png`(현재 미사용), `img/cup_taste.jpg`·`img/cup_depth.jpg`(브랜드 이야기 Point 3).
- 기존 것 재사용: `wadiz/assets/real/herb_*.png`(3차수정 실사 누끼 12 — 원료 목록·상세), `wadiz/assets/photo/*`, `wadiz/assets/gen/*`, `wadiz/assets/3d/*`.
- 영상: 새로 만들 일이 생기면 힉스필드. 지금은 브랜드 필름 재인코딩(`video/brand.mp4`)만.

## 아직
- 대표 제공 예정: 교육 재료·자료 품목과 가격, 원료별 중량 옵션 가격 → `catalog.js`.
- 카카오 채널 URL(「연결 예정」), 문의·가입·알림 메일 주소(`hello@example.com`), 영어판.
- 회원(강사 승인·등급가 자동 표시)·장바구니·결제·입고 알림 접수는 쇼핑몰 연동 때. 지금은 구조와 화면만.
- 「가격·구성은 와디즈 리워드 기준이며 확정 전」 문구는 판매가 확정 후 수정.
- 와디즈 상세페이지의 양진호 블록은 별도 확인(요청서 3쪽).
