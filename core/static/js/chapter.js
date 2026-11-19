document.addEventListener('DOMContentLoaded', () => {
  const textarea = document.querySelector('.notes-section textarea');
  if (!textarea) return;

  let timeout = null;
  textarea.addEventListener('input', () => {
    clearTimeout(timeout);
    timeout = setTimeout(() => {
      const status = document.createElement('div');
      status.textContent = '💡 Remember to click "Save notes"';
      status.style.cssText = 'position:fixed;bottom:20px;right:20px;background:#0b2b26;color:#f5c542;padding:10px 16px;border-radius:20px;font-size:13px;z-index:999;';
      document.body.appendChild(status);
      setTimeout(() => status.remove(), 2500);
    }, 1200);
  });
});