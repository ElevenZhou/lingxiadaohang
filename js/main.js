// ===== Claw Navigation - main.js =====

(function () {
  'use strict';

  // ── Set header height CSS variable for sticky category nav ─────────────────
  function updateHeaderHeight() {
    const header = document.querySelector('.site-header');
    if (header) {
      document.documentElement.style.setProperty(
        '--header-height', header.offsetHeight + 'px'
      );
    }
  }
  updateHeaderHeight();
  window.addEventListener('resize', updateHeaderHeight, { passive: true });

  // ── Search ──────────────────────────────────────────────────────────────────
  const searchInput = document.getElementById('search-input');
  const noResults   = document.getElementById('no-results');
  const allCards    = Array.from(document.querySelectorAll('.nav-card'));
  const allSections = Array.from(document.querySelectorAll('.nav-section'));

  function doSearch(query) {
    const q = query.trim().toLowerCase();

    if (!q) {
      // restore everything
      allCards.forEach(c => c.classList.remove('hidden'));
      allSections.forEach(s => s.classList.remove('hidden'));
      noResults.classList.remove('visible');
      resetCatButtons();
      return;
    }

    let visibleCount = 0;
    allCards.forEach(card => {
      const name = (card.dataset.name || '').toLowerCase();
      const desc = (card.dataset.desc || '').toLowerCase();
      const tags = (card.dataset.tags || '').toLowerCase();
      if (name.includes(q) || desc.includes(q) || tags.includes(q)) {
        card.classList.remove('hidden');
        visibleCount++;
      } else {
        card.classList.add('hidden');
      }
    });

    // hide sections that have no visible cards
    allSections.forEach(section => {
      const visible = section.querySelectorAll('.nav-card:not(.hidden)').length;
      section.classList.toggle('hidden', visible === 0);
    });

    noResults.classList.toggle('visible', visibleCount === 0);
  }

  searchInput && searchInput.addEventListener('input', e => doSearch(e.target.value));

  // search on enter key
  searchInput && searchInput.addEventListener('keydown', e => {
    if (e.key === 'Enter') doSearch(e.target.value);
  });

  document.getElementById('search-btn') &&
    document.getElementById('search-btn').addEventListener('click', () => {
      doSearch(searchInput.value);
    });

  // ── Category filter ──────────────────────────────────────────────────────────
  const catButtons = Array.from(document.querySelectorAll('.cat-btn'));

  function resetCatButtons() {
    catButtons.forEach(b => b.classList.remove('active'));
    const allBtn = document.querySelector('.cat-btn[data-cat="all"]');
    allBtn && allBtn.classList.add('active');
    allSections.forEach(s => s.classList.remove('hidden'));
  }

  catButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      const cat = btn.dataset.cat;
      searchInput.value = '';
      allCards.forEach(c => c.classList.remove('hidden'));
      noResults.classList.remove('visible');

      if (cat === 'all') {
        resetCatButtons();
        return;
      }

      catButtons.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');

      allSections.forEach(section => {
        section.classList.toggle('hidden', section.dataset.cat !== cat);
      });
    });
  });

  // ── Favicon error fallback ──────────────────────────────────────────────────
  document.querySelectorAll('.card-icon img').forEach(img => {
    img.addEventListener('error', function () {
      this.classList.add('error');
    });
  });

  // ── Back to top ─────────────────────────────────────────────────────────────
  const backTop = document.getElementById('back-top');
  window.addEventListener('scroll', () => {
    if (backTop) backTop.classList.toggle('visible', window.scrollY > 400);
  }, { passive: true });
  backTop && backTop.addEventListener('click', () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });

  // ── Keyboard shortcut: "/" focuses search ────────────────────────────────────
  document.addEventListener('keydown', e => {
    if (e.key === '/' && document.activeElement !== searchInput) {
      e.preventDefault();
      searchInput && searchInput.focus();
    }
  });
})();
