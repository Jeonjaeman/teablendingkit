/* 취향의 권리 — 공식 홈페이지(site2) 공통 스크립트 · v1.1 (2026-10-25 1차 수정 요청 반영)
   페이지마다 같은 틀(왼쪽 엠블럼 · 오른쪽 레일 · 메뉴 오버레이 · 브랜드 무비 · 빵부스러기 · 푸터)을 끼워 넣고,
   스크롤 등장(.rv), 포인트 내비, 키트 카드, 원료 목록·단품 상세, 레시피 목록, 교육 품목을 맡는다.
   원료·레시피·교육 품목 데이터는 catalog.js(먼저 읽힘). */
(function () {
  const PAGES = [
    ['index.html', '홈', 'Home'],
    ['ingredients.html', '원료', 'Ingredients'],
    ['products.html', '키트', 'Blending Kit'],
    ['education.html', '교육', 'Education'],
    ['partners.html', '강사', 'Partners'],
    ['about.html', '브랜드 이야기', 'About'],
    ['blends.html', '블렌딩', 'Blending'],
    ['shop.html', '구매 안내', 'Shop Information'],
    ['contact.html', '문의', 'Contact'],
    ['ingredient.html', '원료 상세', 'Ingredient'],
  ];
  const MAIN = PAGES.slice(1, 6), SUB = PAGES.slice(6, 9);   // 상단 메뉴: 원료 · 키트 · 교육 · 강사 · 브랜드 이야기 / 보조: 블렌딩 · 구매 안내 · 문의
  const SHOP = 'shop.html#order';                           // 구매는 site2 안에서. site/ 와는 서로 독립
  const here = location.pathname.split('/').pop() || 'index.html';
  const page = PAGES.find(p => p[0] === here) || PAGES[0];
  const EMBLEM = '../wadiz/assets/emblem.svg';
  const C = window.RTT_CATALOG || { ingredients: [], recipes: [], education: [], weights: [], tiers: [] };
  const ING = C.ingredients, RECIPES = C.recipes;
  const byKey = k => ING.find(i => i.key === k);
  const esc = s => String(s).replace(/[&<>"]/g, m => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[m]));
  const won = n => n == null ? '가격 미정' : n.toLocaleString('ko-KR') + '원';
  const STATUS = { soon: ['오픈 예정', 'soon'], open: ['판매 중', 'open'], soldout: ['품절', 'out'] };
  const verName = v => v === 'taste' ? 'VER.1 Taste' : v === 'depth' ? 'VER.2 Depth' : 'Taste + Depth';

  /* ── 공통 틀 ── */
  const chrome = document.createElement('div');
  chrome.innerHTML = `
  <a class="lg" href="index.html" aria-label="취향의 권리 홈"><img src="${EMBLEM}" alt=""></a>
  <div class="rail">
    <div class="top"><a class="rl-shop" href="${SHOP}">Shop</a></div>
    <button class="rl-menu" aria-label="메뉴 열기"><i></i><i></i><i></i></button>
    <a class="rl-top" href="#top">Page top</a>
  </div>
  <div id="quiz" aria-hidden="true"><div class="q-top"><a class="q-logo" href="index.html"><img src="img/logo.svg" alt="취향의 권리 · the right to taste"></a><button class="q-close" type="button">닫기 ✕</button></div><div id="quizMount"></div></div>
  <div id="menu" aria-hidden="true">
    <div class="m-top">
      <a class="m-logo" href="index.html"><img class="logo" src="img/logo-wide.png" alt="취향의 권리 · the right to taste"></a>
      <a class="m-shop" href="${SHOP}">Online Shop</a>
    </div>
    <div class="m-body">
      <ul class="m-list">${MAIN.map(p => `<li><a href="${p[0]}" class="${p[0] === here ? 'cur' : ''}">${p[1]}<small>${p[2]}</small></a></li>`).join('')}</ul>
      <ul class="m-sub">${SUB.map(p => `<li><a href="${p[0]}" class="${p[0] === here ? 'cur' : ''}">${p[1]}</a></li>`).join('')}</ul>
    </div>
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
  tail.innerHTML = `${here === 'index.html' ? '' : `<div class="bread"><div class="inner"><a href="index.html">Home</a><span id="crumb">${page[1]}</span></div></div>`}
  <footer class="ft">
    <img class="logo-sq" src="img/logo-sq.png" alt="취향의 권리 · the right to taste">
    <nav class="fnav">${MAIN.map(p => `<a href="${p[0]}">${p[1]}</a>`).join('')}</nav>
    <div class="ad">만든 곳 · 티아포테카 (Tea Apotheca)<br>문의 · 카카오 채널(연결 예정) / Instagram @right.totaste</div>
    <div class="sns"><a href="contact.html">Contact</a><a href="${SHOP}">Online Shop</a><a href="blends.html">Blending</a><a href="partners.html">For Teachers</a></div>
    <div class="copy">© 2026 THE RIGHT TO TASTE. ALL RIGHTS RESERVED.</div>
  </footer>`;
  document.body.append(tail);

  /* ── 메뉴 · 무비 ── */
  const menu = document.getElementById('menu'), movie = document.getElementById('movie'), vid = movie.querySelector('video');
  const openMenu = o => { menu.classList.toggle('open', o); menu.setAttribute('aria-hidden', !o); document.body.style.overflow = o ? 'hidden' : ''; };
  document.querySelector('.rl-menu').addEventListener('click', () => openMenu(true));
  menu.querySelector('.m-close').addEventListener('click', () => openMenu(false));
  menu.querySelector('.m-movie').addEventListener('click', () => { movie.classList.add('open'); vid.play().catch(() => {}); });
  movie.querySelector('.x').addEventListener('click', () => { movie.classList.remove('open'); vid.pause(); });
  movie.addEventListener('click', e => { if (e.target === movie) { movie.classList.remove('open'); vid.pause(); } });
  document.addEventListener('keydown', e => { if (e.key === 'Escape') { openMenu(false); movie.classList.remove('open'); vid.pause(); } });
  document.querySelectorAll('[data-menu]').forEach(b => b.addEventListener('click', () => openMenu(true)));

  /* ── 취향 테스트 오버레이: 키트 페이지의 보조 도구(10/25). 모듈(quiz.js)은 처음 열 때 불러온다 ── */
  const quiz = document.getElementById('quiz'), qm = document.getElementById('quizMount');
  let quizReady = null;
  const loadQuiz = () => quizReady || (quizReady = new Promise(res => {
    const s = document.createElement('script'); s.src = 'quiz.js'; s.onload = () => { RTTQuiz.mount(qm, { onKit(kit) { location.href = `products.html?pick=${kit}#pick`; } }); res(); };
    document.head.appendChild(s); }));
  const openQuiz = async o => { if (o) { await loadQuiz(); openMenu(false); } quiz.classList.toggle('open', o); quiz.setAttribute('aria-hidden', !o);
    document.body.style.overflow = o ? 'hidden' : ''; if (o) quiz.scrollTo({ top: 0 }); };
  document.addEventListener('click', e => { const b = e.target.closest('[data-quiz]'); if (b) { e.preventDefault(); openQuiz(true); } });
  quiz.querySelector('.q-close').addEventListener('click', () => openQuiz(false));
  document.addEventListener('keydown', e => { if (e.key === 'Escape') openQuiz(false); });
  { const sp = new URLSearchParams(location.search); if (location.hash === '#quiz' || sp.has('quiz') || sp.has('result')) setTimeout(() => openQuiz(true), 300); }

  /* ── 등장 · Page top ── */
  const io = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) { e.target.classList.add('on'); io.unobserve(e.target); } }), { rootMargin: '0px 0px -8% 0px', threshold: .08 });
  const watch = () => document.querySelectorAll('.rv:not(.on)').forEach(el => io.observe(el));
  addEventListener('scroll', () => document.body.classList.toggle('scrolled', scrollY > 300), { passive: true });
  document.querySelector('.rl-top').addEventListener('click', e => { e.preventDefault(); scrollTo({ top: 0, behavior: 'smooth' }); });

  /* ── 포인트 내비 (브랜드 이야기) ── */
  const pnav = document.querySelector('.pnav');
  if (pnav) { const items = [...pnav.querySelectorAll('li')], secs = items.map(li => document.getElementById(li.dataset.t));
    const pio = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) { const i = secs.indexOf(e.target); items.forEach((li, k) => li.classList.toggle('on', k === i)); } }), { rootMargin: '-40% 0px -50% 0px' });
    secs.forEach(s => s && pio.observe(s)); items.forEach((li, i) => li.addEventListener('click', () => secs[i].scrollIntoView({ behavior: 'smooth', block: 'start' }))); }

  /* ── 키트 3종 ── */
  const KITS = [
    { id: 'ver1', name: 'VER.1 Taste', sub: '티 블렌딩 키트', price: '59,000원', img: '../wadiz/assets/3d/flatlay/flatlay_taste.jpg', tags: [['t', 'Taste'], ['p', '인기'], ['g', '카페인 없음']], ver: 'taste',
      desc: '레몬밤 · 히비스커스 · 페퍼민트 · 유자 · 장미 · 캐모마일. 향과 색으로 즐기는 허브 블렌딩.' },
    { id: 'ver2', name: 'VER.2 Depth', sub: '티 블렌딩 키트', price: '59,000원', img: '../wadiz/assets/3d/flatlay/flatlay_depth.jpg', tags: [['d', 'Depth'], ['g', '카페인 없음']], ver: 'depth',
      desc: '둥굴레 · 찰수수 · 단팥 · 현미 · 민들레 뿌리 · 보리. 커피처럼 즐기는 곡물 블렌딩.' },
    { id: 'set', name: 'Taste + Depth', sub: '2개 세트', price: '110,000원', was: '118,000원', img: '../wadiz/assets/gen/package_gift.png', tags: [['t', 'Taste'], ['d', 'Depth'], ['p', '선물']], ver: 'both',
      desc: '키트 2개 · 노트 2권 · 인퓨저 2개 · 단팥차 샘플. 허브와 곡물을 섞는 교차 블렌드까지.' },
  ];
  window.RTT = { ING, KITS, RECIPES, SHOP, watch };

  const kitGrid = document.getElementById('pgrid');
  if (kitGrid) {
    kitGrid.innerHTML = KITS.map(c => `
      <article class="card rv" data-id="${c.id}" data-ver="${c.ver}">
        <a href="${SHOP}">
          <div class="ph"><img src="${c.img}" alt="${c.name}" loading="lazy"></div>
          <h3>${c.name}<small class="small" style="display:block;letter-spacing:.14em;margin-top:2px">${c.sub}</small></h3>
          <div class="tags">${c.tags.map(t => `<span class="tag ${t[0]}">${t[1]}</span>`).join('')}</div>
          <div class="pr">${c.price}${c.was ? `<s>${c.was}</s>` : ''}</div>
          <p>${c.desc}</p>
        </a>
      </article>`).join('');
    const pick = new URLSearchParams(location.search).get('pick');   // 취향 테스트 결과로 넘어온 경우
    if (pick) { const c = kitGrid.querySelector(`.card[data-id="${pick}"]`);
      if (c) { c.classList.add('pick', 'on'); c.id = 'pick'; setTimeout(() => c.scrollIntoView({ behavior: 'smooth', block: 'center' }), 400); } }
  }

  /* ── 원료 목록 (ingredients.html): 단품 12종 + 상태 + 중량 옵션 ── */
  const igrid = document.getElementById('igrid');
  if (igrid) {
    const minPrice = i => { const v = Object.values(i.price).filter(x => x != null); return v.length ? `${won(Math.min(...v))}부터` : '가격 미정 · 오픈 전 확정'; };
    igrid.innerHTML = ING.map(i => { const [sl, sc] = STATUS[i.status] || STATUS.soon; return `
      <article class="card icard rv" data-id="${i.key}" data-ver="${i.ver}" data-status="${i.status}">
        <a href="ingredient.html?id=${i.key}">
          <div class="ph"><img class="pad" src="../wadiz/assets/real/herb_${i.key}.png" alt="${i.kr}" loading="lazy"><span class="st ${sc}">${sl}</span></div>
          <div class="no">${i.no}</div>
          <h3>${i.kr}<small class="small" style="display:block;letter-spacing:.14em;margin-top:2px">${i.en}</small></h3>
          <div class="tags"><span class="tag ${i.ver === 'taste' ? 't' : 'd'}">${verName(i.ver)}</span><span class="tag">${C.weights.map(w => w >= 1000 ? w / 1000 + 'kg' : w + 'g').join(' · ')}</span></div>
          <div class="pr">${minPrice(i)}</div>
          <p>${i.feat}</p>
        </a>
        ${i.status === 'soon' ? `<button class="notify" type="button" data-notify="${i.key}">입고 알림 신청</button>` : ''}
      </article>`; }).join('');
    const state = { ver: '', status: '' };
    const apply = () => igrid.querySelectorAll('.card').forEach(c => c.classList.toggle('hide', !((!state.ver || c.dataset.ver === state.ver) && (!state.status || c.dataset.status === state.status))));
    document.querySelectorAll('.chip[data-ver]').forEach(ch => ch.addEventListener('click', () => { state.ver = state.ver === ch.dataset.ver ? '' : ch.dataset.ver; document.querySelectorAll('.chip[data-ver]').forEach(x => x.classList.toggle('on', x.dataset.ver === state.ver)); apply(); }));
    document.querySelectorAll('.chip[data-status]').forEach(ch => ch.addEventListener('click', () => { state.status = state.status === ch.dataset.status ? '' : ch.dataset.status; document.querySelectorAll('.chip[data-status]').forEach(x => x.classList.toggle('on', x.dataset.status === state.status)); apply(); }));
    const reset = document.getElementById('preset'); if (reset) reset.addEventListener('click', e => { e.preventDefault(); state.ver = state.status = ''; document.querySelectorAll('.chip').forEach(x => x.classList.remove('on')); apply(); });
  }

  /* ── 입고 알림 신청: 접수 서버가 없어 이 브라우저에 기억하고 메일 신청으로 잇는다(쇼핑몰 연동 때 교체) ── */
  document.addEventListener('click', e => {
    const b = e.target.closest('[data-notify]'); if (!b) return; e.preventDefault();
    const key = b.dataset.notify, ing = byKey(key); if (!ing) return;
    let box = b.nextElementSibling; if (box && box.classList.contains('nbox')) { box.remove(); return; }
    box = document.createElement('form'); box.className = 'nbox'; box.innerHTML = `<input type="email" placeholder="이메일 주소" required autocomplete="email"><button class="btnbox sm" type="submit">신청</button><span class="msg"></span>`;
    b.after(box);
    box.addEventListener('submit', ev => { ev.preventDefault(); const em = box.querySelector('input').value.trim(); if (!em) return;
      try { const l = JSON.parse(localStorage.getItem('rtt_notify') || '[]'); l.push({ key, em, t: Date.now() }); localStorage.setItem('rtt_notify', JSON.stringify(l)); } catch (_) {}
      box.querySelector('.msg').innerHTML = `신청되었습니다. 오픈 시 안내드립니다. <a href="mailto:hello@example.com?subject=${encodeURIComponent('[취향의 권리] ' + ing.kr + ' 입고 알림 신청')}&body=${encodeURIComponent('이메일: ' + em)}">메일로도 남기기</a>`;
      box.querySelector('input').disabled = box.querySelector('button').disabled = true; });
  });

  /* ── 원료 단품 상세 (ingredient.html?id=): 사진 · 향·맛 한두 줄 · 우리는 온도·시간 · 중량별 가격(등급가) · 추천 블렌드 ── */
  const idet = document.getElementById('idetail');
  if (idet) {
    const id = new URLSearchParams(location.search).get('id'), i = byKey(id) || ING[0], n = ING.indexOf(i), prev = ING[(n + ING.length - 1) % ING.length], next = ING[(n + 1) % ING.length];
    const [sl, sc] = STATUS[i.status] || STATUS.soon;
    document.title = `${i.kr}｜원료｜취향의 권리`; const cr = document.getElementById('crumb'); if (cr) cr.innerHTML = `<a href="ingredients.html">원료</a><span style="margin-left:14px">${i.kr}</span>`;
    const radar = (a, b, f) => { const R = 70, cx = 100, cy = 104, ax = ['향', '바디', '여운'], v = [a, b, f];
      const pt = (k, r) => { const t = -Math.PI / 2 + k * 2 * Math.PI / 3; return [cx + r * Math.cos(t), cy + r * Math.sin(t)]; };
      const ring = r => [0, 1, 2].map(k => pt(k, r).join(',')).join(' ');
      const poly = [0, 1, 2].map(k => pt(k, R * v[k] / 5).join(',')).join(' ');
      return `<svg class="radar" viewBox="0 0 200 200">${[1, 2, 3, 4, 5].map(s => `<polygon points="${ring(R * s / 5)}" fill="none" stroke="#e3e0d8" stroke-width="1"/>`).join('')}
        ${[0, 1, 2].map(k => `<line x1="${cx}" y1="${cy}" x2="${pt(k, R)[0]}" y2="${pt(k, R)[1]}" stroke="#e3e0d8"/>`).join('')}
        <polygon points="${poly}" fill="#E8E6BF" fill-opacity=".85" stroke="#9FA86A" stroke-width="1.2"/>
        ${[0, 1, 2].map(k => { const [x, y] = pt(k, R + 18); return `<text x="${x}" y="${y + 3}" text-anchor="middle">${ax[k]} ${v[k]}</text>`; }).join('')}</svg>`; };
    const tierId = (() => { try { return localStorage.getItem('rtt_tier') || 'guest'; } catch (_) { return 'guest'; } })();
    const rec = RECIPES.filter(r => r.items.some(it => it[0] === i.key));
    const wl = w => w >= 1000 ? w / 1000 + 'kg' : w + 'g';
    idet.innerHTML = `
      <div class="phead">
        <h1>${i.kr}<small>${i.en} · <i>${i.sci}</i></small></h1>
        <div class="intro"><p>${i.feat}</p><p class="small" style="margin-top:10px">${i.no} · ${verName(i.ver)} 키트의 원료</p></div>
      </div>
      <section class="blk idet" style="padding-top:10px">
        <div class="cols">
          <figure class="rv"><img class="herb" src="../wadiz/assets/real/herb_${i.key}.png" alt="${i.kr}"></figure>
          <div class="rv">${radar(i.a, i.b, i.f)}<div class="small" style="text-align:center;margin-top:-6px">향 · 바디 · 여운 (5점 기준)</div></div>
          <div class="buy rv">
            <div class="sthead"><span class="st ${sc}">${sl}</span><span class="small">${i.status === 'soon' ? '오픈 시 순서대로 열립니다' : ''}</span></div>
            <label class="tier">가격 보기 <select id="tier">${C.tiers.map(t => `<option value="${t.id}" ${t.id === tierId ? 'selected' : ''}>${t.name}</option>`).join('')}</select></label>
            <table class="wt"><thead><tr><th>중량</th><th>소비자가</th><th id="tierhead">선택 등급가</th><th></th></tr></thead><tbody>
              ${C.weights.map(w => `<tr data-w="${w}"><td>${wl(w)}</td><td class="base">${won(i.price[w])}</td><td class="tp"></td><td><button class="pick" type="button" ${i.status !== 'open' || i.price[w] == null ? 'disabled' : ''}>담기</button></td></tr>`).join('')}
            </tbody></table>
            <p class="small tnote">강사 회원(승인제)은 로그인 후 등급가가 자동 표시됩니다. 지금은 미리 보기이며, 결제·회원 기능은 쇼핑몰 연동 시 열립니다. <a href="partners.html">강사 파트너 안내 →</a></p>
            ${i.status === 'soon' ? `<button class="btnbox" type="button" data-notify="${i.key}">입고 알림 신청</button>` : i.status === 'soldout' ? `<button class="btnbox" type="button" data-notify="${i.key}">재입고 알림 신청</button>` : `<a class="btnbox" href="${SHOP}">주문하기</a>`}
          </div>
        </div>
        <div class="txt rv">
          <div><h4>Taste · 향과 맛</h4><p>${i.feat}</p></div>
          <div><h4>Brew · 우리는 온도 · 시간</h4><p>${i.brew}<br><span class="small">종이 스쿱 한 스푼 기준 · 빈 티백에 담아 우립니다</span></p></div>
          <div><h4>Story · 원료 이야기</h4><p>${i.bio}</p></div>
        </div>
        <div class="recs rv">
          <h4>이 원료가 들어가는 추천 블렌드</h4>
          <ul>${rec.map(r => `<li><a href="blends.html#r-${r.id}"><b>${r.name}</b><small>${r.ver}</small><span>${r.items.map(it => `${(byKey(it[0]) || {}).kr || it[0]} ${it[1]}`).join(' · ')}</span></a></li>`).join('') || '<li class="small">준비 중</li>'}</ul>
          <a class="btnbox sm" href="products.html#${i.ver === 'taste' ? 'ver1' : 'ver2'}">이 원료가 든 키트 · ${verName(i.ver)}</a>
        </div>
        <nav class="pn rv"><a href="ingredient.html?id=${prev.key}">← ${prev.no} ${prev.kr}</a><a href="ingredients.html">원료 전체</a><a href="ingredient.html?id=${next.key}">${next.no} ${next.kr} →</a></nav>
      </section>`;
    const sel = document.getElementById('tier');
    const paint = () => { const t = C.tiers.find(x => x.id === sel.value) || C.tiers[0]; document.getElementById('tierhead').textContent = t.off ? t.name : '강사 등급가';
      idet.querySelectorAll('tr[data-w]').forEach(tr => { const base = i.price[tr.dataset.w]; tr.querySelector('.tp').textContent = base == null ? '—' : t.off ? won(Math.round(base * (1 - t.off) / 100) * 100) : '—'; });
      try { localStorage.setItem('rtt_tier', t.id); } catch (_) {} };
    sel.addEventListener('change', paint); paint();
  }

  /* ── 레시피 목록 (blends.html #recipes) ── */
  const rl = document.getElementById('recipes');
  if (rl) rl.innerHTML = RECIPES.map(r => `
      <div class="recipe" id="r-${r.id}">
        <div class="rn"><small>${r.ver === '교차' ? 'VER.1 + VER.2 · 교차 블렌드' : r.ver + ' · 추천 레시피'}</small>${r.name}</div>
        <ul>${r.items.map(it => { const g = byKey(it[0]); return `<li><a href="ingredient.html?id=${it[0]}">${g ? g.kr : it[0]}</a><b>${it[1]}</b></li>`; }).join('')}</ul>
        <div class="brew">${r.brew.split(' · ').join('<br>')}</div>
        <div class="note">${r.note}</div>
      </div>`).join('');

  /* ── 교육 재료·자료 (education.html #egrid) ── */
  const eg = document.getElementById('egrid');
  if (eg) eg.innerHTML = C.education.map(e => { const [sl, sc] = STATUS[e.status] || STATUS.soon; return `
      <article class="card ecard2 rv">
        <div class="ph"><span class="st ${sc}">${sl}</span></div>
        <h3>${e.name}<small class="small" style="display:block;letter-spacing:.14em;margin-top:2px">${e.sub}</small></h3>
        <div class="pr">${e.price == null ? '가격 미정 · 품목 확정 후 안내' : won(e.price)}</div>
        <p>${e.desc}</p>
      </article>`; }).join('');

  /* ── 시작 ── */
  watch();
  setTimeout(() => document.body.classList.add('ready'), 40);   // rAF 는 숨은 탭에서 멈추므로 타이머로
  if (location.hash && location.hash !== '#quiz') setTimeout(() => { const t = document.querySelector(location.hash); if (t) t.scrollIntoView(); }, 300);
})();
