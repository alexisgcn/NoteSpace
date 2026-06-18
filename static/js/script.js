// script.js

// THEME TOGGLE (suave)
const themeToggle = document.getElementById('theme-toggle');
const html = document.documentElement;

function setTheme(t) {
  if (t === 'dark') {
    html.setAttribute('data-theme', 'dark');
    themeToggle.textContent = '☀️';
  } else {
    html.setAttribute('data-theme', 'light');
    themeToggle.textContent = '🌙';
  }
  localStorage.setItem('theme', t);
}

const saved = localStorage.getItem('theme') || (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
setTheme(saved);

if (themeToggle) {
  themeToggle.addEventListener('click', () => {
    const current = html.getAttribute('data-theme') === 'dark' ? 'dark' : 'light';
    setTheme(current === 'dark' ? 'light' : 'dark');
  });
}

// FADE-IN ON SCROLL
document.addEventListener('DOMContentLoaded', () => {
  const items = document.querySelectorAll('.fade-in');
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.15 });

  items.forEach(item => observer.observe(item));
});
/* Ripple effect for buttons with class .btn-ripple */
(function () {
  document.addEventListener('click', function (e) {
    const btn = e.target.closest('.btn-ripple');
    if (!btn) return;

    // create ripple element
    const rect = btn.getBoundingClientRect();
    const ripple = document.createElement('span');
    ripple.className = 'ripple';
    // size: make it cover the button
    const size = Math.max(rect.width, rect.height) * 1.2;
    ripple.style.width = ripple.style.height = size + 'px';
    // position: center on click
    const left = e.clientX - rect.left - size / 2;
    const top = e.clientY - rect.top - size / 2;
    ripple.style.left = left + 'px';
    ripple.style.top = top + 'px';

    // append and remove after animation
    btn.appendChild(ripple);
    setTimeout(() => {
      ripple.remove();
    }, 700);
  });
})();
document.addEventListener("scroll", () => {
  document.querySelectorAll(".fade-in").forEach(el => {
    const rect = el.getBoundingClientRect();
    if (rect.top < window.innerHeight - 50) {
      el.classList.add("visible");
    }
  });
});
// Ripple for feature cards
document.querySelectorAll(".feature-card").forEach(card => {
  card.addEventListener("click", e => {
    const rect = card.getBoundingClientRect();
    card.style.setProperty("--x", `${e.clientX - rect.left}px`);
    card.style.setProperty("--y", `${e.clientY - rect.top}px`);
  });
});
