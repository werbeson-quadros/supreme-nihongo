const $ = (selector) => document.querySelector(selector);
const savedRate = Number(localStorage.getItem('n5PlaybackRate'));
const playbackRate = [0.5,0.75,0.85,1,1.25,1.5,2].includes(savedRate) ? savedRate : 1;
const savedLevel = localStorage.getItem('n5Level');
const state = {mode:'Listening',level:['N5','N4','N3'].includes(savedLevel) ? savedLevel : 'N5',id:null,exerciseId:null,glossary:[],voice:2,replays:0,playStarted:false,playbackRate,particlePause:localStorage.getItem('n5ParticlePause') === 'true',loading:false,loadToken:0,phraseCount:0};
const audio = $('#audio');
const dialog = $('#resultDialog');
const themeToggle = $('#themeToggle');
$('#playbackRate').value = String(state.playbackRate);
$('#dialogPlaybackRate').value = String(state.playbackRate);
$('#particlePause').checked = state.particlePause;
audio.defaultPlaybackRate = state.playbackRate;
audio.playbackRate = state.playbackRate;

function audioStatus(message) {
  $('#audioStatus').textContent = message;
  $('#dialogAudioStatus').textContent = message;
}

function updateThemeButton() {
  const dark = document.documentElement.dataset.theme === 'dark';
  themeToggle.setAttribute('aria-pressed', String(dark));
  themeToggle.setAttribute('aria-label', dark ? 'Ativar tema claro' : 'Ativar tema escuro');
  themeToggle.innerHTML = dark ? '☀ <span>Tema claro</span>' : '☾ <span>Tema escuro</span>';
}
themeToggle.addEventListener('click', () => {
  const next = document.documentElement.dataset.theme === 'dark' ? 'light' : 'dark';
  document.documentElement.dataset.theme = next;
  localStorage.setItem('n5Theme', next);
  updateThemeButton();
});
updateThemeButton();

for (let i = 0; i < 56; i++) {
  const bar = document.createElement('span');
  bar.className = 'bar';
  bar.style.height = `${8 + ((i * 17 + i * i * 7) % 24)}px`;
  $('#wave').append(bar);
}

async function api(url, options) {
  const response = await fetch(url, options);
  const data = await response.json();
  if (!response.ok) throw new Error(data.error || 'Não foi possível concluir a operação.');
  return data;
}

async function loadVoices() {
  const select = $('#voiceSelect');
  try {
    const data = await api('/api/voices');
    const preferred = Number(localStorage.getItem('n5Voice') || 2);
    select.replaceChildren();
    for (const voice of data.voices) {
      const option = document.createElement('option');
      option.value = voice.id;
      option.textContent = voice.label;
      select.append(option);
    }
    state.voice = data.voices.some(v => v.id === preferred) ? preferred : data.voices[0].id;
    select.value = String(state.voice);
  } catch (error) {
    select.replaceChildren(new Option(`Voz indisponível: ${error.message}`, '2'));
  }
}

function setMode(mode) {
  if (mode !== 'Listening' && mode !== 'Writing') return;
  state.mode = mode;
  audio.pause();
  for (const button of document.querySelectorAll('[data-mode]')) {
    button.classList.toggle('active', button.dataset.mode === mode);
    if (button.getAttribute('role') === 'tab') button.setAttribute('aria-selected',String(button.dataset.mode === mode));
  }
  const writing = mode === 'Writing';
  $('#topMode').textContent = writing ? 'WRITING' : 'LISTENING';
  $('#heroEyebrow').textContent = writing ? '作文 · GRAMÁTICA E VOCABULÁRIO' : '聴解 · COMPREENSÃO AUDITIVA';
  $('#heroTitle').innerHTML = writing ? 'Complete a frase.<br><em>Construa em japonês.</em>' : 'Treine o ouvido.<br><em>Palavra por palavra.</em>';
  $('#heroDescription').textContent = writing ? 'Leia o objetivo em português e preencha somente os trechos que faltam na frase japonesa.' : `Uma frase ${state.level} por vez. Ouça quantas vezes precisar e escreva exatamente o que entendeu.`;
  $('#exerciseTitle').textContent = writing ? 'Complete a frase' : 'Ouça a frase';
  $('#playerBlock').hidden = false;
  $('#playerPrompt').hidden = !writing;
  $('#answerForm').hidden = writing;
  $('#writingPanel').hidden = !writing;
  $('#clozeForm').hidden = !writing;
  $('#accuracyLabel').textContent = writing ? 'precisão de escrita ponderada' : 'precisão de escuta';
  $('#rankingMode').textContent = writing ? 'ESCRITA' : 'ESCUTA';
  $('#progressCopy').textContent = writing ? 'Ordenadas pelos erros de escrita.' : 'Ordenadas pelos erros de escuta.';
  loadPhrase();
  refreshStats();
}

