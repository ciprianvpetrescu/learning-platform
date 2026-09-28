// learning.simplu.ie - single-page app
const $ = (s, r=document) => r.querySelector(s);
const $$ = (s, r=document) => [...r.querySelectorAll(s)];
const el = (t, a={}, ...kids) => {
  const n = document.createElement(t);
  for (const [k,v] of Object.entries(a)) {
    if (k === 'cls') n.className = v;
    else if (k === 'html') n.innerHTML = v;
    else if (k.startsWith('on')) n[k] = v;
    else n.setAttribute(k, v);
  }
  kids.flat().forEach(k => n.append(k?.nodeType ? k : document.createTextNode(k ?? '')));
  return n;
};
const esc = s => String(s ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));

const API = async (p, o={}) => {
  const r = await fetch(p, {credentials:'same-origin', headers:{'Content-Type':'application/json'}, ...o});
  if (r.status === 401) {
    // session gone: go to the shared portal login once, never reload in a loop
    if (!location.pathname.startsWith('/__login') && !window.__fredRedirecting) {
      window.__fredRedirecting = true;
      location.replace('/__login/login?next=' + encodeURIComponent(location.pathname + location.hash));
    }
    throw new Error('unauth');
  }
  const j = await r.json().catch(()=>({}));
  if (!r.ok) throw Object.assign(new Error(j.error || j.detail || 'request failed'), {data:j});
  return j;
};
const post = (p, body) => API(p, {method:'POST', body: JSON.stringify(body)});

let CATALOG = null, ME = null;

const state = { view:'home', cat:null, module:null, game:null, box:null };

// ---------------- sidebar ----------------
const ICONS = {networking:'●', linux:'▸', web:'◆', crypto:'🔒', forensics:'🔍', osint:'◎',
  malware:'☣', netsec:'⛨', cloud:'☁', blueteam:'◉', windows:'▣', coding:'⌘'};

function renderSide() {
  const cats = CATALOG?.categories || [];
  const done = (c) => c.modules.filter(m => m.progress?.done).length;
  $('#side').innerHTML = '';
  const brand = el('div', {cls:'brand'},
    el('div', {cls:'logo', html:'L'}),
    el('div', {}, el('h1', {}, 'learning.simplu.ie'), el('small', {}, 'cybersecurity academy')));
  $('#side').append(brand);
  $('#side').append(el('h4', {}, 'Overview'));
  const nv = (id, label, badge) => el('a', {
    cls:'item' + (state.view===id ? ' on':''), href:'#', onclick: (e)=>{e.preventDefault(); go(id);}
  }, el('span', {html:'▪'}), label, badge ? el('span',{cls:'badge'}, badge) : null);
  $('#side').append(nv('home','Dashboard'));
  $('#side').append(nv('boxes','Vulnerable Boxes', (CATALOG?.boxes||[]).length));
  $('#side').append(nv('leaderboard','Leaderboard'));
  $('#side').append(nv('profile','Profile'));
  $('#side').append(el('h4', {}, 'Categories'));
  cats.forEach(c => {
    const b = `${done(c)}/${c.modules.length}`;
    const a = el('a', {cls:'item' + (state.view==='cat' && state.cat===c.id ? ' on':''), href:'#',
      onclick:(e)=>{e.preventDefault(); go('cat', {cat:c.id});}},
      el('span', {cls:'dot', style:`background:${c.color}`}), c.name, el('span',{cls:'badge'}, b));
    $('#side').append(a);
  });
}

// ---------------- router ----------------
function go(view, opts={}) {
  Object.assign(state, {view, ...opts});
  renderSide();
  if (view === 'home') renderHome();
  else if (view === 'cat') renderCat(opts.cat);
  else if (view === 'module') renderModule(opts.module);
  else if (view === 'game') renderGame(opts.game);
  else if (view === 'boxes') renderBoxes();
  else if (view === 'box') renderBox(opts.box);
  else if (view === 'leaderboard') renderLeaderboard();
  else if (view === 'profile') renderProfile();
  window.scrollTo(0,0);
  location.hash = [view, opts.cat||opts.module||opts.game||opts.box].filter(Boolean).join('/');
}

const main = () => $('#main');
const head = (title, sub) => el('div', {cls:'topbar'},
  el('div', {}, el('h2', {}, title), sub ? el('div',{cls:'sub'}, sub) : null));

function statsBar() {
  return [
    el('div', {cls:'spacer'}),
    el('div', {cls:'stat'}, 'Points ', el('b',{}, ME?.points ?? 0)),
    el('div', {cls:'stat'}, 'Modules ', el('b',{}, ME?.modules_done ?? 0)),
    el('div', {cls:'stat'}, 'Flags ', el('b',{}, ME?.flags ?? 0)),
  ];
}
function topWithStats(title, sub) {
  const t = head(title, sub);
  t.append(...statsBar());
  return t;
}

