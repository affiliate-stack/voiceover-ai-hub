'use strict';

(function () {
  const GA_ID = 'G-5V3WHH6K6E';
  const CONSENT_KEY = 'voaih-consent-v1';
  const defaultConsent = { analytics: false };
  let gaLoaded = false;

  const win = window;
  win.dataLayer = win.dataLayer || [];
  function gtag() {
    win.dataLayer.push(arguments);
  }
  win.gtag = win.gtag || gtag;

  gtag('consent', 'default', {
    ad_storage: 'denied',
    analytics_storage: 'denied',
    wait_for_update: true
  });

  function loadGA() {
    if (gaLoaded || !GA_ID) return;
    const script = document.createElement('script');
    script.async = true;
    script.src = `https://www.googletagmanager.com/gtag/js?id=${GA_ID}`;
    script.onload = function () {
      gtag('js', new Date());
      gtag('config', GA_ID, { anonymize_ip: true });
    };
    document.head.appendChild(script);
    gaLoaded = true;
  }

  function safeStorage(action, value) {
    try {
      if (action === 'get') {
        return localStorage.getItem(CONSENT_KEY);
      }
      if (action === 'set') {
        localStorage.setItem(CONSENT_KEY, value);
      }
      if (action === 'remove') {
        localStorage.removeItem(CONSENT_KEY);
      }
    } catch (err) {
      return null;
    }
    return null;
  }

  function parseConsent() {
    const stored = safeStorage('get');
    if (!stored) return null;
    try {
      const parsed = JSON.parse(stored);
      if (typeof parsed.analytics === 'boolean') {
        return parsed;
      }
      return null;
    } catch (err) {
      return null;
    }
  }

  function applyConsent(consent) {
    const decision = consent && typeof consent.analytics === 'boolean' ? consent : defaultConsent;
    const analyticsGranted = !!decision.analytics;
    gtag('consent', 'update', {
      ad_storage: 'denied',
      analytics_storage: analyticsGranted ? 'granted' : 'denied'
    });
    if (analyticsGranted) {
      loadGA();
    }
  }

  function persistConsent(consent) {
    safeStorage('set', JSON.stringify(consent));
    applyConsent(consent);
  }

  function initConsentBanner() {
    const banner = document.querySelector('[data-consent-banner]');
    const openers = document.querySelectorAll('[data-consent-open]');
    const existing = parseConsent();

    if (!banner) {
      applyConsent(existing || defaultConsent);
      return;
    }

    const toggle = banner.querySelector('[data-consent-toggle]');
    const acceptBtn = banner.querySelector('[data-consent-accept]');
    const rejectBtn = banner.querySelector('[data-consent-reject]');
    const saveBtn = banner.querySelector('[data-consent-save]');
    const closeBtn = banner.querySelector('[data-consent-close]');

    function hideBanner() {
      banner.hidden = true;
      banner.setAttribute('aria-hidden', 'true');
    }
    function showBanner() {
      banner.hidden = false;
      banner.setAttribute('aria-hidden', 'false');
    }
    function syncToggle(value) {
      if (toggle) {
        toggle.checked = !!value;
      }
    }
    function currentConsent() {
      return parseConsent() || defaultConsent;
    }
    function saveAndClose(value) {
      const consent = { analytics: value };
      persistConsent(consent);
      syncToggle(consent.analytics);
      hideBanner();
    }

    if (existing) {
      syncToggle(existing.analytics);
      applyConsent(existing);
      hideBanner();
    } else {
      showBanner();
    }

    acceptBtn?.addEventListener('click', () => saveAndClose(true));
    rejectBtn?.addEventListener('click', () => saveAndClose(false));
    saveBtn?.addEventListener('click', () => {
      const value = toggle ? !!toggle.checked : false;
      saveAndClose(value);
    });
    closeBtn?.addEventListener('click', hideBanner);

    openers.forEach((el) => {
      el.addEventListener('click', (event) => {
        event.preventDefault();
        syncToggle(currentConsent().analytics);
        showBanner();
      });
    });
  }

  document.addEventListener('DOMContentLoaded', initConsentBanner);
})();