function setLevel(level) {
  if (!['N5','N4','N3'].includes(level)) return;
  state.level = level;
  localStorage.setItem('n5Level', level);
  $('#levelSelect').value = level;
  $('#levelPill').textContent = `NÍVEL ${level}`;
  document.title = `Prática ${level} · Supreme Nihongo`;
  if (state.mode === 'Listening') $('#heroDescription').textContent = `Uma frase ${level} por vez. Ouça quantas vezes precisar e escreva exatamente o que entendeu.`;
  refreshMetadata();
  loadPhrase();
  refreshStats();
}

async function refreshMetadata() {
  try {
    const data = await api('/api/metadata');
    state.phraseCount = data.levels[state.level].phrase_count;
    $('#phraseCountMain').textContent = `/ ${state.phraseCount}`;
  } catch (error) { console.error(error); }
}

async function loadAudio() {
  const current = ++state.loadToken;
  state.loading = true;
  state.playStarted = false;
  $('#play').disabled = true;
  $('#dialogPlay').disabled = true;
  audioStatus('Preparando áudio…');
  audio.src = `/api/audio/${state.id}?speaker=${state.voice}&spaced=${state.particlePause ? 1 : 0}`;
  audio.playbackRate = state.playbackRate;
  try {
    await new Promise((resolve,reject) => {
      audio.oncanplay = resolve;
      audio.onerror = () => reject(new Error('O áudio não carregou. Verifique o VOICEVOX.'));
      audio.load();
    });
    if (current !== state.loadToken) return;
    audioStatus('Pronto para ouvir');
    $('#play').disabled = false;
    $('#dialogPlay').disabled = false;
  } catch (error) {
    if (current === state.loadToken) audioStatus(error.message);
  } finally {
    if (current === state.loadToken) state.loading = false;
  }
}

function renderCloze(phrase) {
  $('#objective').textContent = phrase.translation_pt;
  const parts = $('#clozeParts');
  parts.replaceChildren();
  let activeBlank = null;
  for (const part of phrase.parts) {
    if (part.blank) {
      const input = document.createElement('input');
      input.type = 'text';
      input.className = 'blank-input';
      input.dataset.index = part.index;
      input.placeholder = '____';
      input.setAttribute('aria-label',`Lacuna ${parts.querySelectorAll('input').length + 1}`);
      input.lang = 'ja';
      input.spellcheck = false;
      input.autocomplete = 'off';
      input.required = true;
      input.addEventListener('focus', () => { activeBlank = input; });
      parts.append(input);
    } else {
      const span = document.createElement('span');
      span.className = 'fixed-part';
      span.textContent = part.surface;
      parts.append(span);
    }
  }
  const mark = document.createElement('span');
  mark.className = 'fixed-part';
  mark.textContent = phrase.punctuation;
  parts.append(mark);
  const choices = $('#clozeChoices');
  choices.replaceChildren();
  for (const surface of phrase.choices) {
    const button = document.createElement('button');
    button.type = 'button';
    button.className = 'choice-word';
    button.textContent = surface;
    button.addEventListener('click', () => {
      const inputs = [...parts.querySelectorAll('input')];
      const target = activeBlank && !activeBlank.value.trim() ? activeBlank : inputs.find(input => !input.value.trim()) || activeBlank || inputs[0];
      if (!target) return;
      target.value = surface;
      target.dispatchEvent(new Event('input', {bubbles:true}));
      (inputs.find(input => !input.value.trim()) || target).focus();
    });
    choices.append(button);
  }
}