// ---------------- home ----------------
function renderHome() {
  const m = main(); m.innerHTML = '';
  m.append(topWithStats('Dashboard', 'Pick a category, or spawn a box and break something.'));

  const totalMods = CATALOG.categories.reduce((a,c)=>a+c.modules.length,0);
  const totalGames = CATALOG.categories.reduce((a,c)=>a+c.game_count,0);
  const totalPts = CATALOG.categories.reduce((a,c)=>a+c.points,0);

  const tiles = el('div', {cls:'grid g3'});
  const tile = (n, l, s) => el('div', {cls:'card'}, el('h3', {}, n), el('p',{}, l), el('div',{cls:'muted', style:'margin-top:6px'}, s));
  tiles.append(
    tile(String(totalMods), 'Theory modules', `${CATALOG.categories.length} categories`),
    tile(String(totalGames), 'Mini-games', 'hands-on challenges'),
    tile(String(CATALOG.boxes.length), 'Vulnerable boxes', 'spawn a live instance'),
    tile(String(totalPts), 'Points available', 'complete everything'),
  );
  m.append(tiles);

  m.append(el('h3', {style:'margin:26px 0 12px;font-size:16px'}, 'Categories'));
  const g = el('div', {cls:'grid g2'});
  CATALOG.categories.forEach(c => {
    const done = c.modules.filter(x=>x.progress?.done).length;
    const pct = c.modules.length ? Math.round(done/c.modules.length*100) : 0;
    g.append(el('div', {cls:'card click', onclick:()=>go('cat',{cat:c.id})},
      el('h3', {}, el('span',{style:`color:${c.color}`}, ICONS[c.icon]||'•'), ' ', c.name),
      el('p', {}, c.blurb),
      el('div', {cls:'row'}, el('span',{cls:'chip'}, `${c.modules.length} modules`),
        el('span',{cls:'chip'}, `${c.game_count} games`), el('span',{cls:'pts'}, `${c.points} pts`)),
      el('div', {cls:'bar'}, el('i', {style:`width:${pct}%`}))));
  });
  m.append(g);

  m.append(el('h3', {style:'margin:28px 0 12px;font-size:16px'}, 'Quick start'));
  const qs = el('div', {cls:'grid g2'});
  const pick = CATALOG.categories.filter(c=>['web','networking','linux'].includes(c.id));
  pick.forEach(c => {
    const mod = c.modules.find(m=>!m.progress?.done) || c.modules[0];
    qs.append(el('div', {cls:'card click', onclick:()=>go('module',{module:mod.id})},
      el('span', {cls:'tier t-'+mod.tier}, mod.tier),
      el('h3', {style:'margin-top:8px'}, mod.title),
      el('p', {}, mod.summary),
      el('div', {cls:'row'}, el('span',{cls:'pts'}, mod.points+' pts'),
        el('span',{cls:'muted'}, c.name))));
  });
  m.append(qs);
}

// ---------------- category ----------------
function renderCat(cid) {
  const c = CATALOG.categories.find(x=>x.id===cid);
  if (!c) return go('home');
  const m = main(); m.innerHTML = '';
  const t = head(c.name, c.blurb); t.append(...statsBar()); m.append(t);

  m.append(el('h3', {style:'margin:6px 0 12px;font-size:15px'}, 'Modules'));
  const g = el('div', {cls:'grid g2'});
  c.modules.forEach(md => {
    const p = md.progress || {};
    const qs = p.quiz != null ? `${p.quiz}/${md.quiz_count}` : `${md.quiz_count}`;
    g.append(el('div', {cls:'card click', onclick:()=>go('module',{module:md.id})},
      el('div', {cls:'row', style:'margin:0 0 6px'}, el('span',{cls:'tier t-'+md.tier}, md.tier),
        p.done ? el('span',{cls:'done', style:'font-size:12px'}, '✓ complete') : null),
      el('h3', {}, md.title), el('p', {}, md.summary),
      el('div', {cls:'row'}, el('span',{cls:'chip'}, `${md.theory_count} topics`),
        el('span',{cls:'chip'}, `quiz ${qs}`), el('span',{cls:'chip'}, `${md.lab_count} labs`),
        el('span',{cls:'pts'}, md.points+' pts'))));
  });
  m.append(g);

  if (c.games.length) {
    m.append(el('h3', {style:'margin:26px 0 12px;font-size:15px'}, 'Mini-games'));
    const gg = el('div', {cls:'grid g3'});
    c.games.forEach(gm => {
      gg.append(el('div', {cls:'card click', onclick:()=>go('game',{game:gm.id})},
        el('h3', {}, gm.title), el('p', {}, gm.blurb),
        el('div', {cls:'row'}, el('span',{cls:'chip'}, gm.kind), el('span',{cls:'pts'}, gm.points+' pts'),
          gm.best ? el('span',{cls:'done'}, `best ${Math.round(gm.best*100)}%`) : null)));
    });
    m.append(gg);
  }

  const boxes = CATALOG.boxes.filter(b=>b.cat===c.id);
  if (boxes.length) {
    m.append(el('h3', {style:'margin:26px 0 12px;font-size:15px'}, 'Vulnerable boxes'));
    const bg = el('div', {cls:'grid g2'});
    boxes.forEach(b => bg.append(boxCard(b)));
    m.append(bg);
  }
}

function boxCard(b) {
  const inst = b.instance;
  return el('div', {cls:'card click', onclick:()=>go('box',{box:b.id})},
    el('div', {cls:'row', style:'margin:0 0 6px'}, el('span',{cls:'tier t-'+b.tier}, b.tier),
      inst ? el('span',{cls:'live', style:'font-size:11.5px'}, '● running') : el('span',{cls:'dead', style:'font-size:11.5px'}, '○ stopped')),
    el('h3', {}, b.title), el('p', {}, b.summary),
    el('div', {cls:'row'}, el('span',{cls:'pts'}, b.points+' pts'),
      (b.skills||[]).slice(0,3).map(s=>el('span',{cls:'chip'}, s))));
}

