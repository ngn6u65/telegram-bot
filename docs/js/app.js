const TELEGRAM_ICON = `<svg viewBox="0 0 24 24" fill="currentColor"><path d="M11.944 0A12 12 0 0 0 0 12a12 12 0 0 0 12 12 12 12 0 0 0 12-12A12 12 0 0 0 12 0a12 12 0 0 0-.056 0zm4.962 7.224c.1-.002.321.023.465.14a.506.506 0 0 1 .171.325c.016.093.036.306.02.472-.18 1.898-.962 6.502-1.36 8.627-.168.9-.499 1.201-.82 1.23-.696.065-1.225-.46-1.9-.902-1.056-.693-1.653-1.124-2.678-1.8-1.185-.78-.417-1.21.258-1.91.177-.184 3.247-2.977 3.307-3.23.007-.032.014-.15-.056-.212s-.174-.041-.249-.024c-.106.024-1.793 1.14-5.061 3.345-.48.33-.913.49-1.302.48-.428-.008-1.252-.241-1.865-.44-.752-.245-1.349-.374-1.297-.789.027-.216.325-.437.893-.663 3.498-1.524 5.83-2.529 6.998-3.014 3.332-1.386 4.025-1.627 4.476-1.635z"/></svg>`;

document.addEventListener('DOMContentLoaded', () => {
  loadData();
  trackVisitor();

  const menuToggle = document.querySelector('.menu-toggle');
  const navLinks = document.querySelector('.nav-links');
  if (menuToggle && navLinks) {
    menuToggle.addEventListener('click', () => {
      navLinks.classList.toggle('open');
    });
  }
});

async function loadData() {
  try {
    const res = await fetch('data.json?' + Date.now());
    const data = await res.json();

    document.getElementById('site-title').textContent = data.site.title;
    document.getElementById('site-description').textContent = data.site.description;
    document.title = data.site.title;

    const activeBots = data.bots.filter(b => b.is_active);
    const activeChannels = data.channels.filter(c => c.is_active);

    document.getElementById('stat-bots').textContent = activeBots.length;
    document.getElementById('stat-channels').textContent = activeChannels.length;
    document.getElementById('bots-count').textContent = activeBots.length;
    document.getElementById('channels-count').textContent = activeChannels.length;

    renderCards('bots-grid', activeBots, 'bot');
    renderCards('channels-grid', activeChannels, 'channel');
  } catch (err) {
    console.error('Failed to load data:', err);
  }
}

function renderCards(containerId, items, type) {
  const container = document.getElementById(containerId);
  if (!items.length) {
    container.innerHTML = `
      <div class="empty-state">
        <div class="icon">${type === 'bot' ? '🤖' : '📢'}</div>
        <p>No ${type === 'bot' ? 'bots' : 'channels'} added yet</p>
      </div>`;
    return;
  }

  container.innerHTML = items.map((item, i) => `
    <div class="card fade-in" style="animation-delay: ${i * 0.1}s">
      <div class="card-header">
        <div class="card-icon">${item.icon || (type === 'bot' ? '🤖' : '📢')}</div>
        <div class="card-info">
          <div class="card-name">${escapeHtml(item.name)}</div>
          <div class="card-username">@${escapeHtml(item.username)}</div>
          <div class="card-status active">
            <span class="dot" style="width:6px;height:6px;background:var(--success);border-radius:50%;display:inline-block;"></span>
            Active
          </div>
        </div>
      </div>
      ${item.category ? `<span class="card-category">${escapeHtml(item.category)}</span>` : ''}
      <p class="card-description">${escapeHtml(item.description)}</p>
      <a href="https://t.me/${encodeURIComponent(item.username)}" target="_blank" rel="noopener" class="card-action">
        ${TELEGRAM_ICON}
        Open in Telegram
      </a>
    </div>
  `).join('');
}

function escapeHtml(text) {
  const div = document.createElement('div');
  div.textContent = text;
  return div.innerHTML;
}

function trackVisitor() {
  const STORAGE_KEY = 'tghub_visitors';
  const SESSION_KEY = 'tghub_session';

  let visitors = parseInt(localStorage.getItem(STORAGE_KEY) || '0');

  if (!sessionStorage.getItem(SESSION_KEY)) {
    visitors++;
    localStorage.setItem(STORAGE_KEY, visitors.toString());
    sessionStorage.setItem(SESSION_KEY, '1');
  }

  const counterEl = document.getElementById('visitor-count');
  if (counterEl) {
    animateCounter(counterEl, visitors);
  }
}

function animateCounter(el, target) {
  let current = 0;
  const duration = 1200;
  const step = Math.max(1, Math.floor(target / (duration / 16)));
  const timer = setInterval(() => {
    current += step;
    if (current >= target) {
      current = target;
      clearInterval(timer);
    }
    el.textContent = current.toLocaleString();
  }, 16);
}