async function loadPhrase() {
  const mode = state.mode;
  const current = ++state.loadToken;
  state.id = null;
  state.exerciseId = null;
  state.glossary = [];
  stopSelectionSpeech();
  state.replays = 0;
  state.playStarted = false;
  audio.pause();
  $('#replays').textContent = '0 reproduções';
  $('#answer').value = '';
  $('#category').textContent = 'Preparando frase…';
  $('#play').disabled = true;
  try {
    const level = state.level;
    const phrase = await api(`${mode === 'Writing' ? '/api/cloze/next' : '/api/next'}?level=${level}`);
    if (current !== state.loadToken || state.mode !== mode || state.level !== level) return;
    state.id = phrase.id;
    state.exerciseId = phrase.exercise_id || null;
    state.glossary = phrase.glossary || [];
    $('#category').textContent = phrase.category;
    const number = level === 'N3' ? phrase.id - 2200 : level === 'N4' ? phrase.id - 1000 : phrase.id;
    $('.exercise-number').innerHTML = `${String(number).padStart(2,'0')} <small>/ ${state.phraseCount || '…'}</small>`;
    if (mode === 'Writing') renderCloze(phrase);
    loadAudio();
  } catch (error) {
    $('#category').textContent = error.message;
  }
}

function updatePlayButton(playing) {
  const button = $('#play');
  button.setAttribute('aria-label', playing ? 'Pausar áudio' : 'Reproduzir áudio');
  button.title = playing ? 'Pausar áudio' : 'Reproduzir áudio';
  button.innerHTML = playing
    ? '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M6 4h4v16H6zm8 0h4v16h-4z"/></svg>'
    : '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M8 5v14l11-7z"/></svg>';
  const dialogButton = $('#dialogPlay');
  dialogButton.textContent = playing ? 'Ⅱ' : '▶';
  dialogButton.setAttribute('aria-label', playing ? 'Pausar frase em japonês' : 'Reproduzir frase em japonês');
}

function playAudio(restart = false) {
  if (state.loading || !state.id) return;
  window.getSelection()?.removeAllRanges();
  stopSelectionSpeech();
  if (restart || audio.ended) { audio.currentTime = 0; state.playStarted = false; }
  audio.play().then(() => {
    if (!state.playStarted) {
      state.playStarted = true;
      state.replays++;
      $('#replays').textContent = `${state.replays} ${state.replays === 1 ? 'reprodução' : 'reproduções'}`;
    }
  }).catch(() => { audioStatus('Não foi possível reproduzir o áudio.'); });
}

audio.addEventListener('play', () => {
  $('.player').classList.add('playing');
  audioStatus('Reproduzindo…');
  updatePlayButton(true);
});
audio.addEventListener('pause', () => {
  $('.player').classList.remove('playing');
  if (!audio.ended && !state.loading && state.playStarted) audioStatus('Pausado');
  updatePlayButton(false);
});
audio.addEventListener('ended', () => {
  $('.player').classList.remove('playing');
  state.playStarted = false;
  audioStatus('Fim do áudio');
  updatePlayButton(false);
});
$('#play').addEventListener('click', () => audio.paused ? playAudio() : audio.pause());
$('#dialogPlay').addEventListener('click', () => audio.paused ? playAudio() : audio.pause());
function setPlaybackRate(rate) {
  state.playbackRate = rate;
  $('#playbackRate').value = String(rate);
  $('#dialogPlaybackRate').value = String(rate);
  audio.defaultPlaybackRate = state.playbackRate;
  audio.playbackRate = state.playbackRate;
  localStorage.setItem('n5PlaybackRate', String(state.playbackRate));
}
$('#playbackRate').addEventListener('change', event => setPlaybackRate(Number(event.target.value)));
$('#dialogPlaybackRate').addEventListener('change', event => setPlaybackRate(Number(event.target.value)));
$('#voiceSelect').addEventListener('change', () => {
  state.voice = Number($('#voiceSelect').value);
  localStorage.setItem('n5Voice', String(state.voice));
  audio.pause();
  if (state.id) loadAudio();
});
$('#particlePause').addEventListener('change', event => {
  state.particlePause = event.target.checked;
  localStorage.setItem('n5ParticlePause', String(state.particlePause));
  audio.pause();
  if (state.id) loadAudio();
});
document.querySelectorAll('[data-mode]').forEach(button => button.addEventListener('click', () => setMode(button.dataset.mode)));
$('#levelSelect').addEventListener('change', event => setLevel(event.target.value));