// ---------------- module ----------------
let QUIZ_ANSWERS = [];
function renderModule(mid) {
  API('/api/module/'+mid).then(d => {
    const md = d.module, m = main(); m.innerHTML = '';
    const c = CATALOG.categories.find(x=>x.id===md.cat);
    m.append(el('div', {cls:'crumbs'}, el('a',{href:'#',onclick:e=>{e.preventDefault();go('home');}},'Home'),
      ' / ', el('a',{href:'#',onclick:e=>{e.preventDefault();go('cat',{cat:md.cat});}}, c?.name||md.cat), ' / ', md.title));
    const t = head(md.title, md.summary);
    t.append(el('span', {cls:'tier t-'+md.tier, style:'align-self:center'}, md.tier),
      el('span', {cls:'pts', style:'align-self:center'}, md.points+' pts'));
    t.append(...statsBar()); m.append(t);

    // theory
    const th = el('div', {cls:'theory'});
    th.append(el('h3', {style:'margin-top:0'}, 'Theory'));
    (md.theory||[]).forEach(([h, body]) => { th.append(el('h3', {}, h), el('p', {}, body)); });
    m.append(th);

    const labs = el('div', {cls:'row', style:'margin:18px 0'});
    labs.append(el('button', {cls:'btn', onclick:()=>{
      post('/api/module/'+mid+'/read', {}).then(r => { ME.points = r.points; toast('Module marked as read, +' + Math.max(1, Math.floor(md.points/4)) + ' points'); renderSide(); });
    }}, 'Mark theory as read'));
    (md.labs||[]).forEach(l => {
      if (l.startsWith('game-')) labs.append(el('button', {cls:'btn sec', onclick:()=>go('game',{game:l})}, '▶ Play: '+l.replace('game-','').replace(/-/g,' ')));
      else if (l.startsWith('box-')) labs.append(el('button', {cls:'btn sec', onclick:()=>go('box',{box:l})}, '◈ Spawn: '+l.replace('box-','').replace(/-/g,' ')));
    });
    m.append(labs);

    // quiz
    if ((md.quiz||[]).length) {
      m.append(el('h3', {style:'margin:22px 0 12px;font-size:16px'}, `Knowledge check (${md.quiz.length} questions)`));
      QUIZ_ANSWERS = new Array(md.quiz.length).fill(null);
      md.quiz.forEach((q, i) => {
        const box = el('div', {cls:'q'});
        box.append(el('div', {cls:'qq'}, `${i+1}. ${q.q}`));
        q.a.forEach((opt, oi) => {
          box.append(el('label', {cls:'opt', id:`q${i}o${oi}`, onclick:()=>{
            QUIZ_ANSWERS[i] = oi;
            q.a.forEach((_, k)=>$('#q'+i+'o'+k).classList.remove('sel'));
            $('#q'+i+'o'+oi).classList.add('sel');
          }}, opt));
        });
        m.append(box);
      });
      const submit = el('button', {cls:'btn', style:'margin-top:8px'}, 'Submit answers');
      submit.onclick = () => {
        submit.disabled = true;
        post('/api/module/'+mid+'/quiz', {answers: QUIZ_ANSWERS}).then(r => {
          ME.points = r.points;
          r.detail.forEach((dd, i) => {
            md.quiz[i].a.forEach((_, oi) => {
              const n = $('#q'+i+'o'+oi); if (!n) return;
              n.classList.remove('sel');
              if (oi === dd.correct) n.classList.add('ok');
              else if (QUIZ_ANSWERS[i] === oi) n.classList.add('no');
            });
            $('.q:nth-of-type(' + (i+1) + ')')?.append(el('div', {cls:'why'}, dd.why));
          });
          toast(`Score ${r.score}/${r.total}`);
          renderSide();
          submit.textContent = `Score: ${r.score}/${r.total}`;
        }).catch(e => { submit.disabled = false; toast(e.message, true); });
      };
      m.append(submit);
    }
  }).catch(e => toast(e.message, true));
}

function toast(msg, bad) {
  const n = el('div', {cls:'notice ' + (bad?'bad':'ok'), style:'position:fixed;bottom:20px;right:20px;z-index:200;max-width:380px'}, msg);
  document.body.append(n);
  setTimeout(()=>n.remove(), 4200);
}

// ---------------- game engine ----------------
let GAME = null, GAME_ANSWERS = {}, GAME_TIMER = null, GAME_LEFT = 0;

