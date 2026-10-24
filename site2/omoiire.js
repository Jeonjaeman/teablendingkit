/* 취향의 권리 — 두 번째 시안 공통 스크립트
   페이지마다 같은 틀(왼쪽 엠블럼 · 오른쪽 레일 · 메뉴 오버레이 · 브랜드 무비 · 빵부스러기 · 푸터)을 끼워 넣고,
   스크롤 등장(.rv), 포인트 내비, 상품 필터, 원료 가이드 렌더를 맡는다. */
(function () {
  const PAGES = [
    ['index.html', '홈', 'Home'],
    ['products.html', '키트', 'Kit'],
    ['about.html', '취향의 권리', 'About'],
    ['guide.html', '원료 가이드', 'Ingredient Guide'],
    ['blends.html', '블렌딩', 'Blending'],
    ['enjoy.html', '즐기는 법', 'How to enjoy'],
    ['shop.html', '구매 안내', 'Shop Information'],
    ['contact.html', '문의', 'Contact'],
  ];
  const SHOP = 'shop.html#order';                 // 구매는 site2 안에서(구매 안내의 주문 구역). site/ 와는 서로 독립
  const here = location.pathname.split('/').pop() || 'index.html';
  const page = PAGES.find(p => p[0] === here) || PAGES[0];
  const EMBLEM = '../wadiz/assets/emblem.svg';

  /* ── 공통 틀 ── */
  const chrome = document.createElement('div');
  chrome.innerHTML = `
  <a class="lg" href="index.html" aria-label="취향의 권리 홈"><img src="${EMBLEM}" alt=""></a>
  <div class="rail">
    <div class="top"><a class="rl-shop" href="${SHOP}">Shop</a><button class="rl-quiz" data-quiz type="button">취향 찾기</button></div>
    <button class="rl-menu" aria-label="메뉴 열기"><i></i><i></i><i></i></button>
    <a class="rl-top" href="#top">Page top</a>
  </div>
  <div id="quiz" aria-hidden="true"><div class="q-top"><a class="q-logo" href="index.html"><img src="img/logo.svg" alt="취향의 권리 · the right to taste"></a><button class="q-close" type="button">닫기 ✕</button></div><div id="quizMount"></div></div>
  <div id="menu" aria-hidden="true">
    <div class="m-top">
      <a class="m-logo" href="index.html"><img class="logo" src="img/logo-wide.png" alt="취향의 권리 · the right to taste"></a>
      <a class="m-shop" href="${SHOP}">Online Shop</a>
    </div>
    <ul class="m-list"><li><a href="#quiz" class="q" data-quiz>1분 취향 찾기</a></li>${PAGES.slice(1).map(p => `<li><a href="${p[0]}" class="${p[0] === here ? 'cur' : ''}">${p[1]}</a></li>`).join('')}</ul>
    <button class="m-close" aria-label="닫기"></button>
    <div class="m-bottom">
      <div class="lang"><a href="https://www.instagram.com/right.totaste/" target="_blank" rel="noopener" style="margin-right:14px">Instagram</a> <u>한국어</u> / <span title="준비 중">English</span></div>
      <div class="copy">© THE RIGHT TO TASTE.</div>
      <button class="m-movie" type="button"><span class="th" style="background-image:url(video/brand.jpg)"></span><span>Brand Movie</span></button>
    </div>
  </div>
  <div id="movie"><button class="x">Close</button><video controls playsinline preload="none" poster="video/brand.jpg" src="video/brand.mp4"></video></div>`;
  document.body.prepend(chrome);

  const tail = document.createElement('div');
  tail.innerHTML = here === 'index.html' ? '' : `
  <div class="bread"><div class="inner"><a href="index.html">Home</a><span>${page[1]}</span></div></div>
  <footer class="ft">
    <img class="logo-sq" src="img/logo-sq.png" alt="취향의 권리 · the right to taste">
    <div class="ad">만든 곳 · 티아포테카 (Tea Apotheca)<br>문의 · 카카오 채널 / Instagram @right.totaste</div>
    <div class="sns"><a href="contact.html">Contact</a><a href="${SHOP}">Online Shop</a><a href="#quiz" data-quiz>Taste Test</a></div>
    <div class="copy">© 2026 THE RIGHT TO TASTE. ALL RIGHTS RESERVED.</div>
  </footer>`;
  document.body.append(tail);

  /* ── 메뉴 · 무비 ── */
  const menu = document.getElementById('menu'), movie = document.getElementById('movie'), vid = movie.querySelector('video');
  const openMenu = o => { menu.classList.toggle('open', o); menu.setAttribute('aria-hidden', !o); document.body.style.overflow = o || document.body.classList.contains('home') ? 'hidden' : ''; };
  document.querySelector('.rl-menu').addEventListener('click', () => openMenu(true));
  menu.querySelector('.m-close').addEventListener('click', () => openMenu(false));
  menu.querySelector('.m-movie').addEventListener('click', () => { movie.classList.add('open'); vid.play().catch(() => {}); });
  movie.querySelector('.x').addEventListener('click', () => { movie.classList.remove('open'); vid.pause(); });
  movie.addEventListener('click', e => { if (e.target === movie) { movie.classList.remove('open'); vid.pause(); } });
  document.addEventListener('keydown', e => { if (e.key === 'Escape') { openMenu(false); movie.classList.remove('open'); vid.pause(); } });
  document.querySelectorAll('[data-menu]').forEach(b => b.addEventListener('click', () => openMenu(true)));

  /* ── 취향 테스트 오버레이: site2 전용 모듈(quiz.js)을 처음 열 때 불러와 붙인다 ── */
  const quiz = document.getElementById('quiz'), qm = document.getElementById('quizMount');
  let quizReady = null;
  const loadQuiz = () => quizReady || (quizReady = new Promise(res => {
    const s = document.createElement('script'); s.src = 'quiz.js'; s.onload = () => { RTTQuiz.mount(qm, { onKit(kit) { location.href = `products.html?pick=${kit}#pick`; } }); res(); };
    document.head.appendChild(s); }));
  const openQuiz = async o => { if (o) { await loadQuiz(); openMenu(false); } quiz.classList.toggle('open', o); quiz.setAttribute('aria-hidden', !o);
    document.body.style.overflow = o || document.body.classList.contains('home') ? 'hidden' : ''; if (o) quiz.scrollTo({ top: 0 }); };
  document.addEventListener('click', e => { const b = e.target.closest('[data-quiz]'); if (b) { e.preventDefault(); openQuiz(true); } });
  quiz.querySelector('.q-close').addEventListener('click', () => openQuiz(false));
  document.addEventListener('keydown', e => { if (e.key === 'Escape') openQuiz(false); });
  { const sp = new URLSearchParams(location.search); if (location.hash === '#quiz' || sp.has('quiz') || sp.has('result')) setTimeout(() => openQuiz(true), 300); }

  /* ── 등장 · Page top ── */
  const io = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) { e.target.classList.add('on'); io.unobserve(e.target); } }), { rootMargin: '0px 0px -8% 0px', threshold: .08 });
  const watch = () => document.querySelectorAll('.rv:not(.on)').forEach(el => io.observe(el));
  addEventListener('scroll', () => document.body.classList.toggle('scrolled', scrollY > 300), { passive: true });
  document.querySelector('.rl-top').addEventListener('click', e => { e.preventDefault(); scrollTo({ top: 0, behavior: 'smooth' }); });

  /* ── 포인트 내비 (About) ── */
  const pnav = document.querySelector('.pnav');
  if (pnav) { const items = [...pnav.querySelectorAll('li')], secs = items.map(li => document.getElementById(li.dataset.t));
    const pio = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) { const i = secs.indexOf(e.target); items.forEach((li, k) => li.classList.toggle('on', k === i)); } }), { rootMargin: '-40% 0px -50% 0px' });
    secs.forEach(s => s && pio.observe(s)); items.forEach((li, i) => li.addEventListener('click', () => secs[i].scrollIntoView({ behavior: 'smooth', block: 'start' }))); }

  /* ── 자료: 원료 12종 (와디즈 E안 원료 노트 · hwpx 향 노트) ── */
  const ING = [
    { key: 'lemon_balm', no: 'T-01', kr: '레몬밤', en: 'Lemon Balm', sci: 'Melissa officinalis', ver: 'taste', a: 4, b: 2, f: 3, liq: '#E3E4A8',
      feat: '레몬과 풋잎을 떠올리게 하는 산뜻함. 첫 향을 밝게 엽니다. 청향 · 은은한 단맛 · 시트러스.',
      bio: '지중해가 고향인 민트과 허브. 잎을 비비면 레몬 향이 나 이름이 붙었습니다. 블렌딩에서는 첫 향을 열어 주는 역할을 맡아, 어떤 원료와도 무리 없이 섞입니다.' },
    { key: 'hibiscus', no: 'T-02', kr: '히비스커스', en: 'Hibiscus', sci: 'Hibiscus sabdariffa', ver: 'taste', a: 3, b: 3, f: 4, liq: '#B3303F',
      feat: '붉은 과일을 연상시키는 선명한 산미. 수색을 루비 레드로 바꿉니다.',
      bio: '꽃이 아니라 꽃받침(꽃받침잎)을 말린 원료입니다. 한 꼬집만 더해도 잔의 색이 달라져, 눈으로 먼저 즐기는 블렌딩의 중심이 됩니다.' },
    { key: 'peppermint', no: 'T-03', kr: '페퍼민트', en: 'Peppermint', sci: 'Mentha × piperita', ver: 'taste', a: 5, b: 2, f: 4, liq: '#D6E2BE',
      feat: '차갑고 깨끗한 상쾌함. 멘톨 · 맑음 · 은은한 단맛. 소량부터 시작하세요.',
      bio: '워터민트와 스피어민트의 교잡종. 향이 강해 비율의 작은 차이가 한 잔을 크게 바꿉니다. 여운을 정리하고 싶을 때 반 스푼이면 충분합니다.' },
    { key: 'yuza', no: 'T-04', kr: '유자', en: 'Yuja', sci: 'Citrus junos', ver: 'taste', a: 4, b: 2, f: 3, liq: '#EBD38A',
      feat: '밝은 감귤 껍질 향과 은은한 쌉싸름함. 느린 시트러스.',
      bio: '껍질을 말린 원료라 과육의 단맛보다 껍질의 향과 가벼운 쓴맛이 앞섭니다. 꽃 향 원료 사이에 넣으면 전체를 또렷하게 세워 줍니다.' },
    { key: 'rose', no: 'T-05', kr: '장미', en: 'Rose', sci: 'Rosa damascena', ver: 'taste', a: 5, b: 3, f: 5, liq: '#E2B7A9',
      feat: '우아하고 풍성한 꽃향. 긴 아로마와 여운.',
      bio: '다마스크 장미의 꽃잎과 봉오리. 향은 길고 맛은 담백해서, 다른 원료의 맛 위에 향만 얹고 싶을 때 씁니다. 첫 번째로 권하는 레시피 「로즈가든」의 중심입니다.' },
    { key: 'chamomile', no: 'T-06', kr: '캐모마일', en: 'Chamomile', sci: 'Matricaria chamomilla', ver: 'taste', a: 3, b: 2, f: 3, liq: '#E8D27A',
      feat: '사과와 꿀을 연상시키는 부드러운 향. 사과 · 꽃 · 꿀 · 건초.',
      bio: '저녁의 차로 오래 사랑받아 온 국화과 꽃. 부드러운 바디가 어느 원료든 감싸 주어, 처음 블렌딩을 시작하는 분께 가장 먼저 권하는 바탕 원료입니다.' },
    { key: 'solomons_seal', no: 'T-07', kr: '둥굴레', en: "Solomon's Seal", sci: 'Polygonatum odoratum', ver: 'depth', a: 2, b: 4, f: 3, liq: '#D7B688',
      feat: '부드러운 볶은 뿌리와 은은한 단맛. 바디감을 둥글게 만듭니다.',
      bio: '뿌리줄기를 쪄서 말리고 볶은 원료. 혼자서도 구수하지만, 곡물 원료 사이에서 단맛을 잇는 다리 역할을 할 때 가장 빛납니다.' },
    { key: 'sorghum', no: 'T-08', kr: '찰수수', en: 'Glutinous Sorghum', sci: 'Sorghum bicolor', ver: 'depth', a: 2, b: 3, f: 3, liq: '#CDA372',
      feat: '담백하고 순한 곡물의 구수함. 뿌리 원료를 받쳐 줍니다.',
      bio: '볶은 수수알. 향이 튀지 않아 깊이 있는 원료(민들레 뿌리·단팥)의 바닥을 받쳐 주는 데 씁니다. 비율을 늘려도 한 잔이 무거워지지 않습니다.' },
    { key: 'red_bean', no: 'T-09', kr: '단팥', en: 'Red Bean', sci: 'Vigna angularis', ver: 'depth', a: 3, b: 4, f: 4, liq: '#A65F4B',
      feat: '볶은 팥의 고소하고 부드러운 여운.',
      bio: '볶은 팥을 굵게 깨서 말렸습니다. 우리면 익숙한 단팥의 향이 올라와, 커피를 마시던 시간에 두는 한 잔의 중심이 됩니다. 교차 블렌드 「밀크티 무드」의 바탕입니다.' },
    { key: 'brown_rice', no: 'T-10', kr: '현미', en: 'Brown Rice', sci: 'Oryza sativa', ver: 'depth', a: 2, b: 3, f: 2, liq: '#D2A662',
      feat: '볶은 쌀의 담백하고 고소한 향. 바디를 받쳐 줍니다.',
      bio: '현미를 볶아 튀운 원료. 향보다 질감을 더하는 쪽이라, 어떤 곡물 블렌드에도 한 스푼을 더하면 입안이 둥글어집니다.' },
    { key: 'dandelion_root', no: 'T-11', kr: '민들레 뿌리', en: 'Dandelion Root', sci: 'Taraxacum officinale', ver: 'depth', a: 4, b: 5, f: 5, liq: '#6B4730',
      feat: '흙 · 나무 · 커피 · 카카오를 연상시키는 깊은 볶음 향. 중심 원료.',
      bio: '뿌리를 잘라 깊게 볶았습니다. 열두 원료 중 가장 깊고 진해, 비율 하나로 한 잔의 무게를 정합니다. 커피 대신 찾는 분이라면 여기서 시작하세요.' },
    { key: 'barley', no: 'T-12', kr: '보리', en: 'Barley', sci: 'Hordeum vulgare', ver: 'depth', a: 3, b: 3, f: 3, liq: '#AE7843',
      feat: '익숙하고 선명한 볶은 곡물 향.',
      bio: '누구에게나 익숙한 볶은 보리. 그 익숙함 덕에 새로운 원료를 더해도 낯설지 않게 받아 줍니다. Depth 블렌딩의 출발점으로 가장 안전한 원료입니다.' },
  ];
  const KITS = [
    { id: 'ver1', name: 'VER.1 Taste', sub: '티 블렌딩 키트', price: '59,000원', img: '../wadiz/assets/3d/flatlay/flatlay_taste.jpg', tags: [['t', 'Taste'], ['p', '인기'], ['g', '카페인 없음']], ver: 'taste', kind: 'kit',
      desc: '레몬밤 · 히비스커스 · 페퍼민트 · 유자 · 장미 · 캐모마일. 향과 색으로 즐기는 허브 블렌딩.' },
    { id: 'ver2', name: 'VER.2 Depth', sub: '티 블렌딩 키트', price: '59,000원', img: '../wadiz/assets/3d/flatlay/flatlay_depth.jpg', tags: [['d', 'Depth'], ['g', '카페인 없음']], ver: 'depth', kind: 'kit',
      desc: '둥굴레 · 찰수수 · 단팥 · 현미 · 민들레 뿌리 · 보리. 커피처럼 즐기는 곡물 블렌딩.' },
    { id: 'set', name: 'Taste + Depth', sub: '2개 세트', price: '110,000원', was: '118,000원', img: '../wadiz/assets/gen/package_gift.png', tags: [['t', 'Taste'], ['d', 'Depth'], ['p', '선물']], ver: 'both', kind: 'kit',
      desc: '키트 2개 · 노트 2권 · 인퓨저 2개 · 단팥차 샘플. 허브와 곡물을 섞는 교차 블렌드까지.' },
  ];
  window.RTT = { ING, KITS, SHOP, watch };

  /* ── 상품 그리드 + 필터 ── */
  const grid = document.getElementById('pgrid');
  if (grid) {
    const flavor = { lemon_balm: ['시트러스', '꽃향'], hibiscus: ['산미', '꽃향'], peppermint: ['맑음'], yuza: ['시트러스'], rose: ['꽃향'], chamomile: ['꽃향', '단맛'],
      solomons_seal: ['뿌리', '단맛'], sorghum: ['곡물'], red_bean: ['곡물', '단맛'], brown_rice: ['곡물'], dandelion_root: ['뿌리', '깊이'], barley: ['곡물'] };
    const cards = KITS.map(k => ({ ...k, flav: ['키트'] })).concat(ING.map(i => ({
      id: i.key, name: i.kr, sub: i.en, price: '', soon: '낱개 · 오픈 예정', img: `../wadiz/assets/real/herb_${i.key}.png`, pad: true, ver: i.ver, kind: 'single',
      tags: [[i.ver === 'taste' ? 't' : 'd', i.ver === 'taste' ? 'Taste' : 'Depth'], ...flavor[i.key].map(f => ['', f])], flav: flavor[i.key], desc: i.feat })));
    grid.innerHTML = cards.map(c => `
      <article class="card rv" data-id="${c.id}" data-ver="${c.ver}" data-kind="${c.kind}" data-flav="${c.flav.join(' ')}">
        <a href="${c.kind === 'kit' ? SHOP : 'guide.html#' + c.id}">
          <div class="ph"><img class="${c.pad ? 'pad' : ''}" src="${c.img}" alt="${c.name}" loading="lazy"><svg class="hrt" viewBox="0 0 24 24" fill="none" stroke="#333" stroke-width="1.4"><path d="M12 21s-7-4.6-9.3-9A5 5 0 0 1 12 6a5 5 0 0 1 9.3 6c-2.3 4.4-9.3 9-9.3 9z"/></svg></div>
          <h3>${c.name}<small class="small" style="display:block;letter-spacing:.14em;margin-top:2px">${c.sub}</small></h3>
          <div class="tags">${c.tags.map(t => `<span class="tag ${t[0]}">${t[1]}</span>`).join('')}</div>
          <div class="pr">${c.price ? c.price + (c.was ? `<s>${c.was}</s>` : '') : `<span class="soon">${c.soon}</span>`}</div>
          <p>${c.desc}</p>
        </a>
      </article>`).join('');
    const state = { ver: '', flav: '' };
    const apply = () => grid.querySelectorAll('.card').forEach(c => {
      const okV = !state.ver || c.dataset.ver === state.ver || c.dataset.ver === 'both';
      const okF = !state.flav || c.dataset.flav.split(' ').includes(state.flav);
      c.classList.toggle('hide', !(okV && okF)); });
    document.querySelectorAll('.chip[data-ver]').forEach(ch => ch.addEventListener('click', () => { state.ver = state.ver === ch.dataset.ver ? '' : ch.dataset.ver; document.querySelectorAll('.chip[data-ver]').forEach(x => x.classList.toggle('on', x.dataset.ver === state.ver)); apply(); }));
    document.querySelectorAll('.chip[data-flav]').forEach(ch => ch.addEventListener('click', () => { state.flav = state.flav === ch.dataset.flav ? '' : ch.dataset.flav; document.querySelectorAll('.chip[data-flav]').forEach(x => x.classList.toggle('on', x.dataset.flav === state.flav)); apply(); }));
    const reset = document.getElementById('preset'); if (reset) reset.addEventListener('click', e => { e.preventDefault(); state.ver = state.flav = ''; document.querySelectorAll('.chip').forEach(x => x.classList.remove('on')); apply(); });
    // 취향 테스트 결과로 넘어온 경우: 추천 키트를 표시하고 그 자리로
    const pick = new URLSearchParams(location.search).get('pick');
    if (pick) { const c = grid.querySelector(`.card[data-id="${pick}"]`);
      if (c) { c.classList.add('pick', 'on'); c.id = 'pick'; setTimeout(() => c.scrollIntoView({ behavior: 'smooth', block: 'center' }), 400); } }
  }

  /* ── 원료 가이드: 목록 + 항목(라디얼 3축: 향·바디·여운) ── */
  const gl = document.getElementById('glist'), gi = document.getElementById('gitems');
  if (gl && gi) {
    gl.innerHTML = ING.map(i => `<a href="#${i.key}"><span class="cup"><img src="../wadiz/assets/real/herb_${i.key}.png" alt="${i.kr}" loading="lazy"></span><span>${i.no}</span></a>`).join('');   // 10/24: 찻물 색 원 → 3차수정 실사 누끼(herb_*.png)
    const radar = (a, b, f) => { const R = 70, cx = 100, cy = 104, ax = ['향', '바디', '여운'], v = [a, b, f];
      const pt = (k, r) => { const t = -Math.PI / 2 + k * 2 * Math.PI / 3; return [cx + r * Math.cos(t), cy + r * Math.sin(t)]; };
      const ring = r => [0, 1, 2].map(k => pt(k, r).join(',')).join(' ');
      const poly = [0, 1, 2].map(k => pt(k, R * v[k] / 5).join(',')).join(' ');
      return `<svg class="radar" viewBox="0 0 200 200">${[1, 2, 3, 4, 5].map(s => `<polygon points="${ring(R * s / 5)}" fill="none" stroke="#e3e0d8" stroke-width="1"/>`).join('')}
        ${[0, 1, 2].map(k => `<line x1="${cx}" y1="${cy}" x2="${pt(k, R)[0]}" y2="${pt(k, R)[1]}" stroke="#e3e0d8"/>`).join('')}
        <polygon points="${poly}" fill="${'#E8E6BF'}" fill-opacity=".85" stroke="#9FA86A" stroke-width="1.2"/>
        ${[0, 1, 2].map(k => { const [x, y] = pt(k, R + 18); return `<text x="${x}" y="${y + 3}" text-anchor="middle">${ax[k]} ${v[k]}</text>`; }).join('')}</svg>`; };
    gi.innerHTML = ING.map((i, n) => `
      <section class="gitem" id="${i.key}">
        <div class="no rv">${i.no}</div>
        <div class="cols">
          <div class="meta rv">
            <div class="nm">${i.kr}</div>
            <div class="sci">${i.en} · ${i.sci}</div>
            <div class="ver">${i.ver === 'taste' ? 'VER.1 TASTE' : 'VER.2 DEPTH'} · 향 바디 여운 5점 기준</div>
            <a class="btnbox sm" href="products.html">이 원료가 든 키트<br><small class="small">${i.ver === 'taste' ? 'VER.1 Taste' : 'VER.2 Depth'}</small></a>
          </div>
          <div class="vis rv">
            ${radar(i.a, i.b, i.f)}
            <img class="herb" src="../wadiz/assets/real/herb_${i.key}.png" alt="${i.kr}" loading="lazy">
          </div>
          <div class="txt rv">
            <div><h4>Feature · 향 노트</h4><p>${i.feat}</p></div>
            <div><h4>Biography · 원료 이야기</h4><p>${i.bio}</p></div>
          </div>
        </div>
      </section>`).join('');
  }

  /* ── 시작 ── */
  watch();
  setTimeout(() => document.body.classList.add('ready'), 40);   // rAF 는 숨은 탭에서 멈추므로 타이머로
  if (location.hash) setTimeout(() => { const t = document.querySelector(location.hash); if (t) t.scrollIntoView(); }, 300);
})();
