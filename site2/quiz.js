/* 취향의 권리 · site2 전용 취향 테스트 (site/ 와 독립 — 공용 모듈을 쓰지 않는다)
   사용: RTTQuiz.mount(rootEl, { onKit(kitId) })   kitId = ver1 | ver2 | set
   질문 8개, 답 A~D 를 세어 가장 많은 유형으로. 동점이면 1번 답(가장 먼저 느끼고 싶은 향) 우선. */
(function (global) {
  const QUESTIONS = [
    { q: '가장 먼저 느끼고 싶은 향은 무엇인가요?', a: ['장미와 캐모마일 같은 화사한 꽃향', '유자와 레몬밤 같은 밝은 과일·허브 향', '볶은 곡물과 뿌리 원료의 깊은 향', '깊은 로스트 위에 피어나는 과일·꽃·허브 향'] },
    { q: '평소 가장 자주 찾는 음료는 무엇인가요?', a: ['부드러운 꽃차', '과일차나 아이스티', '진한 커피나 구수한 곡물차', '향미가 풍부한 스페셜티 커피나 독특한 블렌드'] },
    { q: '가장 좋아하는 맛의 방향은 무엇인가요?', a: ['부드럽고 은은하게', '산뜻하고 선명하게', '구수하고 쌉싸름하게', '향은 화사하지만 맛은 깊고 묵직하게'] },
    { q: '원하는 한 잔의 무게감은?', a: ['가볍고 섬세하게', '맑고 상쾌하게', '진하고 묵직하게', '첫 향은 가볍지만 여운은 깊게'] },
    { q: '커피를 마시는 시간에 어떤 한 잔을 원하나요?', a: ['부드러운 꽃향의 차', '상쾌한 과일·허브차', '곡물과 뿌리로 만든 깊은 로스트', '커피 같은 깊이에 과일·꽃·허브 향을 더한 블렌드'] },
    { q: '가장 만들어보고 싶은 조합은?', a: ['장미와 캐모마일', '유자와 히비스커스', '민들레 뿌리와 단팥·보리', '유자와 민들레 뿌리, 또는 장미와 보리'] },
    { q: '나의 블렌딩 성향은?', a: ['부드럽고 쉬운 조합부터 시작하고 싶다', '좋아하는 향을 중심으로 조금씩 바꾸고 싶다', '진한 맛과 로스트 강도를 직접 조절하고 싶다', '서로 다른 원료를 연결해 새로운 맛을 만들고 싶다'] },
    { q: '원하는 마지막 여운은?', a: ['꽃향이 은은하게 남는 여운', '과일과 허브 향이 맑게 남는 여운', '볶은 곡물과 뿌리의 깊은 여운', '화사한 첫 향 뒤에 로스트가 길게 이어지는 여운'] },
  ];
  const RESULTS = {
    A: { name: '꽃이 머무는 정원', en: 'A Garden Where Flowers Stay', kit: 'ver1', kitName: 'VER.1 Taste', ing: ['장미', '캐모마일', '레몬밤'],
      desc: '강하고 자극적인 맛보다 은은한 꽃향과 부드러운 여운을 좋아합니다.',
      copy: '당신에게 좋은 차는 강하게 기억되는 차보다, 은은하게 오래 머무는 차입니다.',
      basic: { name: '가든 플로럴', ratio: '장미 2 · 캐모마일 1 · 레몬밤 ½', note: '꽃향을 중심에 두고 레몬밤으로 첫 향을 살짝 밝힙니다.' },
      cross: { name: '로즈 그레인', ratio: '장미 + 캐모마일 + 보리', note: '우아한 꽃향과 맑은 곡물의 여운이 만나는 플로럴 로스트 — 2개 세트에서.' } },
    B: { name: '햇살을 머금은 허브', en: 'Herbs Holding the Sunlight', kit: 'ver1', kitName: 'VER.1 Taste', ing: ['유자', '히비스커스', '페퍼민트', '레몬밤'],
      desc: '유자와 허브의 밝은 향, 선명한 산미와 상쾌한 여운을 좋아합니다.',
      copy: '당신의 취향은 한 모금만으로도 분위기를 바꾸는, 밝고 선명한 향에 가깝습니다.',
      basic: { name: '선라이트 시트러스', ratio: '유자 2 · 히비스커스 1 · 레몬밤 1 · 페퍼민트 ½', note: '아이스티로도 잘 어울립니다. 페퍼민트는 소량부터.' },
      cross: { name: '유자 로스트', ratio: '유자 + 민들레 뿌리 + 단팥', note: '유자의 밝은 첫 향 뒤에 깊은 볶음 향과 부드러운 고소함이 이어지는 시트러스 로스트 — 2개 세트에서.' } },
    C: { name: '깊은 뿌리의 로스트', en: 'Roast from the Deep Root', kit: 'ver2', kitName: 'VER.2 Depth', ing: ['민들레 뿌리', '둥굴레', '단팥', '보리'],
      desc: '볶은 향과 묵직한 바디감, 커피처럼 깊게 이어지는 여운을 좋아합니다.',
      copy: '커피의 분위기는 남기고, 곡물과 뿌리로 나만의 로스트를 만들어 보세요.',
      basic: { name: '브라질리언 로스트', ratio: '민들레 뿌리 2 · 단팥 2 · 찰수수 1 · 둥굴레 ½', note: '깊게 볶은 듯한 첫 향에 단팥과 찰수수의 부드러운 구수함이 이어집니다.' },
      cross: { name: '민트 로스트', ratio: '페퍼민트 + 레몬밤 + 보리', note: '상쾌하게 시작해 구수하고 깔끔하게 끝나는 허벌 로스트 — 2개 세트에서.' } },
    D: { name: '향이 피어나는 로스트', en: 'Roast Where Aroma Blooms', kit: 'set', kitName: '2개 세트 · Taste + Depth', ing: ['유자', '장미', '페퍼민트', '민들레 뿌리', '단팥', '보리', '둥굴레'],
      desc: '과일·꽃·허브의 첫 향과 깊은 로스트의 여운을 한 잔에서 함께 느끼고 싶은, 입체적인 취향입니다.',
      copy: '깊이는 로스트로 만들고, 취향은 향으로 완성하세요.',
      basic: { name: '딥 우드 로스트', ratio: '민들레 뿌리 2 · 둥굴레 2 · 단팥 1', note: '볶은 뿌리와 나무를 연상시키는 깊은 향, 둥굴레의 부드러운 바디감, 단팥의 고소한 마무리.' },
      cross: { name: '유자 로스트', ratio: '유자 + 민들레 뿌리 + 단팥', note: '같은 로스트도 유자를 더하면 밝게, 장미를 더하면 우아하게, 페퍼민트를 더하면 상쾌하게.' } },
  };
  const esc = s => String(s).replace(/[&<>"]/g, m => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[m]));
  function score(ans) { const c = { A: 0, B: 0, C: 0, D: 0 }; ans.forEach(k => c[k]++); const m = Math.max(c.A, c.B, c.C, c.D);
    const t = ['A', 'B', 'C', 'D'].filter(k => c[k] === m); return t.length === 1 ? t[0] : (t.includes(ans[0]) ? ans[0] : t[t.length - 1]); }

  function mount(root, opts = {}) {
    let step = 0; const ans = [];
    const intro = () => { root.innerHTML = `
      <div class="qz-intro">
        <div class="qz-eye">Taste Test · 1분 취향 찾기</div>
        <h2 class="qz-h">나는 향을 좋아할까,<br>깊이를 좋아할까?</h2>
        <p class="qz-p">여덟 개의 질문에 답하면 Taste · Depth · 2개 세트 가운데 오늘의 나에게 맞는 키트와, 처음 만들어 볼 레시피를 골라 드립니다. 개인정보는 수집하지 않습니다.</p>
        <button class="btnbox" data-act="start">테스트 시작하기</button>
      </div>`; };
    const question = () => { const Q = QUESTIONS[step]; root.innerHTML = `
      <div class="qz-q">
        <div class="qz-prog"><span>${step + 1} <i>/ ${QUESTIONS.length}</i></span><b style="width:${(step / QUESTIONS.length * 100).toFixed(1)}%"></b></div>
        <h2 class="qz-h">${esc(Q.q)}</h2>
        <ul class="qz-opts">${Q.a.map((t, i) => `<li><button class="qz-opt" data-k="${'ABCD'[i]}"><em>${'ABCD'[i]}</em><span>${esc(t)}</span></button></li>`).join('')}</ul>
        <div class="qz-nav">${step > 0 ? '<button class="qz-link" data-act="back">← 이전 질문</button>' : ''}</div>
      </div>`; root.scrollIntoView({ block: 'start' }); };
    const result = key => { const R = RESULTS[key]; root.innerHTML = `
      <div class="qz-res">
        <div class="qz-eye">Result · 유형 ${key}</div>
        <h2 class="qz-h">${esc(R.name)}<small>${esc(R.en)}</small></h2>
        <p class="qz-p">${esc(R.desc)}</p>
        <blockquote class="qz-quote">${esc(R.copy)}</blockquote>
        <div class="qz-grid">
          <div><div class="qz-lab">추천 키트</div><div class="qz-kit">${esc(R.kitName)}</div><div class="qz-ing">${R.ing.map(esc).join(' · ')}</div></div>
          <div><div class="qz-lab">처음 만들어 볼 레시피</div><div class="qz-rn">${esc(R.basic.name)}</div><div class="qz-ratio">${esc(R.basic.ratio)}</div><p>${esc(R.basic.note)}</p></div>
          <div><div class="qz-lab">교차 레시피</div><div class="qz-rn">${esc(R.cross.name)}</div><div class="qz-ratio">${esc(R.cross.ratio)}</div><p>${esc(R.cross.note)}</p></div>
        </div>
        <p class="qz-note">추천 비율은 취향을 발견하기 위한 첫 번째 기준일 뿐, 정답이 아닙니다. 한 번 맛본 뒤 마음에 드는 원료를 반 스푼씩 바꿔 보세요. 달라진 비율이 당신의 레시피가 됩니다.</p>
        <div class="qz-act"><button class="btnbox" data-act="kit" data-kit="${R.kit}">추천 키트 보기</button><button class="btnbox" data-act="retry">다시 해보기</button><button class="qz-link" data-act="share">결과 링크 복사</button><span class="qz-shared" hidden>복사했습니다</span></div>
      </div>`; root.scrollIntoView({ block: 'start' }); };
    root.addEventListener('click', e => { const b = e.target.closest('button'); if (!b) return;
      if (b.classList.contains('qz-opt')) { ans[step] = b.dataset.k; step++; step >= QUESTIONS.length ? result(score(ans)) : question(); return; }
      const act = b.dataset.act;
      if (act === 'start') question();
      else if (act === 'back') { step = Math.max(0, step - 1); question(); }
      else if (act === 'retry') { step = 0; ans.length = 0; question(); }
      else if (act === 'kit') opts.onKit && opts.onKit(b.dataset.kit);
      else if (act === 'share') { const key = root.querySelector('.qz-eye').textContent.slice(-1); const u = new URL(location.href); u.hash = ''; u.searchParams.set('result', key);
        (navigator.clipboard ? navigator.clipboard.writeText(u.toString()) : Promise.reject()).catch(() => {}).finally(() => { const s = root.querySelector('.qz-shared'); if (s) { s.hidden = false; setTimeout(() => s.hidden = true, 2400); } }); } });
    const r = new URLSearchParams(location.search).get('result');
    if (r && RESULTS[r]) result(r); else intro();
    return { intro, result };
  }
  global.RTTQuiz = { mount, QUESTIONS, RESULTS, score };
})(window);