let lastStats = null;
function renderStats() {
  if (!lastStats) return;
  const levelStats = lastStats.levels[state.level] || {};
  const listening = levelStats.Listening || {attempts:0,correct_tokens:0,total_tokens:0,needs_practice:[]};
  const writing = levelStats.Writing || {attempts:0,earned_weight:0,possible_weight:0,needs_practice:[]};
  const rate = metric => metric.possible_weight ? `${Math.round(100 * metric.earned_weight / metric.possible_weight)}%` : '—';
  const listeningRate = listening.total_tokens ? `${Math.round(100 * listening.correct_tokens / listening.total_tokens)}%` : '—';
  $('#listeningScore').textContent = listeningRate;
  $('#writingScore').textContent = rate(writing);
  const current = state.mode === 'Writing' ? writing : listening;
  $('#attempts').textContent = current.attempts;
  $('#accuracy').textContent = state.mode === 'Writing' ? rate(writing) : listeningRate;
  const box = $('#weakWords');
  box.replaceChildren();
  const ranked = [...current.needs_practice].filter(word => word.attempts > word.correct)
    .sort((a,b) => (b.attempts - b.correct) - (a.attempts - a.correct) || (a.correct / a.attempts) - (b.correct / b.attempts));
  if (!ranked.length) {
    const empty = document.createElement('div');
    empty.className = 'empty';
    empty.textContent = 'Seu mapa de aprendizagem começa com a primeira resposta com erros.';
    box.append(empty);
    return;
  }
  for (const [index, word] of ranked.slice(0,10).entries()) {
    const row = document.createElement('div'); row.className = 'weak-item';
    const number = document.createElement('span'); number.className = 'rank-number'; number.textContent = String(index + 1).padStart(2,'0');
    const left = document.createElement('div'); left.className = 'rank-word';
    const name = document.createElement('b'); name.textContent = word.surface;
    const reading = document.createElement('small'); reading.textContent = [word.reading !== word.surface ? word.reading : '', word.kind].filter(Boolean).join(' · ');
    left.append(name,reading);
    const score = document.createElement('span'); score.className = 'rank-errors'; score.textContent = `${word.attempts - word.correct} erro${word.attempts - word.correct === 1 ? '' : 's'}`;
    row.append(number,left,score); box.append(row);
  }
}
async function refreshStats() {
  try { lastStats = await api('/api/stats'); renderStats(); }
  catch (error) { console.error(error); }
}

function showResult(data) {
  stopSelectionSpeech();
  state.glossary = data.phrase.tokens || state.glossary;
  state.playStarted = false;
  audio.pause();
  audio.currentTime = 0;
  audioStatus(state.loading ? 'Preparando áudio…' : 'Pronto para ouvir');
  updatePlayButton(false);
  const writing = data.mode === 'Writing';
  const perfect = data.correct === data.total;
  $('#resultBadge').textContent = perfect ? (writing ? 'ESCRITA PRECISA' : 'ESCUTA PRECISA') : 'VAMOS REVISAR';
  $('#resultBadge').classList.toggle('miss',!perfect);
  $('#resultTitle').textContent = perfect ? 'Você acertou!' : 'Quase lá — veja os trechos.';
  $('#scoreLine').textContent = `${data.correct} de ${data.total} ${writing ? 'lacunas corretas · gramática ×1,5 e vocabulário ×1,25' : 'trechos reconhecidos · Listening ×1'}`;
  $('#correctText').textContent = data.phrase.text;
  $('#translation').textContent = data.phrase.translation_pt;
  const grammarNote = $('#grammarNote');
  grammarNote.hidden = !data.phrase.grammar_point;
  grammarNote.textContent = data.phrase.grammar_point
    ? [data.phrase.grammar_point,data.phrase.grammar_explanation_pt].filter(Boolean).join(' · ') : '';
  $('#analysisTitle').textContent = writing ? 'Análise das lacunas' : 'Análise por trecho';
  const box = $('#tokenResults'); box.replaceChildren();
  for (const token of data.results) {
    const row = document.createElement('div'); row.className = `token-row ${token.correct ? '' : 'bad'}`;
    const symbol = document.createElement('span'); symbol.className = 'symbol'; symbol.textContent = token.correct ? '✓' : '×';
    const expected = document.createElement('div');
    const surface = document.createElement('b'); surface.textContent = token.surface;
    const reading = document.createElement('small'); reading.textContent = token.reading;
    expected.append(surface,reading);
    const typed = document.createElement('div'); typed.className = 'typed'; typed.textContent = token.correct ? 'Correto' : `Você escreveu: ${token.typed || '—'}`;
    const meaning = document.createElement('div'); meaning.className = 'meaning';
    meaning.textContent = token.meanings_pt.join(' · ');
    const note = document.createElement('small');
    note.textContent = `${writing ? `${token.category} ×${token.weight} · ` : ''}${token.kind} · ${token.note_pt}`;
    meaning.append(note); row.append(symbol,expected,typed,meaning); box.append(row);
  }
  dialog.showModal();
}

