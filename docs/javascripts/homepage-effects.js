(() => {
  'use strict';

  const resolveSiteRoot = () => {
    const logo = document.querySelector('.md-header__button.md-logo');
    return logo ? new URL(logo.href, document.baseURI) : new URL('./', document.baseURI);
  };

  document.addEventListener('click', (event) => {
    const trigger = event.target.closest?.('[data-dsg-search]');
    if (!trigger) return;

    event.preventDefault();
    event.stopImmediatePropagation();

    const destination = new URL('documentation/#enterprise-search-center', resolveSiteRoot());
    window.location.assign(destination.href);
  }, true);

  document.addEventListener('DOMContentLoaded', () => {
    const counters = document.querySelectorAll('.dsg-counter');

    if (!counters.length || window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
      counters.forEach((counter) => {
        const value = Number(counter.dataset.value || 0);
        const decimals = Number(counter.dataset.decimals || 0);
        const suffix = counter.dataset.suffix || '';
        counter.textContent = value.toLocaleString('it-IT', {
          minimumFractionDigits: decimals,
          maximumFractionDigits: decimals
        }) + suffix;
      });
      return;
    }

    const animate = (counter) => {
      const target = Number(counter.dataset.value || 0);
      const decimals = Number(counter.dataset.decimals || 0);
      const suffix = counter.dataset.suffix || '';
      const duration = 900;
      const start = performance.now();

      const frame = (now) => {
        const progress = Math.min((now - start) / duration, 1);
        const eased = 1 - Math.pow(1 - progress, 3);
        const current = target * eased;

        counter.textContent = current.toLocaleString('it-IT', {
          minimumFractionDigits: decimals,
          maximumFractionDigits: decimals
        }) + suffix;

        if (progress < 1) requestAnimationFrame(frame);
      };

      requestAnimationFrame(frame);
    };

    const observer = new IntersectionObserver((entries, obs) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          animate(entry.target);
          obs.unobserve(entry.target);
        }
      });
    }, { threshold: 0.35 });

    counters.forEach((counter) => observer.observe(counter));
  });
})();