function renderGame(gid) {
  API('/api/game/'+gid).then(d => {
    GAME = d; GAME_ANSWERS = {};
    const m = main(); m.innerHTML = '';
    m.append(el('div', {cls:'crumbs'}, el('a',{href:'#',onclick:e=>{e.preventDefault();go('home');}},'Home'),
      ' / ', 'game / ', d.game.title));
    const t = head(d.game.title, d.intro);
    t.append(el('span', {cls:'pts', style:'align-self:center'}, d.game.points+' pts'));
    if (d.seconds) {
      GAME_LEFT = d.seconds;
      const tm = el('div', {cls:'timer', id:'timer'}, fmtTime(GAME_LEFT));
      t.append(el('div', {style:'margin-left:auto;text-align:right'}, tm));
    }
    t.append(...statsBar()); m.append(t);

    const wrap = el('div', {id:'qwrap'});
    m.append(wrap);
    d.rounds.forEach((r, ri) => {
      const box = el('div', {cls:'q'});
      box.append(el('div', {cls:'qq'}, `${ri+1}. ${r.q}`));
      if (r.kind === 'quiz') {
        r.a.forEach((opt, oi) => {
          box.append(el('label', {cls:'opt', id:`g${ri}o${oi}`, onclick:()=>{
            GAME_ANSWERS[r.idx] = r.map[oi];
            r.a.forEach((_,k)=>$(`#g${ri}o${k}`).classList.remove('sel'));
            $(`#g${ri}o${oi}`).classList.add('sel');
          }}, opt));
        });
      } else if (r.kind === 'input') {
        const inp = el('input', {cls:'txt', placeholder:'your answer', oninput:(e)=>{GAME_ANSWERS[r.idx]=e.target.value;}});
        box.append(inp);
        if (r.hint) box.append(el('div', {cls:'muted', style:'margin-top:6px'}, 'hint: ' + r.hint));
      } else if (r.kind === 'order') {
        box.append(el('div', {cls:'muted', style:'margin-bottom:8px'}, 'Click items in the correct order. Click again to remove.'));
        const stack = el('div', {cls:'stack'});
        const chosen = [];
        r.items.forEach((it, ii) => {
          const node = el('div', {cls:'seq'}, el('span',{cls:'n'}, ''), it);
          node.onclick = () => {
            const at = chosen.indexOf(r.map[ii]);
            if (at >= 0) { chosen.splice(at,1); node.classList.remove('ok'); }
            else { chosen.push(r.map[ii]); node.classList.add('ok'); }
            $$('.seq', stack).forEach(s => s.querySelector('.n').textContent = '');
            chosen.forEach((orig, pos) => {
              const idx = r.map.indexOf(orig);
              stack.children[idx].querySelector('.n').textContent = String(pos+1);
            });
            GAME_ANSWERS[r.idx] = [...chosen];
          };
          stack.append(node);
        });
        box.append(stack);
      } else if (r.kind === 'pick') {
        r.items.forEach((it, ii) => {
          box.append(el('label', {cls:'opt', id:`g${ri}o${ii}`, onclick:()=>{
            GAME_ANSWERS[r.idx] = r.map[ii];
            r.items.forEach((_,k)=>$(`#g${ri}o${k}`).classList.remove('sel'));
            $(`#g${ri}o${ii}`).classList.add('sel');
          }}, it));
        });
      }
      wrap.append(box);
    });

    const row = el('div', {cls:'row', style:'margin-top:14px'});
    const btn = el('button', {cls:'btn'}, 'Submit');
    btn.onclick = () => submitGame(gid, d, btn);
    row.append(btn, el('button', {cls:'btn sec', onclick:()=>go('game',{game:gid})}, 'Restart'));
    m.append(row);

    if (d.seconds) {
      GAME_TIMER = setInterval(() => {
        GAME_LEFT--;
        const tm = $('#timer'); if (!tm) return clearInterval(GAME_TIMER);
        tm.textContent = fmtTime(GAME_LEFT);
        tm.classList.toggle('low', GAME_LEFT <= 10);
        if (GAME_LEFT <= 0) { clearInterval(GAME_TIMER); submitGame(gid, d, btn, true); }
      }, 1000);
    }
  }).catch(e => toast(e.message, true));
}
const fmtTime = s => `${Math.floor(s/60)}:${String(s%60).padStart(2,'0')}`;

function submitGame(gid, d, btn, auto) {
  if (GAME_TIMER) { clearInterval(GAME_TIMER); GAME_TIMER = null; }
  btn.disabled = true;
  const results = d.rounds.map(r => ({idx: r.idx, answer: GAME_ANSWERS[r.idx] ?? (r.kind==='order'?[]:null)}));
  post('/api/game/'+gid+'/submit', {results}).then(r => {
    ME.points = r.points;
    toast(`Score ${r.correct}/${r.total} (${Math.round(r.score*100)}%)  +${r.awarded} points` + (auto?' - time up':''), r.score < 0.5);
    // mark correct answers
    d.rounds.forEach((rd, ri) => {
      const res = r.results.find(x => x.idx === rd.idx);
      if (!res) return;
      if (rd.kind === 'quiz' || rd.kind === 'pick') {
        rd.a?.forEach((_, oi) => {
          const n = $(`#g${ri}o${oi}`); if (!n) return;
          n.classList.remove('sel');
          const origIdx = rd.map?.[oi];
          const correctOrig = rd.kind === 'quiz' ? res.correct : null;
          if (rd.kind === 'quiz' && origIdx === correctOrig) n.classList.add('ok');
          else if (GAME_ANSWERS[rd.idx] === origIdx) n.classList.add('no');
        });
      }
      if (res.why) $('.q:nth-of-type(' + (ri+1) + ')')?.append(el('div', {cls:'why'}, res.why));
    });
    btn.textContent = `Score: ${r.correct}/${r.total}`;
    renderSide();
    setTimeout(()=>{ btn.disabled = false; }, 1200);
  }).catch(e => { btn.disabled = false; toast(e.message, true); });
}

// ---------------- boxes ----------------
function renderBoxes() {
  const m = main(); m.innerHTML = '';
  const t = head('Vulnerable Boxes', 'Spawn a live instance, attack it from your own Kali sidecar. One hour per instance.');
  t.append(...statsBar()); m.append(t);
  if (!CATALOG.docker) {
    m.append(el('div', {cls:'notice bad'}, 'Docker is not reachable, so instances cannot be spawned right now.'));
  }
  const g = el('div', {cls:'grid g2'});
  CATALOG.boxes.forEach(b => g.append(boxCard(b)));
  m.append(g);
}

