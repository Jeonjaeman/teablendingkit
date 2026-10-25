/* 취향의 권리 · 원료 카탈로그 (site2 v1.1, 2026-10-25 1차 수정 요청)
   원료를 추가하거나 품절·가격을 바꿀 때는 이 파일만 고친다. 모든 페이지가 omoiire.js 앞에서 읽는다.
   - status : 'soon'(오픈 예정) | 'open'(판매 중) | 'soldout'(품절)
   - price  : 중량(g)별 소비자가(원). 아직 정해지지 않은 값은 null → 화면에 '가격 미정'
   - tiers  : 강사 회원 등급별 할인율(소비자가 대비). 로그인·승인은 쇼핑몰 연동 때 붙고, 지금은 화면에서 등급을 골라 미리 볼 수 있다. */
window.RTT_CATALOG = {
  weights: [10, 50, 100, 200, 1000],
  tiers: [
    { id: 'guest', name: '소비자가', off: 0 },
    { id: 't1', name: '강사 1등급 · 30%', off: .30 },
    { id: 't2', name: '강사 2등급 · 40%', off: .40 },
    { id: 't3', name: '강사 3등급 · 50%', off: .50 },
  ],
  /* 레시피 — 이름은 그대로 두고 출처·제안자는 적지 않는다(10/25 요청). items: [원료 key, 비율] */
  recipes: [
    { id: 'rosegarden', name: '로즈가든', ver: 'VER.1', items: [['chamomile', '2'], ['rose', '1'], ['lemon_balm', '1']], brew: '95~100°C · 150ml · 3~5분', note: '부드러운 캐모마일 위로 장미의 꽃향이 길게 머무는, 첫 번째로 권하는 블렌드.' },
    { id: 'garden_floral', name: '가든 플로럴', ver: 'VER.1', items: [['rose', '2'], ['chamomile', '1'], ['lemon_balm', '½']], brew: '95~100°C · 150ml · 3~5분', note: '꽃향을 중심에 두고 레몬밤으로 첫 향을 살짝 밝힙니다.' },
    { id: 'sunlight', name: '선라이트 시트러스', ver: 'VER.1', items: [['yuza', '2'], ['hibiscus', '1'], ['lemon_balm', '1'], ['peppermint', '½']], brew: '95~100°C · 150ml · 3~5분', note: '밝은 산미와 상쾌한 여운. 아이스티로도 잘 어울립니다. 페퍼민트는 소량부터.' },
    { id: 'brazilian', name: '브라질리언 로스트', ver: 'VER.2', items: [['dandelion_root', '2'], ['red_bean', '2'], ['sorghum', '1'], ['solomons_seal', '½']], brew: '100°C · 150ml · 7분 이상', note: '깊게 볶은 듯한 첫 향에 단팥과 찰수수의 부드러운 구수함이 이어집니다.' },
    { id: 'deepwood', name: '딥 우드 로스트', ver: 'VER.2', items: [['dandelion_root', '2'], ['solomons_seal', '2'], ['red_bean', '1']], brew: '100°C · 150ml · 7분', note: '볶은 뿌리와 나무를 연상시키는 깊은 향, 둥굴레의 부드러운 바디감, 단팥의 고소한 마무리.' },
    { id: 'milktea', name: '밀크티 무드', ver: '교차', items: [['red_bean', '2'], ['chamomile', '1½'], ['brown_rice', '1'], ['solomons_seal', '1']], brew: '100°C · 150ml · 7분', note: '단팥과 현미의 고소함 위에 캐모마일이 부드럽게 얹히는, 두 키트를 함께 가졌을 때의 한 잔.' },
    { id: 'rosegrain', name: '로즈 그레인', ver: '교차', items: [['rose', '1'], ['chamomile', '1'], ['barley', '2']], brew: '100°C · 150ml · 5~7분', note: '우아한 꽃향과 맑은 곡물의 여운이 만나는 플로럴 로스트.' },
    { id: 'yuja_roast', name: '유자 로스트', ver: '교차', items: [['yuza', '1'], ['dandelion_root', '2'], ['red_bean', '1']], brew: '100°C · 150ml · 7분', note: '유자의 밝은 첫 향 뒤에 깊은 볶음 향과 부드러운 고소함이 이어지는 시트러스 로스트.' },
    { id: 'mint_roast', name: '민트 로스트', ver: '교차', items: [['peppermint', '½'], ['lemon_balm', '1'], ['barley', '2']], brew: '100°C · 150ml · 5~7분', note: '상쾌하게 시작해 구수하고 깔끔하게 끝나는 허벌 로스트.' },
  ],
  /* 원료 12종 (와디즈 E안 원료 노트 · hwpx 향 노트). 효능 문구는 넣지 않는다. */
  ingredients: [
    { key: 'lemon_balm', no: 'T-01', kr: '레몬밤', en: 'Lemon Balm', sci: 'Melissa officinalis', ver: 'taste', a: 4, b: 2, f: 3, liq: '#E3E4A8', brew: '95~100°C · 150ml · 3~5분', status: 'soon', price: { 10: null, 50: null, 100: null, 200: null, 1000: null },
      feat: '레몬과 풋잎을 떠올리게 하는 산뜻함. 첫 향을 밝게 엽니다. 청향 · 은은한 단맛 · 시트러스.',
      bio: '지중해가 고향인 민트과 허브. 잎을 비비면 레몬 향이 나 이름이 붙었습니다. 블렌딩에서는 첫 향을 열어 주는 역할을 맡아, 어떤 원료와도 무리 없이 섞입니다.' },
    { key: 'hibiscus', no: 'T-02', kr: '히비스커스', en: 'Hibiscus', sci: 'Hibiscus sabdariffa', ver: 'taste', a: 3, b: 3, f: 4, liq: '#B3303F', brew: '95~100°C · 150ml · 3~5분', status: 'soon', price: { 10: null, 50: null, 100: null, 200: null, 1000: null },
      feat: '붉은 과일을 연상시키는 선명한 산미. 수색을 루비 레드로 바꿉니다.',
      bio: '꽃이 아니라 꽃받침(꽃받침잎)을 말린 원료입니다. 한 꼬집만 더해도 잔의 색이 달라져, 눈으로 먼저 즐기는 블렌딩의 중심이 됩니다.' },
    { key: 'peppermint', no: 'T-03', kr: '페퍼민트', en: 'Peppermint', sci: 'Mentha × piperita', ver: 'taste', a: 5, b: 2, f: 4, liq: '#D6E2BE', brew: '95~100°C · 150ml · 3~5분', status: 'soon', price: { 10: null, 50: null, 100: null, 200: null, 1000: null },
      feat: '차갑고 깨끗한 상쾌함. 멘톨 · 맑음 · 은은한 단맛. 소량부터 시작하세요.',
      bio: '워터민트와 스피어민트의 교잡종. 향이 강해 비율의 작은 차이가 한 잔을 크게 바꿉니다. 여운을 정리하고 싶을 때 반 스푼이면 충분합니다.' },
    { key: 'yuza', no: 'T-04', kr: '유자', en: 'Yuja', sci: 'Citrus junos', ver: 'taste', a: 4, b: 2, f: 3, liq: '#EBD38A', brew: '95~100°C · 150ml · 3~5분', status: 'soon', price: { 10: null, 50: null, 100: null, 200: null, 1000: null },
      feat: '밝은 감귤 껍질 향과 은은한 쌉싸름함. 느린 시트러스.',
      bio: '껍질을 말린 원료라 과육의 단맛보다 껍질의 향과 가벼운 쓴맛이 앞섭니다. 꽃 향 원료 사이에 넣으면 전체를 또렷하게 세워 줍니다.' },
    { key: 'rose', no: 'T-05', kr: '장미', en: 'Rose', sci: 'Rosa damascena', ver: 'taste', a: 5, b: 3, f: 5, liq: '#E2B7A9', brew: '95~100°C · 150ml · 3~5분', status: 'soon', price: { 10: null, 50: null, 100: null, 200: null, 1000: null },
      feat: '우아하고 풍성한 꽃향. 긴 아로마와 여운.',
      bio: '다마스크 장미의 꽃잎과 봉오리. 향은 길고 맛은 담백해서, 다른 원료의 맛 위에 향만 얹고 싶을 때 씁니다. 첫 번째로 권하는 레시피 「로즈가든」의 중심입니다.' },
    { key: 'chamomile', no: 'T-06', kr: '캐모마일', en: 'Chamomile', sci: 'Matricaria chamomilla', ver: 'taste', a: 3, b: 2, f: 3, liq: '#E8D27A', brew: '95~100°C · 150ml · 3~5분', status: 'soon', price: { 10: null, 50: null, 100: null, 200: null, 1000: null },
      feat: '사과와 꿀을 연상시키는 부드러운 향. 사과 · 꽃 · 꿀 · 건초.',
      bio: '저녁의 차로 오래 사랑받아 온 국화과 꽃. 부드러운 바디가 어느 원료든 감싸 주어, 처음 블렌딩을 시작하는 분께 가장 먼저 권하는 바탕 원료입니다.' },
    { key: 'solomons_seal', no: 'T-07', kr: '둥굴레', en: "Solomon's Seal", sci: 'Polygonatum odoratum', ver: 'depth', a: 2, b: 4, f: 3, liq: '#D7B688', brew: '100°C · 150ml · 7분', status: 'soon', price: { 10: null, 50: null, 100: null, 200: null, 1000: null },
      feat: '부드러운 볶은 뿌리와 은은한 단맛. 바디감을 둥글게 만듭니다.',
      bio: '뿌리줄기를 쪄서 말리고 볶은 원료. 혼자서도 구수하지만, 곡물 원료 사이에서 단맛을 잇는 다리 역할을 할 때 가장 빛납니다.' },
    { key: 'sorghum', no: 'T-08', kr: '찰수수', en: 'Glutinous Sorghum', sci: 'Sorghum bicolor', ver: 'depth', a: 2, b: 3, f: 3, liq: '#CDA372', brew: '100°C · 150ml · 7분', status: 'soon', price: { 10: null, 50: null, 100: null, 200: null, 1000: null },
      feat: '담백하고 순한 곡물의 구수함. 뿌리 원료를 받쳐 줍니다.',
      bio: '볶은 수수알. 향이 튀지 않아 깊이 있는 원료(민들레 뿌리·단팥)의 바닥을 받쳐 주는 데 씁니다. 비율을 늘려도 한 잔이 무거워지지 않습니다.' },
    { key: 'red_bean', no: 'T-09', kr: '단팥', en: 'Red Bean', sci: 'Vigna angularis', ver: 'depth', a: 3, b: 4, f: 4, liq: '#A65F4B', brew: '100°C · 150ml · 7분', status: 'soon', price: { 10: null, 50: null, 100: null, 200: null, 1000: null },
      feat: '볶은 팥의 고소하고 부드러운 여운.',
      bio: '볶은 팥을 굵게 깨서 말렸습니다. 우리면 익숙한 단팥의 향이 올라와, 커피를 마시던 시간에 두는 한 잔의 중심이 됩니다. 교차 블렌드 「밀크티 무드」의 바탕입니다.' },
    { key: 'brown_rice', no: 'T-10', kr: '현미', en: 'Brown Rice', sci: 'Oryza sativa', ver: 'depth', a: 2, b: 3, f: 2, liq: '#D2A662', brew: '100°C · 150ml · 7분', status: 'soon', price: { 10: null, 50: null, 100: null, 200: null, 1000: null },
      feat: '볶은 쌀의 담백하고 고소한 향. 바디를 받쳐 줍니다.',
      bio: '현미를 볶아 튀운 원료. 향보다 질감을 더하는 쪽이라, 어떤 곡물 블렌드에도 한 스푼을 더하면 입안이 둥글어집니다.' },
    { key: 'dandelion_root', no: 'T-11', kr: '민들레 뿌리', en: 'Dandelion Root', sci: 'Taraxacum officinale', ver: 'depth', a: 4, b: 5, f: 5, liq: '#6B4730', brew: '100°C · 150ml · 7분', status: 'soon', price: { 10: null, 50: null, 100: null, 200: null, 1000: null },
      feat: '흙 · 나무 · 커피 · 카카오를 연상시키는 깊은 볶음 향. 중심 원료.',
      bio: '뿌리를 잘라 깊게 볶았습니다. 열두 원료 중 가장 깊고 진해, 비율 하나로 한 잔의 무게를 정합니다. 커피 대신 찾는 분이라면 여기서 시작하세요.' },
    { key: 'barley', no: 'T-12', kr: '보리', en: 'Barley', sci: 'Hordeum vulgare', ver: 'depth', a: 3, b: 3, f: 3, liq: '#AE7843', brew: '100°C · 150ml · 7분', status: 'soon', price: { 10: null, 50: null, 100: null, 200: null, 1000: null },
      feat: '익숙하고 선명한 볶은 곡물 향.',
      bio: '누구에게나 익숙한 볶은 보리. 그 익숙함 덕에 새로운 원료를 더해도 낯설지 않게 받아 줍니다. Depth 블렌딩의 출발점으로 가장 안전한 원료입니다.' },
  ],
  /* 교육 재료·자료 — 품목·가격은 대표 제공 예정(10/25 요청서 4쪽). 들어오면 여기만 채운다. */
  education: [
    { id: 'class_kit', name: '수업용 블렌딩 키트', sub: '원료 12종 소분 · 빈 티백 · 스쿱 · 노트', price: null, status: 'soon', desc: '한 반이 함께 쓰는 수업용 구성. 인원수에 맞춰 원료 소분을 늘릴 수 있습니다.' },
    { id: 'note', name: '블렌딩 노트', sub: '비율·감상 기록 노트 · 고재 결 표지', price: null, status: 'soon', desc: '키트에 든 것과 같은 노트. 수업과 개인 기록용으로 낱권 판매합니다.' },
    { id: 'textbook', name: '티 블렌딩 교재', sub: '원료 12종 · 비율 · 우리기 · 기록법', price: null, status: 'soon', desc: '취향의 권리 방식으로 블렌딩을 가르치는 교재. 강사 회원에게 먼저 엽니다.' },
    { id: 'refill', name: '수업용 원료 리필', sub: '허브·곡물 12종 · 대용량', price: null, status: 'soon', desc: '수업에서 많이 쓰는 원료를 대용량으로. 강사 회원 등급가가 적용됩니다.' },
  ],
};
