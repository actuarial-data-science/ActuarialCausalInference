document.addEventListener('DOMContentLoaded', function () {
  const observer = new MutationObserver(function () {
    // Handle button text replacements more directly
    document.querySelectorAll('button.thebe-button').forEach(el => {
      const text = el.textContent?.trim();
      const title = el.title?.trim();

      if (!el.hasAttribute('data-i18n-processed')) {
        if (text === "run") {
          el.textContent = thebeRun;
          el.title = thebeRunCell;
          el.setAttribute('data-i18n-processed', 'run');
        }
        if (text === "run all") {
          el.textContent = thebeRunAll;
          el.title = thebeRunAllCells;
          el.setAttribute('data-i18n-processed', 'run-all');
        }
        if (text === "restart & run all") {
          el.textContent = thebeRestartRun;
          el.title = thebeRestartRunCells;
          el.setAttribute('data-i18n-processed', 'restart-run-all');
        }
      }
    });
    document.querySelectorAll('button.btn-launch-thebe').forEach(el => {
      const text = el.textContent?.trim();
      if (!el.hasAttribute('data-i18n-processed')) {
        if (text === "Live Code") {
          el.innerHTML = el.innerHTML.replace("Live Code", thebeLiveCode);
          el.setAttribute('data-i18n-processed', 'live-code');
        }
      }
    });
    document.querySelectorAll('div.tooltip').forEach(el => {
      const text = el.textContent?.trim();
      if (!el.hasAttribute('data-i18n-processed')) {
        if (text === "Launch Thebe") {
          el.innerHTML = el.innerHTML.replace("Launch Thebe", thebeLaunchThebe);
          el.setAttribute('data-i18n-processed', 'launch-thebe');
        }
      }
    });
  });

  // Initial scan
  observer.observe(document.body, { childList: true, subtree: true, characterData: true });

  // Also run immediately for any existing content
  setTimeout(() => {
    const event = new Event('DOMContentLoaded');
    observer.takeRecords();
  }, 100);
});