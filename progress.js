    import {saveData, loadData, renderMoqrarat, updateProgress, getMoqrar} from '/firebase.js';
              
  let lastSentProgress = null;
  function getDateFromPath() {
    // Extracts the date from the folder name in the URL (e.g., /pages/10-07-2025/)
    const match = window.location.pathname.match(/pages\/([^\/]+)\//);
    return match ? match[1] : null;
  }
  function saveProgress(progress) {
    const date = getDateFromPath();
    if (!date) return;
    // Only send if progress changed by at least 1%
    if (lastSentProgress !== null && Math.abs(progress - lastSentProgress) < 0.01) return;
    lastSentProgress = progress;
    updateProgress(progress, date);
  }
  function updateProgressBar() {
    const scrollTop = window.scrollY || document.documentElement.scrollTop;
    const docHeight = document.documentElement.scrollHeight - window.innerHeight;
    const progress = docHeight > 0 ? (scrollTop / docHeight) : 0;
    document.getElementById('progress-bar').style.width = (progress * 100) + '%';
    saveProgress(progress);
  }
  function initProgress(){
    const date = getDateFromPath();
    if (!date) return;
    getMoqrar(date).then(moqrar => {
      if (moqrar && moqrar.progress) {
        const progress = parseFloat(moqrar.progress);
        document.getElementById('progress-bar').style.width = (progress * 100) + '%';
        lastSentProgress = progress;
        // Scroll to the saved progress position
        const docHeight = document.documentElement.scrollHeight - window.innerHeight;
        if (docHeight > 0) {
            window.scrollTo(0, progress * docHeight);
        }
      }
    });
  }
  window.addEventListener('scroll', updateProgressBar);
  window.addEventListener('resize', updateProgressBar);
  document.addEventListener('DOMContentLoaded', initProgress);

      // Tooltip update logic
      function updateTooltip(progress) {
        const tooltip = document.getElementById('progress-tooltip');
        tooltip.textContent = Math.round(progress * 100) + '%';
        tooltip.style.left = `calc(${progress * 100}% - 20px)`;
      }
      // Initial value
      updateTooltip(0);
      // Listen for progress bar updates
      function updateTooltipOnScroll() {
        const scrollTop = window.scrollY || document.documentElement.scrollTop;
        const docHeight = document.documentElement.scrollHeight - window.innerHeight;
        const progress = docHeight > 0 ? (scrollTop / docHeight) : 0;
        updateTooltip(progress);
      }
      window.addEventListener('scroll', updateTooltipOnScroll);
      window.addEventListener('resize', updateTooltipOnScroll);
      document.addEventListener('DOMContentLoaded', updateTooltipOnScroll);