function renderBox(bid) {
  API('/api/boxes').then(d => {
    const b = d.boxes.find(x=>x.id===bid);
    if (!b) return go('boxes');
    const m = main(); m.innerHTML = '';
    const c = CATALOG.categories.find(x=>x.id===b.cat);
    m.append(el('div', {cls:'crumbs'}, el('a',{href:'#',onclick:e=>{e.preventDefault();go('home');}},'Home'),
      ' / ', el('a',{href:'#',onclick:e=>{e.preventDefault();go('boxes');}},'Boxes'), ' / ', b.title));
    const t = head(b.title, b.summary);
    t.append(el('span', {cls:'tier t-'+b.tier, style:'align-self:center'}, b.tier),
      el('span', {cls:'pts', style:'align-self:center'}, b.points+' pts'));
    t.append(...statsBar()); m.append(t);

    const info = el('div', {cls:'card'});
    info.append(el('h3', {}, b.teaches || 'What this box teaches'));
    info.append(el('div', {cls:'row'}, (b.skills||[]).map(s=>el('span',{cls:'chip'}, s))));
    if (b.entry) info.append(el('div', {cls:'brief', style:'margin-top:12px'}, 'Entry point: ' + b.entry));
    if ((b.hints||[]).length) {
      info.append(el('h3', {style:'margin-top:16px'}, 'Hints'));
      b.hints.forEach(h => info.append(el('p', {cls:'muted', style:'margin-bottom:5px'}, '• ' + h)));
    }
    m.append(info);

    const ctrl = el('div', {cls:'card', style:'margin-top:14px'});
    ctrl.append(el('h3', {}, 'Instance'));
    const body = el('div', {id:'instbody'}, el('p',{cls:'muted'},'Checking...'));
    ctrl.append(body);
    m.append(ctrl);
    drawInstance(b);
  }).catch(e => toast(e.message, true));
}

// ---- browser terminal: in-page draggable / resizable windows ----------
// ttyd runs inside the user's own kali sidecar; we proxy its websocket
// through /__term/<port>/ so it rides the same session cookie.
const XTERM_CSS = 'https://cdn.jsdelivr.net/npm/xterm@5.3.0/css/xterm.min.css';
const XTERM_JS  = 'https://cdn.jsdelivr.net/npm/xterm@5.3.0/lib/xterm.min.js';
const FIT_JS    = 'https://cdn.jsdelivr.net/npm/xterm-addon-fit@0.8.0/lib/xterm-addon-fit.min.js';
const ESC = String.fromCharCode(27);
const BANNER = ESC + '[32mconnected' + ESC + '[0m to your kali sidecar.\r\n\r\n';
const BYE = '\r\n' + ESC + '[31mdisconnected' + ESC + '[0m\r\n';

function loadScript(src) {
  return new Promise((res, rej) => {
    if ($$('script').some(s => s.src === src)) return res();
    const t = document.createElement('script');
    t.src = src; t.onload = res; t.onerror = rej;
    document.head.append(t);
  });
}

async function loadXterm() {
  if (window.Terminal && window.FitAddon) return true;
  if (!$$('link').some(l => l.href === XTERM_CSS)) {
    document.head.append(el('link', {rel:'stylesheet', href:XTERM_CSS}));
  }
  try { await loadScript(XTERM_JS); await loadScript(FIT_JS); }
  catch (e) { return false; }
  return !!window.Terminal;
}

// ---- window manager ---------------------------------------------------
// Windows live inside #winlayer: a fixed, see-through layer on top of the
// page. The layer ignores pointer events, each window takes them, so the
// description underneath stays readable and scrollable while you work.
const TERMS = [];
let WINZ = 400;
let WINN = 0;

function winLayer() {
  let l = $('#winlayer');
  if (!l) { l = el('div', {id:'winlayer'}); document.body.append(l); }
  return l;
}

function placeWin(w) {
  const l = winLayer(); if (!l || !w) return;
  l.append(w);
  const W = Math.min(900, Math.max(360, window.innerWidth - 80));
  const H = Math.min(540, Math.max(300, window.innerHeight - 120));
  const off = (WINN++ % 7) * 28;
  const maxL = Math.max(10, window.innerWidth  - W - 20);
  const maxT = Math.max(10, window.innerHeight - H - 20);
  w.style.width  = W + 'px';
  w.style.height = H + 'px';
  w.style.left   = Math.min(maxL, 120 + off) + 'px';
  w.style.top    = Math.min(maxT, 130 + off) + 'px';
  focusWin(w);
}

function focusWin(w) {
  if (!w || !document.body.contains(w)) return;
  w.style.zIndex = ++WINZ;
  $$('.win.on').forEach(x => { if (x !== w) x.classList.remove('on'); });
  w.classList.add('on');
}

function closeWin(w) {
  if (!w) return;
  const i = TERMS.indexOf(w);
  if (i >= 0) TERMS.splice(i, 1);
  w._closed = true;
  if (w._ka) clearInterval(w._ka);
  try { if (w._ws) w._ws.close(); } catch (e) {}
  if (w._onWinResize) window.removeEventListener('resize', w._onWinResize);
  try { if (w._termObj) w._termObj.dispose(); } catch (e) {}
  w.remove();
  toast(w._term ? 'Terminal closed' : 'Window closed');
}

function termFit(w) {
  if (!w || !w._fit || !document.body.contains(w)) return;
  try { w._fit.fit(); } catch (e) {}
}

let FIT_T = null;
function fitSoon(w) { clearTimeout(FIT_T); FIT_T = setTimeout(function(){ termFit(w); }, 60); }

function clampWin(w) {
  const r = w.getBoundingClientRect();
  w.style.left = Math.min(Math.max(0, r.left), Math.max(0, window.innerWidth  - 120)) + 'px';
  w.style.top  = Math.min(Math.max(0, r.top),  Math.max(0, window.innerHeight - 40))  + 'px';
  fitSoon(w);
}

