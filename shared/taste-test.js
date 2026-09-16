/* ═══════════════════════════════════════════════════════════════
   취향의 권리 · 티 블렌딩 취향 테스트  (design6 · design7 공용)
   근거: data/20260916.txt §7~§11, §15  — 8문항 · 결과 4유형 · 기본 레시피 1 + 교차 레시피 1
   사용: TasteTest.mount(containerEl, { onKit(kitId), onRetry() })
   ═══════════════════════════════════════════════════════════════ */
(function (global) {
  const QUESTIONS = [
    { q: '가장 먼저 느끼고 싶은 향은 무엇인가요?', a: ['장미와 카모마일 같은 화사한 꽃향', '유자와 레몬밤 같은 밝은 과일·허브 향', '볶은 곡물과 뿌리 원료의 깊은 향', '깊은 로스트 위에 피어나는 과일·꽃·허브 향'] },
    { q: '평소 가장 자주 찾는 음료는 무엇인가요?', a: ['부드러운 꽃차', '과일차나 아이스티', '진한 커피나 구수한 곡물차', '향미가 풍부한 스페셜티 커피나 독특한 블렌드'] },
    { q: '가장 좋아하는 맛의 방향은 무엇인가요?', a: ['부드럽고 은은하게', '산뜻하고 선명하게', '구수하고 쌉싸름하게', '향은 화사하지만 맛은 깊고 묵직하게'] },
    { q: '원하는 한 잔의 무게감은?', a: ['가볍고 섬세하게', '맑고 상쾌하게', '진하고 묵직하게', '첫 향은 가볍지만 여운은 깊게'] },
    { q: '커피를 마시는 시간에 어떤 한 잔을 원하나요?', a: ['부드러운 꽃향의 차', '상쾌한 과일·허브차', '곡물과 뿌리로 만든 깊은 로스트', '커피 같은 깊이에 과일·꽃·허브 향을 더한 블렌드'] },
    { q: '가장 만들어보고 싶은 조합은?', a: ['장미와 카모마일', '유자와 히비스커스', '민들레 뿌리와 단팥·통보리', '유자와 민들레 뿌리 또는 장미와 통보리'] },
    { q: '나의 블렌딩 성향은?', a: ['부드럽고 쉬운 조합부터 시작하고 싶다', '좋아하는 향을 중심으로 조금씩 바꾸고 싶다', '진한 맛과 로스트 강도를 직접 조절하고 싶다', '서로 다른 원료를 연결해 새로운 맛을 만들고 싶다'] },
    { q: '원하는 마지막 여운은?', a: ['꽃향이 은은하게 남는 여운', '과일과 허브 향이 맑게 남는 여운', '볶은 곡물과 뿌리의 깊은 여운', '화사한 첫 향 뒤에 로스트가 길게 이어지는 여운'] }
  ];
  const RESULTS = {
    A: { key: 'A', name: '꽃이 머무는 정원', en: 'A Garden Where Flowers Stay', kit: 'ver1', kitName: 'VER.1 아로마 티 블렌딩',
      desc: '강하고 자극적인 맛보다 은은한 꽃향과 부드러운 여운을 좋아합니다.', ingredients: ['장미', '카모마일', '레몬밤'],
      copy: '당신에게 좋은 차는 강하게 기억되는 차보다 은은하게 오래 머무는 차입니다.',
      basic: { name: '가든 플로럴', ratio: '장미 2 : 카모마일 1 : 레몬밤 0.5', note: '꽃향을 중심에 두고 레몬밤으로 첫 향을 살짝 밝힙니다. ※ 시음 후 최종 확정' },
      cross: { name: '로즈 그레인', ratio: '장미 + 카모마일 + 통보리', note: '우아한 꽃향과 맑은 곡물의 여운이 만나는 플로럴 로스트 (TWO KIT SET)' } },
    B: { key: 'B', name: '햇살을 머금은 허브', en: 'Herbs Holding the Sunlight', kit: 'ver1', kitName: 'VER.1 아로마 티 블렌딩',
      desc: '유자와 허브의 밝은 향, 선명한 산미와 상쾌한 여운을 좋아합니다.', ingredients: ['유자', '히비스커스', '페퍼민트', '레몬밤'],
      copy: '당신의 취향은 한 모금만으로도 분위기를 바꾸는 밝고 선명한 향에 가깝습니다.',
      basic: { name: '선라이트 시트러스', ratio: '유자 2 : 히비스커스 1 : 레몬밤 1 : 페퍼민트 0.5', note: '아이스티로도 잘 어울립니다. 페퍼민트는 소량부터. ※ 시음 후 최종 확정' },
      cross: { name: '유자 로스트', ratio: '유자 + 민들레 뿌리 + 단팥', note: '유자의 밝은 첫 향 뒤에 깊은 볶음 향과 부드러운 고소함이 이어지는 시트러스 로스트 (TWO KIT SET)' } },
    C: { key: 'C', name: '깊은 뿌리의 로스트', en: 'Roast from the Deep Root', kit: 'ver2', kitName: 'VER.2 루트 앤드 그레인 로스트',
      desc: '볶은 향과 묵직한 바디감, 커피처럼 깊게 이어지는 여운을 좋아합니다.', ingredients: ['민들레 뿌리', '둥굴레', '단팥', '통보리'],
      copy: '커피의 분위기는 남기고, 곡물과 뿌리로 나만의 로스트를 만들어보세요.',
      basic: { name: '브라질리언 로스트', ratio: '민들레 뿌리 2 : 단팥 2 : 찰수수 1 : 둥굴레 0.5', note: '깊게 볶은 듯한 첫 향에 단팥과 찰수수의 부드러운 구수함이 이어집니다.' },
      cross: { name: '민트 로스트', ratio: '페퍼민트 + 레몬밤 + 통보리', note: '상쾌하게 시작해 구수하고 깔끔하게 끝나는 허벌 로스트 (TWO KIT SET)' } },
    D: { key: 'D', name: '향이 피어나는 로스트', en: 'Roast Where Aroma Blooms', kit: 'set', kitName: 'TWO KIT SET 프리미엄 아로마 로스트',
      desc: '과일·꽃·허브의 첫 향과 깊은 로스트의 여운을 한 잔에서 함께 느끼고 싶은 입체적인 취향입니다.', ingredients: ['유자', '장미', '페퍼민트', '민들레 뿌리', '단팥', '통보리', '둥굴레'],
      copy: '깊이는 로스트로 만들고, 취향은 향으로 완성하세요.',
      basic: { name: '딥 우드 로스트', ratio: '민들레 뿌리 2 : 둥굴레 2 : 단팥 1', note: '볶은 뿌리와 나무를 연상시키는 깊은 향, 둥굴레의 부드러운 바디감, 단팥의 고소한 마무리.' },
      cross: { name: '유자 로스트', ratio: '유자 + 민들레 뿌리 + 단팥', note: '같은 로스트도 유자를 더하면 밝게, 장미를 더하면 우아하게, 페퍼민트를 더하면 상쾌하게 달라집니다.' } }
  };
  const KIT_BTN = { ver1: '오늘의 향 만들기', ver2: '나만의 로스트 만들기', set: '12가지 원료로 향과 깊이 설계하기' };

  function score(answers) {
    const c = { A: 0, B: 0, C: 0, D: 0 }; answers.forEach(k => c[k]++);
    const max = Math.max(c.A, c.B, c.C, c.D); const tied = ['A', 'B', 'C', 'D'].filter(k => c[k] === max);
    if (tied.length === 1) return tied[0];
    if (tied.includes(answers[0])) return answers[0];           // 동점이면 "가장 먼저 느끼고 싶은 향"(1번) 우선
    return tied[tied.length - 1];
  }

  function mount(root, opts) {
    opts = opts || {}; let step = 0; const answers = [];
    root.classList.add('tt');
    function esc(s) { return String(s).replace(/[&<>"]/g, m => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[m])); }
    function renderIntro() {
      root.innerHTML = `<div class="tt-intro">
        <div class="tt-eyebrow">Taste Test — 오늘의 나에게 맞는 티 블렌딩 찾기</div>
        <h2 class="tt-h">나는 향을 좋아할까,<br>깊이를 좋아할까?</h2>
        <p class="tt-p">1분 만에 오늘의 블렌딩 취향을 확인해보세요. 8개의 질문으로 VER.1, VER.2 또는 TWO KIT SET과 추천 레시피를 연결합니다. 개인정보는 수집하지 않습니다.</p>
        <button class="tt-btn" data-act="start"><span>테스트 시작하기</span></button>
      </div>`;
    }
    function renderQ() {
      const Q = QUESTIONS[step];
      root.innerHTML = `<div class="tt-q">
        <div class="tt-prog"><span>${step + 1} / ${QUESTIONS.length}</span><i style="width:${((step) / QUESTIONS.length * 100).toFixed(1)}%"></i></div>
        <h2 class="tt-h">${esc(Q.q)}</h2>
        <ul class="tt-opts">${Q.a.map((t, i) => `<li><button class="tt-opt" data-k="${'ABCD'[i]}"><b>${'ABCD'[i]}</b><span>${esc(t)}</span></button></li>`).join('')}</ul>
        <div class="tt-nav">${step > 0 ? '<button class="tt-link" data-act="back">← 이전 질문</button>' : ''}</div>
      </div>`;
    }
    function renderResult(key) {
      const R = RESULTS[key];
      root.innerHTML = `<div class="tt-result tt-${key}">
        <div class="tt-eyebrow">Result — 유형 ${key}</div>
        <h2 class="tt-h">${esc(R.name)}<small>${esc(R.en)}</small></h2>
        <p class="tt-desc">${esc(R.desc)}</p>
        <blockquote class="tt-quote">${esc(R.copy)}</blockquote>
        <div class="tt-grid">
          <div class="tt-card"><div class="tt-lab">추천 제품</div><div class="tt-kit">${esc(R.kitName)}</div><div class="tt-ing">${R.ingredients.map(esc).join(' · ')}</div></div>
          <div class="tt-card"><div class="tt-lab">기본 레시피</div><div class="tt-rn">${esc(R.basic.name)}</div><div class="tt-ratio">${esc(R.basic.ratio)}</div><p>${esc(R.basic.note)}</p></div>
          <div class="tt-card"><div class="tt-lab">교차 레시피</div><div class="tt-rn">${esc(R.cross.name)}</div><div class="tt-ratio">${esc(R.cross.ratio)}</div><p>${esc(R.cross.note)}</p></div>
        </div>
        <p class="tt-note">추천 비율은 취향을 발견하기 위한 첫 번째 기준입니다. 한 번 맛본 뒤 마음에 드는 원료를 반 스푼씩 조절해보세요. 달라진 비율이 바로 당신의 레시피가 됩니다.</p>
        <div class="tt-actions">
          <button class="tt-btn" data-act="kit" data-kit="${R.kit}"><span>추천 키트 자세히 보기</span></button>
          <button class="tt-btn tt-ghost" data-act="retry"><span>다른 취향도 발견하기</span></button>
          <button class="tt-link" data-act="share">결과 공유하기</button><span class="tt-shared" hidden>링크가 복사되었습니다</span>
        </div>
      </div>`;
      if (opts.onResult) opts.onResult(R);
    }
    root.addEventListener('click', e => {
      const b = e.target.closest('button'); if (!b) return;
      const act = b.dataset.act;
      if (act === 'start') { step = 0; answers.length = 0; renderQ(); return; }
      if (b.classList.contains('tt-opt')) { answers[step] = b.dataset.k; step++; if (step >= QUESTIONS.length) renderResult(score(answers)); else renderQ(); return; }
      if (act === 'back') { step = Math.max(0, step - 1); renderQ(); return; }
      if (act === 'retry') { step = 0; answers.length = 0; renderQ(); if (opts.onRetry) opts.onRetry(); return; }
      if (act === 'kit') { if (opts.onKit) opts.onKit(b.dataset.kit); return; }
      if (act === 'share') { const key = root.querySelector('.tt-result').className.match(/tt-([ABCD])/)[1]; const u = new URL(location.href); u.searchParams.set('result', key);
        (navigator.clipboard ? navigator.clipboard.writeText(u.toString()) : Promise.reject()).catch(() => {}).finally(() => { const s = root.querySelector('.tt-shared'); if (s) { s.hidden = false; setTimeout(() => { s.hidden = true; }, 2400); } }); return; }
    });
    const q = new URLSearchParams(location.search); const r = q.get('result');
    if (r && RESULTS[r]) renderResult(r); else renderIntro();
    return { restart: renderIntro, showResult: renderResult, QUESTIONS, RESULTS, KIT_BTN };
  }
  global.TasteTest = { mount, QUESTIONS, RESULTS, KIT_BTN, score };
})(window);
