/* 취향의 권리 · 와디즈 상세 — 큰 타이틀 모션 그래픽 (GIF 변환용 4초 루프)
   사용:  <p class="big" data-mo="words" data-mo-fx="rise">같은 재료,<br>비율만 바꿨을 뿐인데.</p>
   data-mo     : chars(글자) | words(단어) | lines(문장·줄, <br> 기준)
   data-mo-fx  : rise(아래서 떠오름) | wave(물결) | glow(밝기 훑기) | mark(형광펜 밑줄) | slide(옆에서 밀려옴)
   data-mo-step: 단위 사이 시차(초, 선택). 기본은 전체 시차가 0.8초 이내가 되도록 자동.
   - 시차는 음수 지연으로 넣어 4초 주기가 처음부터 맞물린다(어느 4초를 잘라도 같은 GIF).
   - 주기 0초에는 모든 단위가 다 보이는 상태라 정지 캡처·포스터에도 문장이 온전히 남는다.
   - 안쪽 강조 요소(.gold, <b> 등)와 <br>은 그대로 유지한다. */
(function () {
  var T = 4;   // 주기(초) — motion.css 의 --mo-t 와 같아야 한다
  function wrap(node, mode, units) {
    var kids = Array.prototype.slice.call(node.childNodes);
    kids.forEach(function (k) {
      if (k.nodeType === 3) {
        var text = k.nodeValue; if (!text.trim()) return;
        var frag = document.createDocumentFragment();
        text.split(/(\s+)/).forEach(function (tok) {
          if (!tok) return;
          if (/^\s+$/.test(tok)) { frag.appendChild(document.createTextNode(tok)); return; }
          var w = document.createElement('span'); w.className = 'mo-w';
          if (mode === 'chars') {
            Array.from(tok).forEach(function (ch) {
              var c = document.createElement('span'); c.className = 'mo-u'; c.textContent = ch; w.appendChild(c); units.push(c);
            });
          } else { w.classList.add('mo-u'); w.textContent = tok; units.push(w); }
          frag.appendChild(w);
        });
        node.replaceChild(frag, k);
      } else if (k.nodeType === 1 && k.tagName !== 'BR' && !k.classList.contains('mo-u')) {
        wrap(k, mode, units);
      }
    });
  }
  function lines(el, units) {
    // <br> 기준으로 줄 묶음을 만든다
    var groups = [[]];
    Array.prototype.slice.call(el.childNodes).forEach(function (k) {
      if (k.nodeType === 1 && k.tagName === 'BR') groups.push([k]), groups.push([]);
      else groups[groups.length - 1].push(k);
    });
    groups.forEach(function (g) {
      if (!g.length || (g.length === 1 && g[0].tagName === 'BR')) return;
      if (!g.some(function (n) { return (n.textContent || '').trim(); })) return;
      var s = document.createElement('span'); s.className = 'mo-u mo-l';
      g[0].parentNode.insertBefore(s, g[0]); g.forEach(function (n) { s.appendChild(n); }); units.push(s);
    });
  }
  function run() {
    document.querySelectorAll('[data-mo]').forEach(function (el) {
      if (el.dataset.moDone) return; el.dataset.moDone = '1';
      var mode = el.dataset.mo, fx = el.dataset.moFx || 'rise', units = [];
      if (!el.getAttribute('aria-label')) el.setAttribute('aria-label', el.textContent.replace(/\s+/g, ' ').trim());
      if (mode === 'lines') lines(el, units); else wrap(el, mode, units);
      var n = units.length;
      var step = el.dataset.moStep ? parseFloat(el.dataset.moStep) : Math.min(mode === 'chars' ? 0.05 : 0.12, n > 1 ? 0.8 / (n - 1) : 0);
      el.classList.add('mo-tx', 'mo-tx-' + fx);
      units.forEach(function (u, i) {
        u.setAttribute('aria-hidden', 'true');
        u.style.animationDelay = (i * step - T).toFixed(3) + 's';
      });
    });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', run); else run();
})();