function dragMove(w, grip) {
  let sx = 0, sy = 0, bx = 0, by = 0, on = false;
  const move = e => {
    if (!on) return;
    e.preventDefault();
    const nl = Math.min(Math.max(0, bx + e.clientX - sx), Math.max(0, window.innerWidth  - 100));
    const nt = Math.min(Math.max(0, by + e.clientY - sy), Math.max(0, window.innerHeight - 42));
    w.style.left = nl + 'px';
    w.style.top  = nt + 'px';
  };
  const release = () => {
    on = false;
    document.documentElement.style.userSelect = '';
    grip.classList.remove('grab');
    window.removeEventListener('pointermove', move);
    window.removeEventListener('pointerup', release);
  };
  grip.addEventListener('pointerdown', e => {
    if (e.button !== 0 || (e.target.closest && e.target.closest('.wbtn'))) return;
    const r = w.getBoundingClientRect();
    on = true; sx = e.clientX; sy = e.clientY; bx = r.left; by = r.top;
    focusWin(w);
    window.addEventListener('pointermove', move);
    window.addEventListener('pointerup', release);
    document.documentElement.style.userSelect = 'none';
    grip.classList.add('grab');
    e.preventDefault();
    if (grip.setPointerCapture) { try { grip.setPointerCapture(e.pointerId); } catch (err) {} }
  });
}

function dragSize(w, grip) {
  let sx = 0, sy = 0, bw = 0, bh = 0, bx = 0, by = 0, on = false;
  const move = e => {
    if (!on) return;
    e.preventDefault();
    const nw = Math.max(320, bw + e.clientX - sx);
    const nh = Math.max(180, bh + e.clientY - sy);
    w.style.width  = Math.min(nw, window.innerWidth  - bx - 4) + 'px';
    w.style.height = Math.min(nh, window.innerHeight - by - 4) + 'px';
    fitSoon(w);
  };
  const release = () => {
    on = false;
    document.documentElement.style.userSelect = '';
    window.removeEventListener('pointermove', move);
    window.removeEventListener('pointerup', release);
  };
  grip.addEventListener('pointerdown', e => {
    if (e.button !== 0) return;
    const r = w.getBoundingClientRect();
    on = true; sx = e.clientX; sy = e.clientY; bw = r.width; bh = r.height; bx = r.left; by = r.top;
    focusWin(w);
    window.addEventListener('pointermove', move);
    window.addEventListener('pointerup', release);
    document.documentElement.style.userSelect = 'none';
    e.preventDefault(); e.stopPropagation();
    if (grip.setPointerCapture) { try { grip.setPointerCapture(e.pointerId); } catch (err) {} }
  });
}

// ---- terminal windows -------------------------------------------------
function openTerminal(b) {
  b = b || {};
  const slot  = TERMS.length + 1;
  const title = b.title || b.id || 'box';
  const bid   = b.id || b.box || '';

  const win  = el('div', {cls:'win'});
  win._term  = true;
  const head = el('div', {cls:'winhead'});
  const dot  = el('span', {cls:'wdot'});
  const name = el('span', {cls:'wname'}, 'Terminal ' + slot + ' - ' + title);
  const meta = el('span', {cls:'wmeta'}, 'connecting...');
  const btnNew = el('button', {cls:'wbtn', title:'New terminal', onclick: e => { e.stopPropagation(); openTerminal(b); }}, '+');
  const btnFit = el('button', {cls:'wbtn', title:'Keep inside the page', onclick: e => { e.stopPropagation(); clampWin(win); }}, 'FIT');
  const btnX   = el('button', {cls:'wbtn x', title:'Close', onclick: e => { e.stopPropagation(); closeWin(win); }}, 'X');
  head.append(dot, name, meta, el('span', {cls:'wspace'}), btnNew, btnFit, btnX);
  const screen = el('div', {cls:'winscreen'});
  const grip   = el('div', {cls:'wgrip', title:'Drag to resize'});
  win.append(head, screen, grip);

  dragMove(win, head);
  dragSize(win, grip);

  screen.append(el('div', {cls:'wmsg'},
    el('div', {cls:'wmsgline'}, 'Starting terminal...'),
    el('div', {cls:'wmsgsub'}, 'Attack terminal for ' + title + (bid ? ' (' + bid + ')' : ''))));

  TERMS.push(win);
  placeWin(win);
  startTerm(win, screen, b, dot, meta);
  return win;
}

function termFail(screen, dot, meta, msg) {
  screen.innerHTML = '';
  screen.append(el('div', {cls:'wmsg'},
    el('div', {cls:'wmsgline'}, msg),
    el('div', {cls:'wmsgsub'}, 'Spawn the instance for this box first, then open the terminal again.')));
  dot.classList.remove('live'); dot.classList.add('bad');
  if (meta) meta.textContent = 'offline';
}

