document.addEventListener('DOMContentLoaded', () => {
  const toggle = document.querySelector('.menu-toggle');
  const nav = document.querySelector('.main-nav');
  if (toggle && nav) {
    toggle.addEventListener('click', () => {
      nav.classList.toggle('open');
    });
  }

  document.querySelectorAll('.message').forEach((msg, i) => {
    setTimeout(() => {
      msg.style.transition = 'opacity .4s';
      msg.style.opacity = '0';
    }, 4000 + i * 500);
    setTimeout(() => msg.remove(), 5000 + i * 500);
  });

  if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('/static/js/sw.js').catch(() => {});
  }
});