async function submit(event, mode) {
  event.preventDefault();
  if (!state.id || state.mode !== mode) return;
  const button = mode === 'Writing' ? $('#clozeForm .submit') : $('#answerForm .submit');
  const payload = mode === 'Writing'
    ? {exercise_id:state.exerciseId,answers:Object.fromEntries([...document.querySelectorAll('.blank-input')].map(input => [input.dataset.index,input.value.trim()]))}
    : {id:state.id,text:$('#answer').value.trim()};
  button.disabled = true;
  button.textContent = 'Conferindo…';
  try {
    const result = await api(mode === 'Writing' ? '/api/cloze/submit' : '/api/submit',
      {method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(payload)});
    showResult(result);
    refreshStats();
  } catch (error) { alert(error.message); }
  finally {
    button.disabled = false;
    button.innerHTML = `${mode === 'Writing' ? 'Conferir lacunas' : 'Conferir resposta'} <span>→</span>`;
  }
}
$('#answerForm').addEventListener('submit', event => submit(event,'Listening'));
$('#clozeForm').addEventListener('submit', event => submit(event,'Writing'));
$('#answer').addEventListener('keydown', event => {
  if (event.key === 'Enter' && (event.ctrlKey || event.metaKey)) {
    event.preventDefault(); $('#answerForm').requestSubmit();
  }
});
$('#closeDialog').addEventListener('click',() => dialog.close());
$('#nextPhrase').addEventListener('click',() => { dialog.close(); loadPhrase(); });

const reviewDialog = $('#reviewDialog');
const reviewClip = new Audio();
reviewClip.playbackRate = 0.85;
const reviewState = {level:null,cards:[],index:0,flipped:false,timer:null,noteTimer:null,dirty:false,generation:0};

function stopReviewTimer() {
  clearTimeout(reviewState.timer);
  reviewState.generation++;
}

function currentReviewCard() { return reviewState.cards[reviewState.index]; }

async function persistReviewNote() {
  clearTimeout(reviewState.noteTimer);
  if (!reviewState.dirty || !currentReviewCard()) return;
  const card = currentReviewCard();
  const note = $('#reviewNote').value;
  reviewState.dirty = false;
  try {
    await api('/api/review/note',{method:'POST',headers:{'Content-Type':'application/json'},
      body:JSON.stringify({level:reviewState.level,key:card.key,note})});
    card.note = note;
  } catch (error) {
    reviewState.dirty = true;
    throw error;
  }
}

function renderReviewCard() {
  stopReviewTimer();
  reviewClip.pause();
  const card = currentReviewCard();
  $('#reviewTitle').textContent = `Revisão ${reviewState.level}`;
  $('#reviewCard').hidden = !card;
  $('#reviewEmpty').hidden = !!card;
  $('#reviewRemove').disabled = !card;
  $('#reviewNext').disabled = !card;
  $('#reviewCount').textContent = card ? `${reviewState.index + 1} de ${reviewState.cards.length} cartões` : 'Nenhum cartão disponível';
  if (!card) return;
  reviewState.flipped = false;
  reviewState.dirty = false;
  $('#reviewFlip').classList.remove('flipped');
  $('#reviewFront').inert = false;
  $('#reviewBack').inert = true;
  $('#reviewFrontText').textContent = card.text;
  $('#reviewBackText').textContent = card.text;
  $('#reviewReading').textContent = card.reading;
  $('#reviewMeaning').textContent = card.meaning;
  $('#reviewNote').value = card.note || '';
  $('#reviewSource').textContent = card.source.includes('mistakes') ? `${card.errors} erros neste nível` : 'Salvo para revisão';
  if ($('#reviewAuto').checked) scheduleReviewFlip();
}