async function startTerm(win, screen, b, dot, meta) {
  let info;
  try { info = await API('/api/terminal'); }
  catch (e) { return termFail(screen, dot, meta, 'Could not reach the terminal service.'); }
  if (!info.up) return termFail(screen, dot, meta, 'No live instance.');
  win._info = info;
  if (info.host_ip) meta.textContent = 'to ' + info.host_ip;

  if (!(await loadXterm())) return termFail(screen, dot, meta, 'Could not load the terminal library.');
  if (!document.body.contains(win)) return;

  screen.innerHTML = '';
  const term = new window.Terminal({
    fontSize: 13.5, cursorBlink: true,
    fontFamily: 'ui-monospace, SFMono-Regular, Menlo, monospace',
    theme: { background:'#0d1117', foreground:'#c9d1d9', cursor:'#58a6ff' },
  });
  const fit = new window.FitAddon.FitAddon();
  term.loadAddon(fit);
  term.open(screen);
  win._termObj = term; win._fit = fit;
  win._onWinResize = () => fitSoon(win);
  window.addEventListener('resize', win._onWinResize);
  termFit(win);

  const proto = location.protocol === 'https:' ? 'wss:' : 'ws:';
  const wsurl = proto + '//' + location.host + info.path + 'ws';
  let ws;
  try { ws = new WebSocket(wsurl, 'tty'); }
  catch (e) { return termFail(screen, dot, meta, 'Terminal connection failed.'); }
  ws.binaryType = 'arraybuffer';
  win._ws = ws;

  // ttyd speaks an all-binary protocol: init -> raw JSON, input -> '0'+data,
  // resize -> '1'+{columns,rows}
  const enc = new TextEncoder();
  const sendBin = txt => { if (ws.readyState === 1) ws.send(enc.encode(txt)); };

  ws.onopen = () => {
    dot.classList.add('live');
    meta.textContent = (info.host_ip ? 'to ' + info.host_ip : 'live');
    term.write(BANNER);
    sendBin(JSON.stringify({AuthToken:'', columns: term.cols, rows: term.rows}));
    term.onData(d => sendBin('0' + d));
    term.onResize(({cols, rows}) => sendBin('1' + JSON.stringify({columns: cols, rows: rows})));
    if (win._ka) clearInterval(win._ka);
    win._ka = setInterval(() => {
      if (ws.readyState === 1) ws.send(enc.encode('0'));
      else clearInterval(win._ka);
    }, 25000);
    term.focus();
  };
  ws.onmessage = ev => {
    let txt;
    if (typeof ev.data === 'string') txt = ev.data;
    else txt = new TextDecoder().decode(ev.data);
    if (txt[0] === '0') term.write(txt.slice(1));
    else if (txt[0] === '1') fitSoon(win);
    else term.write(txt);
  };
  ws.onclose = () => {
    if (win._ka) clearInterval(win._ka);
    dot.classList.remove('live'); dot.classList.add('bad');
    meta.textContent = 'closed';
    if (!win._closed) term.write(BYE);
  };
  ws.onerror = () => { dot.classList.remove('live'); dot.classList.add('bad'); meta.textContent = 'error'; };
}

// keep terminals alive across in-app navigation, close them on a real reload
window.addEventListener('beforeunload', () => { TERMS.slice().forEach(closeWin); });

// companion window with the box details, so you can park it next to the
// terminal and still read both
function openInfoWindow(b) {
  b = b || {};
  const title = b.title || b.id || 'box';
  const win = el('div', {cls:'win'});
  const head = el('div', {cls:'winhead'});
  const dot = el('span', {cls:'wdot live'});
  const name = el('span', {cls:'wname'}, 'Box - ' + title);
  const btnX = el('button', {cls:'wbtn x', title:'Close', onclick: e => { e.stopPropagation(); closeWin(win); }}, 'X');
  head.append(dot, name, el('span', {cls:'wspace'}), btnX);
  const body = el('div', {cls:'winbody'});
  const inst = b.instance || {};
  body.append(el('div', {cls:'term'}, ['target IP    ' + (inst.host_ip || 'n/a'),
    'network      ' + (inst.subnet || 'n/a'),
    'ports        ' + ((inst.ports || []).join(', ') || 'n/a'),
    'kali sidecar ' + (inst.kali_ip || 'n/a')].join('\n')));
  if (b.entry) body.append(el('p', {cls:'muted', style:'margin-top:10px'}, 'Entry point: ' + b.entry));
  (b.hints || []).forEach(h => body.append(el('p', {cls:'muted', style:'margin-bottom:5px'}, '- ' + h)));
  const grip = el('div', {cls:'wgrip', title:'Drag to resize'});
  win.append(head, body, grip);
  dragMove(win, head);
  dragSize(win, grip);
  placeWin(win);
  return win;
}

function drawInstance(b) {
  const body = $('#instbody'); if (!body) return;
  const inst = b.instance;
  body.innerHTML = '';
  if (!inst) {
    body.append(el('p', {cls:'muted', style:'margin-bottom:12px'}, 'No live instance for this box.'));
    const btn = el('button', {cls:'btn'}, 'Spawn instance');
    btn.onclick = () => {
      btn.disabled = true; btn.textContent = 'Starting containers...';
      post('/api/spawn', {box:b.id}).then(r => {
        toast('Instance started'); renderBox(b.id);
      }).catch(e => { btn.disabled = false; btn.textContent = 'Spawn instance'; toast(e.message, true); });
    };
    body.append(btn);
    return;
  }
  body.append(el('div', {cls:'notice ok'}, `Running. Expires in ${Math.floor((inst.ttl_left||0)/60)} minutes.`));
  body.append(el('div', {cls:'term'}, `target IP   ${inst.host_ip}\nnetwork     ${inst.subnet}\nports       ${(inst.ports||[]).join(', ') || 'n/a'}\nkali sidecar ${inst.kali_ip || 'n/a'}`));
  const row = el('div', {cls:'row', style:'margin-top:12px'});
  const termBtn = el('button', {cls:'btn'}, 'Open terminal');
  termBtn.onclick = () => openTerminal(b);
  const det = el('button', {cls:'btn sec'}, 'Box details window');
  det.onclick = () => openInfoWindow(b);
  const cmd = el('button', {cls:'btn sec'}, 'Show commands');
  cmd.onclick = () => {
    let lines = [];
    if ((inst.ports||[]).length) lines.push(`nmap -sV -p ${inst.ports.join(',')} ${inst.host_ip}`);
    else lines.push(`ping -c 3 ${inst.host_ip}`);
    lines.push(`curl -sv http://${inst.host_ip}/`);
    if ((inst.ports||[]).includes(22)) lines.push(`ssh analyst@${inst.host_ip}`);
    const box = el('div', {cls:'term', style:'margin-top:10px'}, lines.join('\n'));
    body.append(box);
  };
  const stop = el('button', {cls:'btn danger'}, 'Stop instance');
  stop.onclick = () => { stop.disabled = true; post('/api/stop', {box:b.id}).then(()=>{ toast('Instance stopped'); renderBox(b.id); }); };
  const flagBtn = el('button', {cls:'btn'}, 'Submit flag');
  flagBtn.onclick = () => {
    const f = prompt('Paste the flag you captured:');
    if (!f) return;
    post('/api/flag', {flag:f}).then(r => {
      ME.points = r.points;
      toast(r.ok ? (r.new ? 'Flag accepted! +50 points' : 'Flag already captured') : 'Not a valid flag for your live instances', !r.ok);
      if (r.ok) { renderSide(); renderBox(b.id); }
    }).catch(e => toast(e.message, true));
  };
  row.append(termBtn, det, cmd, flagBtn, stop);
  body.append(row);
}

