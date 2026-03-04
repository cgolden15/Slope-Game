function UnityProgress(gameInstance, progress) {
  if (!gameInstance || !gameInstance.container) return;

  var p = progress === "complete" ? 1 : Math.max(0, Math.min(1, Number(progress) || 0));

  if (!gameInstance.loadingOverlay) {
    var overlay  = document.createElement("div");
    overlay.className = "loading-overlay";

    var card     = document.createElement("div");
    card.className = "loading-card";

    var title    = document.createElement("div");
    title.className = "loading-title";
    title.textContent = "Slope\u2122: Premium Edition";

    var sub      = document.createElement("div");
    sub.className = "loading-subtitle";
    sub.textContent = "Get ready to roll...";

    var track    = document.createElement("div");
    track.className = "loading-track";

    var fill     = document.createElement("div");
    fill.className = "loading-fill";
    track.appendChild(fill);

    var pct      = document.createElement("div");
    pct.className = "loading-percent";
    pct.textContent = "0%";

    card.appendChild(title);
    card.appendChild(sub);
    card.appendChild(track);
    card.appendChild(pct);
    overlay.appendChild(card);
    gameInstance.container.appendChild(overlay);

    gameInstance.loadingOverlay = overlay;
    gameInstance.loadingFill    = fill;
    gameInstance.loadingPercent = pct;
  }

  var pct = Math.round(p * 100);
  gameInstance.loadingFill.style.width   = pct + "%";
  gameInstance.loadingPercent.textContent = pct + "%";

  if (p >= 1) {
    gameInstance.loadingOverlay.classList.add("is-hidden");
    setTimeout(function () {
      if (gameInstance.loadingOverlay) gameInstance.loadingOverlay.style.display = "none";
    }, 300);
  }
}