function playReviewAudio() {
  const card = currentReviewCard();
  if (!card) return;
  const url = `/api/selection-audio?text=${encodeURIComponent(card.text)}&speaker=${state.voice}`;
  reviewClip.pause();
  reviewClip.src = url;
  reviewClip.playbackRate = 0.85;
  reviewClip.play().catch(() => {});
}

function flipReviewCard() {
  if (!currentReviewCard() || reviewState.flipped) return;
  stopReviewTimer();
  reviewState.flipped = true;
  $('#reviewFlip').classList.add('flipped');
  $('#reviewFront').inert = true;
  $('#reviewBack').inert = false;
  playReviewAudio();
  if ($('#reviewAuto').checked) {
    const generation = reviewState.generation;
    reviewState.timer = setTimeout(() => {
      if (generation === reviewState.generation) advanceReviewCard();
    },2000);
  }
}

function scheduleReviewFlip() {
  stopReviewTimer();
  if (!$('#reviewAuto').checked || !currentReviewCard()) return;
  const generation = reviewState.generation;
  reviewState.timer = setTimeout(() => {
    if (generation === reviewState.generation) flipReviewCard();
  },2000);
}

async function advanceReviewCard() {
  stopReviewTimer();
  try { await persistReviewNote(); }
  catch (error) { $('#reviewAuto').checked = false; alert(error.message); return; }
  if (!reviewState.cards.length) return;
  reviewState.index = (reviewState.index + 1) % reviewState.cards.length;
  renderReviewCard();
}

$('#openReview').addEventListener('click',async () => {
  stopSelectionSpeech();
  reviewState.level = state.level;
  $('#openReview').disabled = true;
  try {
    const data = await api(`/api/review?level=${reviewState.level}`);
    reviewState.cards = data.cards;
    reviewState.index = 0;
    $('#reviewAuto').checked = false;
    reviewDialog.showModal();
    renderReviewCard();
  } catch (error) { alert(error.message); }
  finally { $('#openReview').disabled = false; }
});
$('#closeReview').addEventListener('click',() => reviewDialog.close());
reviewDialog.addEventListener('close',() => {
  stopReviewTimer();
  clearTimeout(reviewState.noteTimer);
  reviewClip.pause();
  $('#reviewAuto').checked = false;
  persistReviewNote().catch(error => alert(error.message));
});
$('#reviewFront').addEventListener('click',flipReviewCard);
$('#reviewAudio').addEventListener('click',playReviewAudio);
$('#reviewNext').addEventListener('click',advanceReviewCard);
$('#reviewAuto').addEventListener('change',event => {
  stopReviewTimer();
  if (!event.target.checked) return;
  if (reviewState.flipped) {
    const generation = reviewState.generation;
    reviewState.timer = setTimeout(() => {
      if (generation === reviewState.generation) advanceReviewCard();
    },2000);
  } else scheduleReviewFlip();
});
$('#reviewNote').addEventListener('input',() => {
  reviewState.dirty = true;
  clearTimeout(reviewState.noteTimer);
  reviewState.noteTimer = setTimeout(() => persistReviewNote().catch(error => alert(error.message)),700);
});
$('#reviewRemove').addEventListener('click',async () => {
  const card = currentReviewCard();
  if (!card) return;
  stopReviewTimer();
  $('#reviewRemove').disabled = true;
  try {
    await api('/api/review/remove',{method:'POST',headers:{'Content-Type':'application/json'},
      body:JSON.stringify({level:reviewState.level,key:card.key})});
    clearTimeout(reviewState.noteTimer);
    reviewState.dirty = false;
    reviewState.cards.splice(reviewState.index,1);
    if (reviewState.index >= reviewState.cards.length) reviewState.index = 0;
    renderReviewCard();
  } catch (error) { alert(error.message); $('#reviewRemove').disabled = false; }
});