// ---------------- leaderboard ----------------
function renderLeaderboard() {
  API('/api/leaderboard').then(d => {
    const m = main(); m.innerHTML = '';
    const t = head('Leaderboard', 'Points from modules, quizzes, games and captured flags.');
    t.append(...statsBar()); m.append(t);
    const tb = el('table', {cls:'t'});
    tb.append(el('tr', {}, el('th',{},'#'), el('th',{},'User'), el('th',{},'Points')));
    d.leaderboard.forEach((r, i) => tb.append(el('tr', {},
      el('td', {}, String(i+1)),
      el('td', {}, r.user + (r.user===ME.user ? ' (you)' : '')),
      el('td', {}, el('b',{style:'color:var(--accent)'}, String(r.points))))));
    if (!d.leaderboard.length) tb.append(el('tr', {}, el('td',{colspan:3,cls:'muted'},'Nobody yet.')));
    m.append(el('div',{cls:'card'}, tb));
  }).catch(e => toast(e.message, true));
}

// ---------------- profile ----------------
function renderProfile() {
  API('/api/progress').then(d => {
    const m = main(); m.innerHTML = '';
    const t = head(ME.user, 'Your progress.');
    t.append(...statsBar()); m.append(t);
    const st = d.progress;
    const card = el('div', {cls:'card'});
    card.append(el('h3', {}, 'Summary'));
    card.append(el('div', {cls:'row'},
      el('span',{cls:'chip'}, `points ${d.points}`),
      el('span',{cls:'chip'}, `modules completed ${ME.modules_done}`),
      el('span',{cls:'chip'}, `games played ${ME.games_played}`),
      el('span',{cls:'chip'}, `flags ${(st.flags||[]).length}`)));
    m.append(card);

    const tb = el('table', {cls:'t'});
    tb.append(el('tr', {}, el('th',{},'Module'), el('th',{},'Theory'), el('th',{},'Quiz'), el('th',{},'Status')));
    Object.entries(st.modules||{}).forEach(([id, v]) => {
      tb.append(el('tr', {}, el('td',{},id), el('td',{}, v.theory_read?'read':'—'),
        el('td',{}, v.quiz!=null?String(v.quiz):'—'),
        el('td',{}, v.done? el('span',{cls:'done'},'complete') : 'in progress')));
    });
    if (!Object.keys(st.modules||{}).length) tb.append(el('tr',{},el('td',{colspan:4,cls:'muted'},'No activity yet. Start with a module.')));
    m.append(el('div', {cls:'card', style:'margin-top:14px'}, el('h3',{},'Module progress'), tb));

    const gtb = el('table', {cls:'t'});
    gtb.append(el('tr', {}, el('th',{},'Game'), el('th',{},'Best'), el('th',{},'Attempts')));
    Object.entries(st.games||{}).forEach(([id, v]) => gtb.append(el('tr',{},
      el('td',{},id), el('td',{},Math.round((v.best||0)*100)+'%'), el('td',{},String(v.attempts||0)))));
    if (!Object.keys(st.games||{}).length) gtb.append(el('tr',{},el('td',{colspan:3,cls:'muted'},'No games played yet.')));
    m.append(el('div', {cls:'card', style:'margin-top:14px'}, el('h3',{},'Game scores'), gtb));

    if ((st.flags||[]).length) {
      m.append(el('div', {cls:'card', style:'margin-top:14px'}, el('h3',{},'Captured flags'),
        el('div', {cls:'term'}, st.flags.join('\n'))));
    }
  }).catch(e => toast(e.message, true));
}

// ---------------- boot ----------------
async function boot() {
  try {
    ME = await API('/api/me');
    CATALOG = await API('/api/catalog');
    CATALOG.docker = (await API('/api/boxes').catch(()=>({docker:false}))).docker;
  } catch(e) { document.body.innerHTML = '<div style="padding:60px;font-family:system-ui;color:#c9d6e2">'+esc(e.message)+'</div>'; return; }
  renderSide();
  const h = location.hash.replace('#','').split('/').filter(Boolean);
  if (h[0]) go(h[0], {cat:h[1], module:h[1], game:h[1], box:h[1]});
  else go('home');
}
window.addEventListener('hashchange', () => {
  const h = location.hash.replace('#','').split('/').filter(Boolean);
  if (!h.length) return;
  if (state.view === h[0] && (state.cat===h[1]||state.module===h[1]||state.game===h[1]||state.box===h[1])) return;
  go(h[0], {cat:h[1], module:h[1], game:h[1], box:h[1]});
});
boot();
