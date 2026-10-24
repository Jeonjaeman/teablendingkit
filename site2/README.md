# site2 — 취향의 권리 두 번째 시안 (chiran-omoiire.com 인용)

레퍼런스: https://chiran-omoiire.com/en/ (お茶のはまだ, Awwwards SOTD 2018). 분위기·스타일·페이지와 단락 구성을 그대로 따르고, 내용만 취향의 권리로 바꿨다(10/24 전재만 지시).

## 페이지 대응

| 레퍼런스 | site2 | 단락 구성(그대로) |
|---|---|---|
| Home (커버 한 장: 사진 · 로고+2열 메뉴 · 하단 태그라인) | `index.html` | 사진 `img/hero.jpg`(GPT Image 2.5 생성), 로고 + 5개 메뉴, "Life is an endless blending." |
| Products (제목/소개 → 필터 칩 → 3열 카드) | `products.html` | 버전(Taste/Depth)·태그 칩, 키트 3 + 원료 낱개 12(오픈 예정) |
| About Chiran Tea (Point 1~4, 왼쪽 고정 포인트 내비, 마무리 와이드 사진 + 두 줄) | `about.html` | 1 취향은 완성되어 갑니다 · 2 열두 원료 4,000 조합(숫자) · 3 Taste/Depth 두 잔 · 4 고재의 그릇 |
| Tea Guide (T-01~06 찻물 원, 품종별 레이더·사진·Feature/Biography·버튼) | `guide.html` | T-01~12 원료 — 목록은 3차수정 실사 누끼(`wadiz/assets/real/herb_*.png`, 10/24 전재만: 색 원 대신 원료 사진), 항목은 찻물 색 원을 빼고 그 자리에 레이더(원 크기), 레이더 자리에 「이 원료가 든 키트」 버튼, 오른쪽은 실사. 12개 항목 모두 같은 구성(좌우 번갈아 쓰지 않음, 10/24). 레이더는 와디즈 원료 노트의 향·바디·여운 3축(5점) |
| Hamada Blends (에세이: 블렌딩 → 차사(Chashi) 두 사람 → 작업 01~05 → 마무리) | `blends.html` | 비율 → 이소연·양진호 → 고르기·담기·붓기·우리기·기록하기 → 레시피 2개 |
| Tashinamu (큰 일러스트 + 사전 풀이 + 카드 4) | `enjoy.html` | 취향(趣向) 사전 풀이 + 취향 찾기·우리는 법·보관법·차 이야기 |
| Shop Information (사진+주소 → Company outline → 연혁 타임라인 → Outline/Privacy) | `shop.html` | 구매처 → 주문(키트 3종) → 티아포테카 → 2020·2024·2026 연혁(책은 항상 표지 전체, 자르지 않음 — 10/24) → Outline |
| Contact (4칸 폼) | `contact.html` | 회사명·이름·이메일·문의 (접수 서버 없음 → mailto, 주소 교체 필요) |
| 햄버거 메뉴(흰 오버레이, 2열 목록, 브랜드 무비 썸네일, 언어) | `omoiire.js`가 모든 페이지에 삽입 | Brand Movie = `video/brand.mp4`(기존 brand_v2 마스터를 720p로 줄임) |

## 취향 테스트(가장 중요 — 어디서든 한 번에)
- 오른쪽 레일의 초록 세로 버튼 「취향 찾기」, 홈 커버의 「1분 취향 찾기 →」, 메뉴 첫 줄, 즐기는 법 카드, 키트·블렌딩 페이지 버튼 — 모두 같은 오버레이(`#quiz`)를 연다. `#quiz` 해시나 `?quiz`로도 열린다.
- 테스트 본체는 site2 전용 `quiz.js`(8문항, 결과 A~D, site2 디자인 문법). `site/`의 `shared/taste-test.js`와는 데이터만 같고 코드·스타일은 독립. 결과의 「추천 키트 보기」 → `products.html?pick=ver1|ver2|set` → 해당 카드에 「취향 테스트 추천」 표시와 함께 스크롤. `?result=A` 링크로 결과 화면을 바로 열 수 있다(공유용).
- **site/ 와 site2/ 는 서로 링크하지 않는다**(10/24 전재만). 구매는 `shop.html#order`(키트 3종, 주문 버튼은 펀딩 오픈 시 연결).

## 로고(10/24 전재만: 세 가지를 자리에 맞게)
- 가로형 `img/logo.svg`(로고 PDF를 벡터로 뽑음) — 홈 커버 브랜드 블록(데스크톱), 취향 테스트 창 머리.
- 정방형 `img/logo-sq.png`(엠블럼 위·이름 아래) — 푸터, 모바일 커버(세로 박스).
- 가로 띠형 `img/logo-wide.png`(엠블럼 + 스케치 띠) — 햄버거 메뉴 머리. 원본이 496px JPG라 큰 자리에는 쓰지 않는다.
- 왼쪽 위 고정 버튼은 엠블럼만 둥글게(`wadiz/assets/emblem.svg`) 그대로.

## 자산
- 새로 만든 것(GPT Image 2.5 via Higgsfield): `img/hero.jpg`, `img/enjoy_top.png`, `img/enjoy_01~04.png`(선화 일러스트), `img/cup_taste.jpg`·`img/cup_depth.jpg`(About Point 3 — 유리잔 옆모습으로 찻물 색, 10/24 지시: 위에서 찍은 구도 말고 옆에서).
- 기존 것 재사용: `wadiz/assets/real/herb_*.png`(3차수정 실사 누끼 12 — 가이드 목록·항목·키트 페이지 원료 카드), `wadiz/assets/photo/*`(인물·손·잔), `wadiz/assets/gen/*`, `wadiz/assets/3d/*`(상자 렌더).
- 영상: 새로 만들 일이 생기면 힉스필드(전재만 지시). 지금은 기존 브랜드 필름 재인코딩만.

## 아직
- 카카오 채널 URL, 문의 메일 주소(`contact.html`의 hello@example.com), 영어판(메뉴의 English는 비활성).
- 원료 낱개 가격·오픈 시점(FAQ에 "취향의권리.com에서 낱개 구매" 예고만 있음).
- 레퍼런스의 상품 찜(하트)은 장식만 — 기능 없음.