const selectionReader = {key:'',text:'',timer:null,checkTimer:null,generation:0,saved:false};
const selectionAudio = new Audio();
const japaneseCharacters = /[\u3040-\u30ff\u3400-\u9fff]/;
const normalizeSelection = value => value.normalize('NFKC').replace(/[\s。、！？?!,.・「」『』“”]/g,'');

function stopSelectionSpeech() {
  clearTimeout(selectionReader.timer);
  clearTimeout(selectionReader.checkTimer);
  selectionReader.key = '';
  selectionReader.text = '';
  selectionReader.saved = false;
  selectionReader.generation++;
  if ('speechSynthesis' in window) window.speechSynthesis.cancel();
  selectionAudio.pause();
  selectionAudio.onended = null;
  selectionAudio.onerror = null;
  $('#selectionTooltip').hidden = true;
  $('#dialogSelectionTooltip').hidden = true;
}

function selectedJapanese() {
  const active = document.activeElement;
  if (active && (active.tagName === 'TEXTAREA' || active.tagName === 'INPUT') &&
      typeof active.selectionStart === 'number' && active.selectionEnd > active.selectionStart) {
    return {text:active.value.slice(active.selectionStart,active.selectionEnd),rect:active.getBoundingClientRect()};
  }
  const selection = window.getSelection();
  if (!selection || selection.isCollapsed || !selection.rangeCount) return null;
  return {text:selection.toString(),rect:selection.getRangeAt(0).getBoundingClientRect()};
}

function matchingMeanings(text) {
  const chosen = normalizeSelection(text);
  const tokens = state.glossary || [];
  const whole = tokens.map(token => normalizeSelection(token.surface)).join('');
  const start = whole.indexOf(chosen);
  let matches = [];
  if (start !== -1) {
    let position = 0;
    for (const token of tokens) {
      const end = position + normalizeSelection(token.surface).length;
      if (end > start && position < start + chosen.length) matches.push(token);
      position = end;
    }
  } else {
    matches = tokens.filter(token => {
      const surface = normalizeSelection(token.surface);
      const reading = normalizeSelection(token.reading);
      return surface === chosen || reading === chosen ||
        (chosen.length >= 2 && (surface.includes(chosen) || chosen.includes(surface) || chosen.includes(reading)));
    });
  }
  return [...new Map(matches.map(token => [`${token.surface}|${token.reading}`,token])).values()].slice(0,8);
}

function showSelectionMeaning(text, rect) {
  const tooltip = dialog.open ? $('#dialogSelectionTooltip') : $('#selectionTooltip');
  const other = dialog.open ? $('#selectionTooltip') : $('#dialogSelectionTooltip');
  other.hidden = true;
  tooltip.replaceChildren();
  const title = document.createElement('strong');
  title.className = 'selection-title';
  title.textContent = text.length > 28 ? `${text.slice(0,28)}…` : text;
  tooltip.append(title);
  const matches = matchingMeanings(text);
  if (matches.length) {
    for (const token of matches) {
      const row = document.createElement('div'); row.className = 'selection-definition';
      const word = document.createElement('b'); word.textContent = token.surface;
      const reading = document.createElement('small'); reading.textContent = token.reading !== token.surface ? ` ${token.reading}` : '';
      const meaning = document.createElement('span'); meaning.textContent = (token.meanings_pt || []).join(' · ');
      row.append(word,reading,meaning); tooltip.append(row);
    }
  } else {
    const empty = document.createElement('div'); empty.className = 'selection-definition';
    empty.textContent = 'Sem significado cadastrado para este trecho da frase.';
    tooltip.append(empty);
  }
  const save = document.createElement('button');
  save.type = 'button';
  save.className = 'selection-save';
  save.textContent = selectionReader.saved ? '★ Salvo para revisão' : '☆ Salvar para revisão';
  save.setAttribute('aria-label',`Salvar ${text} para revisão`);
  save.disabled = selectionReader.saved || !state.id || text.length > 100;
  save.addEventListener('pointerdown',event => event.preventDefault());
  save.addEventListener('click',async () => {
    save.disabled = true;
    try {
      await api('/api/review/save',{method:'POST',headers:{'Content-Type':'application/json'},
        body:JSON.stringify({level:state.level,phrase_id:state.id,text})});
      selectionReader.saved = true;
      save.textContent = '★ Salvo para revisão';
    } catch (error) { save.disabled = false; alert(error.message); }
  });
  tooltip.append(save);
  tooltip.hidden = false;
  const bounds = tooltip.getBoundingClientRect();
  tooltip.style.left = `${Math.max(10,Math.min(rect.left,window.innerWidth-bounds.width-10))}px`;
  tooltip.style.top = `${rect.bottom+bounds.height+10 < window.innerHeight ? rect.bottom+8 : Math.max(10,rect.top-bounds.height-8)}px`;
}

