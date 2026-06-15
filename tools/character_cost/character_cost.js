'use strict';

(function () {
  const PLAN_TIERS = [
    { id: 'free', name: 'Free', credits: 10000 },
    { id: 'starter', name: 'Starter', credits: 30000 },
    { id: 'creator', name: 'Creator', credits: 121000 },
    { id: 'pro', name: 'Pro', credits: 600000 },
    { id: 'scale', name: 'Scale', credits: 1800000 },
    { id: 'business', name: 'Business', credits: 6000000 }
  ];

  const COPY = {
    en: {
      charsPerScript: 'Characters / script',
      monthlyChars: 'Monthly characters',
      estimatedCredits: 'Estimated credits',
      estimatedAudio: 'Estimated audio',
      basedOnText: 'Based on pasted text',
      estimatedFromWords: 'Estimated from words',
      scriptsPerMonth: 'scripts / month',
      includesBuffer: 'includes buffer and regenerations',
      minutesPerMonth: 'minutes / month',
      recommendationTitle: 'Plan estimate',
      recommendationFits: 'This workload fits inside the {plan} public monthly credit allowance if your assumptions are accurate.',
      recommendationOver: 'This workload is above the public Business allowance. Treat it as an Enterprise or custom-usage estimate.',
      selectedPlanTitle: 'Selected plan usage',
      selectedPlanText: '{percent}% of {plan} credits used.',
      selectedPlanOver: '{percent}% of {plan} credits used. Raise the plan or lower regenerations/buffer.',
      customPlan: 'custom plan',
      good: 'fits',
      high: 'high',
      over: 'over',
      match: 'match',
      copy: 'Copy summary',
      copied: 'Copied',
      blocked: 'Clipboard blocked',
      summary: 'ElevenLabs character estimate',
      source: 'Source',
      creditsPerMonth: 'credits / month',
      sourceText: 'text sample',
      sourceWords: 'word estimate'
    },
    ko: {
      charsPerScript: '스크립트당 글자 수',
      monthlyChars: '월간 글자 수',
      estimatedCredits: '예상 크레딧',
      estimatedAudio: '예상 오디오',
      basedOnText: '붙여넣은 텍스트 기준',
      estimatedFromWords: '단어 수 기준 추정',
      scriptsPerMonth: '개 / 월',
      includesBuffer: '여유분과 다시 만들기 포함',
      minutesPerMonth: '분 / 월',
      recommendationTitle: '요금제 추정',
      recommendationFits: '현재 가정이 맞다면 이 작업량은 공개된 {plan} 월간 크레딧 한도 안에 들어갑니다.',
      recommendationOver: '이 작업량은 공개된 Business 한도를 넘습니다. Enterprise 또는 맞춤 사용량으로 보세요.',
      selectedPlanTitle: '선택 요금제 사용률',
      selectedPlanText: '{plan} 크레딧의 {percent}%를 사용합니다.',
      selectedPlanOver: '{plan} 크레딧의 {percent}%를 사용합니다. 요금제를 높이거나 다시 만들기/여유분을 줄이세요.',
      customPlan: '맞춤 요금제',
      good: '가능',
      high: '높음',
      over: '초과',
      match: '추천',
      copy: '요약 복사',
      copied: '복사됨',
      blocked: '복사 차단됨',
      summary: 'ElevenLabs 글자 수·크레딧 추정',
      source: '기준',
      creditsPerMonth: '크레딧 / 월',
      sourceText: '텍스트 샘플',
      sourceWords: '단어 수 추정'
    }
  };

  const THEME_KEY = 'voaih_theme';
  const STORAGE_KEY = 'voaih_character_cost_state';
  const locale = document.documentElement.lang && document.documentElement.lang.startsWith('ko') ? 'ko' : 'en';
  const t = COPY[locale];

  const els = {
    text: document.getElementById('scriptText'),
    words: document.getElementById('wordsPerScript'),
    scripts: document.getElementById('scriptsPerMonth'),
    avgChars: document.getElementById('avgCharsPerWord'),
    wpm: document.getElementById('wpm'),
    buffer: document.getElementById('bufferPercent'),
    bufferValue: document.getElementById('bufferValue'),
    generations: document.getElementById('generationMultiplier'),
    creditRate: document.getElementById('creditRate'),
    customCreditRate: document.getElementById('customCreditRate'),
    plan: document.getElementById('planSelect'),
    customPlanCredits: document.getElementById('customPlanCredits'),
    charactersPerScript: document.getElementById('charactersPerScript'),
    monthlyCharacters: document.getElementById('monthlyCharacters'),
    estimatedCredits: document.getElementById('estimatedCredits'),
    estimatedAudio: document.getElementById('estimatedAudio'),
    charactersDetail: document.getElementById('charactersDetail'),
    monthlyDetail: document.getElementById('monthlyDetail'),
    creditsDetail: document.getElementById('creditsDetail'),
    audioDetail: document.getElementById('audioDetail'),
    recommendation: document.getElementById('recommendation'),
    recommendationTitle: document.getElementById('recommendationTitle'),
    recommendationText: document.getElementById('recommendationText'),
    usageFill: document.getElementById('usageFill'),
    planRows: document.getElementById('planRows'),
    copyButton: document.getElementById('copyButton'),
    copyFeedback: document.getElementById('copyFeedback'),
    resetButton: document.getElementById('resetButton'),
    themeToggle: document.getElementById('themeToggle')
  };

  function numberFormat(value, options) {
    return new Intl.NumberFormat(locale === 'ko' ? 'ko-KR' : 'en-US', options).format(value);
  }

  function compact(value) {
    return numberFormat(value, { maximumFractionDigits: value >= 100 ? 0 : 1 });
  }

  function toNumber(el, fallback) {
    const value = Number(el && el.value);
    return Number.isFinite(value) ? value : fallback;
  }

  function countWords(text) {
    const tokens = text.trim().match(/[A-Za-zÀ-ÿ\u3130-\u318F\uAC00-\uD7A3]+(?:['’][A-Za-zÀ-ÿ\u3130-\u318F\uAC00-\uD7A3]+)?|\d+(?:[.,]\d+)?/g);
    return tokens ? tokens.length : 0;
  }

  function estimateCharacters() {
    const text = els.text.value;
    if (text.trim()) {
      return {
        source: 'text',
        words: countWords(text),
        characters: text.length
      };
    }

    const words = Math.max(0, toNumber(els.words, 0));
    const avgChars = Math.max(1, toNumber(els.avgChars, 5));
    const spaces = words > 0 ? Math.max(0, words - 1) : 0;
    return {
      source: 'words',
      words,
      characters: Math.round(words * avgChars + spaces)
    };
  }

  function currentCreditRate() {
    if (els.creditRate.value === 'custom') {
      return Math.max(0.05, toNumber(els.customCreditRate, 1));
    }
    return Math.max(0.05, Number(els.creditRate.value) || 1);
  }

  function selectedPlanCredits() {
    if (els.plan.value === 'custom') {
      return Math.max(1, toNumber(els.customPlanCredits, 100000));
    }
    const plan = PLAN_TIERS.find((tier) => tier.id === els.plan.value) || PLAN_TIERS[0];
    return plan.credits;
  }

  function selectedPlanName() {
    if (els.plan.value === 'custom') return t.customPlan;
    const plan = PLAN_TIERS.find((tier) => tier.id === els.plan.value) || PLAN_TIERS[0];
    return plan.name;
  }

  function recommendPlan(credits) {
    return PLAN_TIERS.find((tier) => credits <= tier.credits) || null;
  }

  function toggleCustomFields() {
    const showRate = els.creditRate.value === 'custom';
    const showPlan = els.plan.value === 'custom';
    els.customCreditRate.closest('.field').style.display = showRate ? 'grid' : 'none';
    els.customPlanCredits.closest('.field').style.display = showPlan ? 'grid' : 'none';
  }

  function renderPlanRows(estimatedCredits, matchPlan) {
    els.planRows.innerHTML = '';
    PLAN_TIERS.forEach((plan) => {
      const row = document.createElement('div');
      const used = estimatedCredits / plan.credits;
      row.className = 'plan-row';
      if (matchPlan && plan.id === matchPlan.id) row.classList.add('is-match');

      const status = used <= 1 ? t.good : t.over;
      const percent = Math.round(used * 100);
      row.innerHTML =
        '<b>' + plan.name + '</b>' +
        '<span>' + compact(plan.credits) + ' ' + t.creditsPerMonth + '</span>' +
        '<span class="status-chip">' + (matchPlan && plan.id === matchPlan.id ? t.match : percent + '% ' + status) + '</span>';
      els.planRows.appendChild(row);
    });
  }

  function resultSnapshot() {
    const perScript = estimateCharacters();
    const scripts = Math.max(0, toNumber(els.scripts, 0));
    const buffer = Math.max(0, toNumber(els.buffer, 0));
    const generations = Math.max(1, toNumber(els.generations, 1));
    const creditRate = currentCreditRate();
    const wpm = Math.max(60, toNumber(els.wpm, 150));

    const monthlyCharacters = Math.round(perScript.characters * scripts);
    const bufferedCharacters = Math.ceil(monthlyCharacters * (1 + buffer / 100));
    const estimatedCredits = Math.ceil(bufferedCharacters * generations * creditRate);
    const minutesPerScript = perScript.words > 0 ? perScript.words / wpm : 0;
    const monthlyMinutes = minutesPerScript * scripts;

    return {
      perScript,
      scripts,
      buffer,
      generations,
      creditRate,
      wpm,
      monthlyCharacters,
      bufferedCharacters,
      estimatedCredits,
      monthlyMinutes,
      matchPlan: recommendPlan(estimatedCredits),
      selectedCredits: selectedPlanCredits(),
      selectedName: selectedPlanName()
    };
  }

  function recalculate() {
    toggleCustomFields();
    const result = resultSnapshot();
    const sourceLabel = result.perScript.source === 'text' ? t.basedOnText : t.estimatedFromWords;

    els.bufferValue.textContent = result.buffer + '%';
    els.charactersPerScript.textContent = compact(result.perScript.characters);
    els.charactersDetail.textContent = sourceLabel + ' · ' + compact(result.perScript.words) + ' words';
    els.monthlyCharacters.textContent = compact(result.monthlyCharacters);
    els.monthlyDetail.textContent = compact(result.scripts) + ' ' + t.scriptsPerMonth;
    els.estimatedCredits.textContent = compact(result.estimatedCredits);
    els.creditsDetail.textContent = t.includesBuffer;
    els.estimatedAudio.textContent = compact(result.monthlyMinutes);
    els.audioDetail.textContent = t.minutesPerMonth + ' @ ' + result.wpm + ' WPM';

    const selectedPercent = result.selectedCredits > 0 ? Math.round((result.estimatedCredits / result.selectedCredits) * 100) : 0;
    els.usageFill.style.width = Math.min(100, selectedPercent) + '%';

    els.recommendation.classList.toggle('warning', !result.matchPlan || selectedPercent > 100);
    if (result.matchPlan) {
      els.recommendationTitle.textContent = t.recommendationTitle + ': ' + result.matchPlan.name;
      els.recommendationText.textContent = t.recommendationFits.replace('{plan}', result.matchPlan.name) + ' ' +
        (selectedPercent > 100
          ? t.selectedPlanOver.replace('{percent}', selectedPercent).replace('{plan}', result.selectedName)
          : t.selectedPlanText.replace('{percent}', selectedPercent).replace('{plan}', result.selectedName));
    } else {
      els.recommendationTitle.textContent = t.recommendationTitle + ': Enterprise';
      els.recommendationText.textContent = t.recommendationOver + ' ' +
        t.selectedPlanOver.replace('{percent}', selectedPercent).replace('{plan}', result.selectedName);
    }

    renderPlanRows(result.estimatedCredits, result.matchPlan);
    persistState();
  }

  function summaryText() {
    const result = resultSnapshot();
    const recommended = result.matchPlan ? result.matchPlan.name : 'Enterprise';
    return [
      t.summary,
      '- ' + t.source + ': ' + (result.perScript.source === 'text' ? t.sourceText : t.sourceWords),
      '- Characters per script: ' + result.perScript.characters,
      '- Scripts per month: ' + result.scripts,
      '- Monthly characters: ' + result.monthlyCharacters,
      '- Buffer: ' + result.buffer + '%',
      '- Generation multiplier: ' + result.generations + 'x',
      '- Credits per character: ' + result.creditRate,
      '- Estimated credits: ' + result.estimatedCredits,
      '- Estimated audio minutes: ' + compact(result.monthlyMinutes),
      '- Estimated plan: ' + recommended
    ].join('\n');
  }

  function persistState() {
    try {
      const payload = {
        text: els.text.value,
        words: els.words.value,
        scripts: els.scripts.value,
        avgChars: els.avgChars.value,
        wpm: els.wpm.value,
        buffer: els.buffer.value,
        generations: els.generations.value,
        creditRate: els.creditRate.value,
        customCreditRate: els.customCreditRate.value,
        plan: els.plan.value,
        customPlanCredits: els.customPlanCredits.value
      };
      localStorage.setItem(STORAGE_KEY, JSON.stringify(payload));
    } catch (err) {
      // Ignore storage errors.
    }
  }

  function hydrateState() {
    try {
      const raw = localStorage.getItem(STORAGE_KEY);
      if (!raw) return;
      const saved = JSON.parse(raw);
      Object.keys(saved).forEach((key) => {
        const map = {
          text: els.text,
          words: els.words,
          scripts: els.scripts,
          avgChars: els.avgChars,
          wpm: els.wpm,
          buffer: els.buffer,
          generations: els.generations,
          creditRate: els.creditRate,
          customCreditRate: els.customCreditRate,
          plan: els.plan,
          customPlanCredits: els.customPlanCredits
        };
        if (map[key] && typeof saved[key] === 'string') {
          map[key].value = saved[key];
        }
      });
    } catch (err) {
      // Ignore storage errors.
    }
  }

  function resetDefaults() {
    els.text.value = '';
    els.words.value = '150';
    els.scripts.value = '20';
    els.avgChars.value = '5';
    els.wpm.value = '150';
    els.buffer.value = '15';
    els.generations.value = '1.25';
    els.creditRate.value = '1';
    els.customCreditRate.value = '1';
    els.plan.value = 'creator';
    els.customPlanCredits.value = '100000';
    recalculate();
  }

  function applyTheme(theme) {
    const isLight = theme === 'light';
    document.body.classList.toggle('theme-dark', !isLight);
    if (els.themeToggle) {
      els.themeToggle.textContent = isLight ? '🌙' : '☀️';
      const label = isLight
        ? (locale === 'ko' ? '어두운 테마' : 'Dark theme')
        : (locale === 'ko' ? '밝은 테마' : 'Light theme');
      els.themeToggle.setAttribute('aria-label', label);
      els.themeToggle.title = label;
      els.themeToggle.setAttribute('aria-pressed', isLight ? 'true' : 'false');
    }
    try {
      localStorage.setItem(THEME_KEY, isLight ? 'light' : 'dark');
    } catch (err) {
      // Ignore storage errors.
    }
  }

  function hydrateTheme() {
    try {
      const saved = localStorage.getItem(THEME_KEY);
      if (saved === 'light' || saved === 'dark') {
        applyTheme(saved);
        return;
      }
    } catch (err) {
      // Ignore storage errors.
    }
    applyTheme('light');
  }

  function attachEvents() {
    [
      els.text,
      els.words,
      els.scripts,
      els.avgChars,
      els.wpm,
      els.buffer,
      els.generations,
      els.creditRate,
      els.customCreditRate,
      els.plan,
      els.customPlanCredits
    ].forEach((el) => {
      el.addEventListener('input', recalculate);
      el.addEventListener('change', recalculate);
    });

    els.copyButton.addEventListener('click', function () {
      if (!navigator.clipboard || !navigator.clipboard.writeText) {
        els.copyFeedback.textContent = t.blocked;
        setTimeout(function () {
          els.copyFeedback.textContent = '';
        }, 1600);
        return;
      }
      navigator.clipboard.writeText(summaryText()).then(
        function () {
          els.copyFeedback.textContent = t.copied;
          setTimeout(function () {
            els.copyFeedback.textContent = '';
          }, 1400);
        },
        function () {
          els.copyFeedback.textContent = t.blocked;
          setTimeout(function () {
            els.copyFeedback.textContent = '';
          }, 1600);
        }
      );
    });

    els.resetButton.addEventListener('click', resetDefaults);

    if (els.themeToggle) {
      els.themeToggle.addEventListener('click', function () {
        const nextTheme = document.body.classList.contains('theme-dark') ? 'light' : 'dark';
        applyTheme(nextTheme);
      });
    }
  }

  hydrateTheme();
  hydrateState();
  attachEvents();
  recalculate();
})();
