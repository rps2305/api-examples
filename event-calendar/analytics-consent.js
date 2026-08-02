(() => {
  'use strict';

  const STORAGE_KEY = 'uit-vandaag-analytics-consent-v1';
  const MATOMO_URL = 'https://matomo.puntuale.nl/';
  const MATOMO_SITE_ID = '15';
  let trackerRequested = false;

  function readChoice() {
    try {
      const value = localStorage.getItem(STORAGE_KEY);
      return value === 'granted' || value === 'denied' ? value : '';
    } catch {
      return '';
    }
  }

  function storeChoice(value) {
    try { localStorage.setItem(STORAGE_KEY, value); } catch { /* Keep the choice for this page only. */ }
  }

  function deleteMatomoCookies() {
    document.cookie.split(';').forEach(cookie => {
      const name = cookie.split('=', 1)[0].trim();
      if (name.startsWith('_pk_') || name.startsWith('mtm_') || name === 'matomo_ignore') {
        document.cookie = `${name}=; Max-Age=0; Path=/; SameSite=Lax; Secure`;
      }
    });
  }

  function loadMatomo() {
    if (trackerRequested || readChoice() !== 'granted') return;
    trackerRequested = true;
    const queue = window._paq = window._paq || [];
    queue.push(['requireConsent']);
    queue.push(['setTrackerUrl', `${MATOMO_URL}matomo.php`]);
    queue.push(['setSiteId', MATOMO_SITE_ID]);
    queue.push(['setDoNotTrack', true]);
    queue.push(['setConsentGiven']);
    queue.push(['trackPageView']);
    queue.push(['enableLinkTracking']);

    const script = document.createElement('script');
    script.async = true;
    script.src = `${MATOMO_URL}matomo.js`;
    script.referrerPolicy = 'strict-origin-when-cross-origin';
    document.head.append(script);
  }

  function scheduleMatomo() {
    const start = () => {
      if ('requestIdleCallback' in window) {
        window.requestIdleCallback(loadMatomo, { timeout: 2_000 });
      } else {
        window.setTimeout(loadMatomo, 0);
      }
    };
    if (document.readyState === 'complete') start();
    else window.addEventListener('load', start, { once: true });
  }

  function revokeMatomo() {
    if (window._paq) {
      window._paq.push(['forgetConsentGiven']);
      window._paq.push(['disableCookies']);
      window._paq.push(['deleteCookies']);
    }
    deleteMatomoCookies();
  }

  function createElement(tagName, className, text) {
    const node = document.createElement(tagName);
    if (className) node.className = className;
    if (text !== undefined) node.textContent = text;
    return node;
  }

  function createNotice() {
    const notice = createElement('aside', 'privacy-notice');
    notice.id = 'privacy-notice';
    notice.hidden = true;
    notice.setAttribute('aria-labelledby', 'privacy-notice-title');

    const copy = createElement('p', 'privacy-notice-copy');
    const title = createElement('strong', '', 'Mag deze site gebruik meten?');
    title.id = 'privacy-notice-title';
    copy.append(title, document.createTextNode(' Matomo wordt pas na toestemming geladen en plaatst dan analytische cookies. '));
    const details = createElement('a', '', 'Lees hoe dit werkt');
    details.href = '/disclaimer.html#privacy';
    copy.append(details, document.createTextNode('.'));

    const actions = createElement('div', 'privacy-actions');
    const reject = createElement('button', 'privacy-reject', 'Niet toestaan');
    reject.type = 'button';
    const accept = createElement('button', 'privacy-accept', 'Toestaan');
    accept.type = 'button';
    actions.append(reject, accept);
    notice.append(copy, actions);
    document.body.append(notice);

    const closeWith = choice => {
      storeChoice(choice);
      notice.hidden = true;
      if (choice === 'granted') scheduleMatomo();
      else revokeMatomo();
    };
    reject.addEventListener('click', () => closeWith('denied'));
    accept.addEventListener('click', () => closeWith('granted'));
    return { notice, reject };
  }

  const { notice, reject } = createNotice();
  document.querySelectorAll('[data-privacy-settings]').forEach(button => {
    button.addEventListener('click', () => {
      notice.hidden = false;
      reject.focus();
    });
  });

  if (readChoice() === 'granted') scheduleMatomo();
  else if (!readChoice()) notice.hidden = false;
})();