function speakSelectedText(generation) {
  if (generation !== selectionReader.generation || !selectionReader.key) return;
  const repeat = () => {
    if (generation === selectionReader.generation && selectionReader.key)
      selectionReader.timer = setTimeout(() => speakSelectedText(generation), 2000);
  };
  const browserVoice = 'speechSynthesis' in window && 'SpeechSynthesisUtterance' in window
    ? window.speechSynthesis.getVoices().find(candidate => /^ja([-_]|$)/i.test(candidate.lang)) : null;
  if (browserVoice) {
    const utterance = new SpeechSynthesisUtterance(selectionReader.text);
    utterance.lang = 'ja-JP';
    utterance.voice = browserVoice;
    utterance.rate = 1;
    utterance.onend = repeat;
    utterance.onerror = () => stopSelectionSpeech();
    window.speechSynthesis.speak(utterance);
    return;
  }
  const url = `/api/selection-audio?text=${encodeURIComponent(selectionReader.text)}&speaker=${state.voice}`;
  if (selectionAudio.getAttribute('src') !== url) selectionAudio.src = url;
  else selectionAudio.currentTime = 0;
  selectionAudio.onended = repeat;
  selectionAudio.onerror = () => stopSelectionSpeech();
  selectionAudio.play().catch(() => { if (generation === selectionReader.generation) stopSelectionSpeech(); });
}

function inspectSelection() {
  if (reviewDialog.open) { stopSelectionSpeech(); return; }
  const selected = selectedJapanese();
  if (!selected || !japaneseCharacters.test(selected.text) || !normalizeSelection(selected.text)) {
    stopSelectionSpeech();
    return;
  }
  const key = `${state.id}|${selected.text}`;
  if (key === selectionReader.key) {
    showSelectionMeaning(selected.text,selected.rect);
    return;
  }
  stopSelectionSpeech();
  selectionReader.key = key;
  selectionReader.text = selected.text.trim();
  const generation = selectionReader.generation;
  if (!audio.paused) audio.pause();
  showSelectionMeaning(selected.text,selected.rect);
  speakSelectedText(generation);
}

function scheduleSelectionInspection() {
  if (reviewDialog.open) return;
  const current = selectedJapanese();
  if (!current || !japaneseCharacters.test(current.text)) { stopSelectionSpeech(); return; }
  clearTimeout(selectionReader.checkTimer);
  selectionReader.checkTimer = setTimeout(inspectSelection,100);
}
document.addEventListener('selectionchange',scheduleSelectionInspection);
document.addEventListener('pointerup',scheduleSelectionInspection);
document.addEventListener('keyup',scheduleSelectionInspection);
window.addEventListener('blur',stopSelectionSpeech);
document.addEventListener('visibilitychange',() => { if (document.hidden) stopSelectionSpeech(); });
dialog.addEventListener('close',stopSelectionSpeech);

async function init() {
  $('#levelSelect').value = state.level;
  $('#levelPill').textContent = `NÍVEL ${state.level}`;
  document.title = `Prática ${state.level} · Supreme Nihongo`;
  if (state.level !== 'N5') $('#heroDescription').textContent = `Uma frase ${state.level} por vez. Ouça quantas vezes precisar e escreva exatamente o que entendeu.`;
  await refreshMetadata();
  await loadVoices();
  refreshStats();
  loadPhrase();
}
init();
