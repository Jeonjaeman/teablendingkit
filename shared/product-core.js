/* 취향의 권리 · 상품 상세 공용 로직 (카페24 product/detail.html 흐름)
   사용: ProductPage.mount({ img:{ver1:{imgs:[],photos:[]},...}, card:id=>url, cardAlt:id=>url(선택), back:'index.html#kit', wish:['♡','♥'] })
   각 페이지는 같은 id 훅을 가진 마크업을 자기 문법(CSS)으로 구성한다. 없는 훅은 건너뛴다. */
(function (global) {
  const $ = (s) => document.querySelector(s), $$ = (s) => [...document.querySelectorAll(s)];
  const fmt = (n) => n.toLocaleString('ko-KR');
  const set = (sel, html, prop) => { const el = $(sel); if (el) el[prop || 'innerHTML'] = html; return el; };

  function mount(cfg) {
    const { PRODUCTS, OPTIONS, PACK, PACK_HL } = global.PRODUCT_DATA;
    const q = new URLSearchParams(location.search);
    const key = PRODUCTS[q.get('p')] ? q.get('p') : 'ver1';
    const P = PRODUCTS[key], IM = cfg.img[key];
    const wish = cfg.wish || ['♡', '♥'];

    /* ── 돌아가기: 시안에서 들어왔으면 그 페이지로 ── */
    try { const r = new URL(document.referrer); if (r.origin === location.origin && /\/design\d\//.test(r.pathname)) { const b = $('#backLink'); if (b) b.href = r.pathname + (r.hash || ''); } } catch (e) { /* no referrer */ }

    /* ── 렌더 ── */
    document.title = `${P.no} ${P.name} — ${cfg.titleSuffix || '취향의 권리'}`;
    $$('[data-cat]').forEach((a) => a.classList.toggle('on', a.dataset.cat === key));
    set('#pathCur', `${P.no} ${P.name}`, 'textContent');
    const key0 = $('#keyImg'); if (key0) { key0.src = IM.imgs[0]; key0.alt = `${P.no} ${P.name}`; }
    set('#keyTag', P.tag, 'textContent');
    set('#keyNo', 'Fig. 01', 'textContent');
    set('#addImg', IM.imgs.map((s, i) => `<button type="button" class="${i ? '' : 'on'}" data-i="${i}" aria-label="상세컷 ${i + 1}"><img src="${s}" alt=""></button>`).join(''));
    set('#pNo', P.no, 'textContent'); set('#pName', `${P.name}<small>${P.en}</small>`); set('#pSummary', P.summary, 'textContent');
    set('#tName', `${P.no} ${P.name}`, 'textContent'); set('#tPrice', fmt(P.price), 'textContent'); set('#tPoint', `${fmt(Math.round(P.price * .01))}원 (1%)`, 'textContent');
    set('#tPack', P.pack, 'textContent'); set('#tCode', P.code, 'textContent');
    set('#dEyebrow', P.eyebrow, 'textContent'); set('#dHead', P.head); set('#dLead', P.lead, 'textContent');
    set('#dPhotos', IM.photos.map((s) => `<img src="${s}" alt="">`).join(''));
    set('#ing', P.ing.map(([id, kr, en, t]) => `<figure><div class="cimg">${cfg.cardAlt ? `<img class="a" src="${cfg.card(id)}" alt="${en} 보태니컬 카드"><img class="b" src="${cfg.cardAlt(id)}" alt="">` : `<img src="${cfg.card(id)}" alt="${en} 보태니컬 카드">`}</div><figcaption><b>${kr}</b><i>${en}</i><span>${t}</span></figcaption></figure>`).join(''));
    set('#ingNote', P.ingNote, 'textContent');
    set('#dValue', P.value.map((v) => `<li>${v}</li>`).join('')); set('#dFor', P.for_.map((v) => `<li>${v}</li>`).join(''));
    const rt = $('#recipeTitle'); if (rt) rt.innerHTML = `${P.recipeTitle} <small>시음 후 최종 확정</small>`;
    set('#recipes', P.recipes.map(([n, r, t], i) => `<div class="rc"><dt><em>${String(i + 1).padStart(2, '0')}</em>${n}<span>${r}</span></dt><dd>${t}</dd></div>`).join(''));
    set('#pack', PACK.map((n, i) => `<li class="${PACK_HL.includes(i) ? 'hl' : ''}"><b>${String(i + 1).padStart(2, '0')}</b>${n}</li>`).join(''));
    set('#packNote', P.packNote, 'textContent');
    set('#sName', `취향의 권리 ${P.no} ${P.name}`, 'textContent'); set('#sWeight', P.weight); set('#sIng', P.sIng);
    set('#rel', Object.keys(PRODUCTS).filter((k) => k !== key).map((k) => { const r = PRODUCTS[k], im = cfg.img[k]; return `<a href="?p=${k}"><div class="th"><img src="${im.imgs[0]}" alt=""></div><div class="b"><div class="no">${r.no}</div><strong>${r.name}</strong><p>${r.summary}</p><div class="pr">${fmt(r.price)}원<small>예시가</small></div></div></a>`; }).join(''));

    /* ── 썸네일 전환 ── */
    const add = $('#addImg'); if (add) add.addEventListener('click', (e) => { const b = e.target.closest('button'); if (!b) return; $$('#addImg button').forEach((x) => x.classList.remove('on')); b.classList.add('on'); const im = $('#keyImg'); im.style.opacity = 0; setTimeout(() => { im.src = IM.imgs[+b.dataset.i]; im.style.opacity = 1; }, 180); set('#keyNo', `Fig. ${String(+b.dataset.i + 1).padStart(2, '0')}`, 'textContent'); });

    /* ── 옵션 → 선택 상품 목록 → 총 상품금액 ── */
    const picked = {}; const MAX = 10;
    function renderPicked() {
      const box = $('#picked'); if (!box) return; const keys = Object.keys(picked);
      box.innerHTML = keys.length ? keys.map((k) => `<div class="row" data-k="${k}"><div class="nm">${P.no} ${P.name}<small>${OPTIONS[k].short}${OPTIONS[k].add ? ` (+${fmt(OPTIONS[k].add)}원)` : ''}</small></div><div class="qty"><button type="button" data-d="-1" aria-label="수량감소">−</button><input type="text" value="${picked[k]}" inputmode="numeric" aria-label="수량"><button type="button" data-d="1" aria-label="수량증가">+</button></div><div class="pr">${fmt((P.price + OPTIONS[k].add) * picked[k])}원</div><button type="button" class="del" aria-label="삭제">×</button></div>`).join('')
        : '<div class="empty">위 옵션선택 박스를 선택하시면 아래에 상품이 추가됩니다.</div>';
      let sum = 0, n = 0; keys.forEach((k) => { sum += (P.price + OPTIONS[k].add) * picked[k]; n += picked[k]; });
      set('#sum', fmt(sum), 'textContent'); set('#sumN', n, 'textContent');
    }
    const sel = $('#optSel'); if (sel) {
      sel.innerHTML = `<option value="">- [필수] 옵션을 선택해 주세요 -</option>` + Object.keys(OPTIONS).map((k) => `<option value="${k}">${OPTIONS[k].n}</option>`).join('');
      sel.addEventListener('change', (e) => { const v = e.target.value; if (!v) return; picked[v] = (picked[v] || 0) + 1; if (picked[v] > MAX) { picked[v] = MAX; toast(`최대주문수량은 ${MAX}개 이하입니다.`); } e.target.value = ''; renderPicked(); });
    }
    const pk = $('#picked'); if (pk) {
      pk.addEventListener('click', (e) => { const row = e.target.closest('.row'); if (!row) return; const k = row.dataset.k;
        if (e.target.closest('.del')) { delete picked[k]; renderPicked(); return; }
        const b = e.target.closest('[data-d]'); if (b) { picked[k] = Math.min(MAX, Math.max(1, picked[k] + +b.dataset.d)); renderPicked(); } });
      pk.addEventListener('change', (e) => { const row = e.target.closest('.row'); if (!row || e.target.tagName !== 'INPUT') return; const v = parseInt(e.target.value, 10); picked[row.dataset.k] = isNaN(v) ? 1 : Math.min(MAX, Math.max(1, v)); renderPicked(); });
    }

    /* ── 액션 (데모: 카페24 연동 전) ── */
    let cartN = 0;
    const needOpt = () => { if (!Object.keys(picked).length) { toast('옵션을 선택해 주세요.'); if (sel) sel.focus(); return true; } return false; };
    const buy = () => { if (needOpt()) return; toast('데모 페이지입니다 — 카페24 연동 후 주문서 작성 화면으로 이동합니다.'); };
    const cart = () => { if (needOpt()) return; cartN += Object.values(picked).reduce((a, b) => a + b, 0); set('#cartN', cartN, 'textContent'); toast('장바구니에 담았습니다. (데모)'); };
    const bb = $('#btnBuy'); if (bb) bb.addEventListener('click', buy);
    const bc = $('#btnCart'); if (bc) bc.addEventListener('click', cart);
    $$('.m-actions button').forEach((b) => b.addEventListener('click', () => (b.dataset.act === 'buy' ? buy() : cart())));
    const bw = $('#btnWish'); if (bw) bw.addEventListener('click', () => { bw.classList.toggle('on'); const on = bw.classList.contains('on'); bw.textContent = on ? wish[1] : wish[0]; toast(on ? '관심상품에 등록했습니다. (데모)' : '관심상품에서 삭제했습니다.'); });
    const cl = $('#copyLink'); if (cl) cl.addEventListener('click', () => { (navigator.clipboard ? navigator.clipboard.writeText(location.href) : Promise.reject()).then(() => toast('상품 링크를 복사했습니다.')).catch(() => toast(location.href)); });
    $$('[data-demo]').forEach((el) => el.addEventListener('click', (e) => { e.preventDefault(); toast('데모 페이지입니다 — 카페24 연동 후 동작합니다.'); }));
    let tt; function toast(m) { const t = $('#toast'); if (!t) return; t.textContent = m; t.classList.add('on'); clearTimeout(tt); tt = setTimeout(() => t.classList.remove('on'), 2400); }

    /* ── 탭 스크롤스파이 ── */
    const tabLinks = $$('#tabs a[href^="#"]'); const panels = tabLinks.map((a) => $(a.getAttribute('href')));
    if (tabLinks.length) addEventListener('scroll', () => { let cur = 0; panels.forEach((p, i) => { if (p && p.getBoundingClientRect().top - (cfg.spyOffset || 80) <= 0) cur = i; }); tabLinks.forEach((a, i) => a.classList.toggle('on', i === cur)); }, { passive: true });

    return { key, P, toast };
  }
  global.ProductPage = { mount };
})(window);
