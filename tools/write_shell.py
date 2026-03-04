#!/usr/bin/env python3
"""Write index.html, style.css, and UnityProgress.js with the React-matching design."""
import pathlib, textwrap

ROOT = pathlib.Path(__file__).resolve().parents[1]

# ─────────────────────────────────────────────────────────────────────────────
#  index.html
# ─────────────────────────────────────────────────────────────────────────────
(ROOT / "index.html").write_text(textwrap.dedent("""\
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <title>Slope\u2122: Premium Edition</title>
  <link rel="stylesheet" href="TemplateData/style.css">
  <script src="TemplateData/UnityProgress.js"></script>
  <script src="TemplateData/unityloader41.js"></script>
</head>
<body>

  <!-- background layers -->
  <div class="bg-dots"></div>
  <div class="bg-grid"></div>
  <div class="bg-vignette"></div>
  <div class="laser laser-top"></div>
  <div class="laser laser-bottom"></div>

  <!-- shared SVG gradient defs -->
  <svg class="svg-defs" aria-hidden="true">
    <defs>
      <linearGradient id="metalBase" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0%"   stop-color="#475569"/>
        <stop offset="30%"  stop-color="#334155"/>
        <stop offset="100%" stop-color="#1e293b"/>
      </linearGradient>
      <linearGradient id="metalEdge" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0%"   stop-color="#cbd5e1"/>
        <stop offset="50%"  stop-color="#94a3b8"/>
        <stop offset="100%" stop-color="#64748b"/>
      </linearGradient>
    </defs>
  </svg>

  <!-- game canvas fills entire viewport; everything else overlays it -->
  <div id="gameContainer"></div>

  <!-- top-left: Guest trapezoid panel -->
  <div class="panel-guest">
    <svg class="panel-svg" viewBox="0 0 256 64" preserveAspectRatio="none" aria-hidden="true">
      <path d="M 0 0 L 256 0 L 220 64 L 0 64 Z"
            fill="url(#metalBase)" stroke="url(#metalEdge)"
            stroke-width="3" vector-effect="non-scaling-stroke"/>
    </svg>
    <div class="panel-guest-inner">
      <div class="guest-icon">
        <svg width="22" height="22" viewBox="0 0 24 24" fill="none"
             stroke="#94a3b8" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
          <circle cx="12" cy="8" r="4"/>
          <path d="M4 20c0-4 3.6-7 8-7s8 3 8 7"/>
        </svg>
      </div>
      <span class="guest-label">GUEST</span>
    </div>
  </div>

  <!-- top-right: Fullscreen trapezoid panel -->
  <button class="panel-fullscreen" id="fsBtn" aria-label="Enter fullscreen">
    <svg class="panel-svg" viewBox="0 0 192 48" preserveAspectRatio="none" aria-hidden="true">
      <path d="M 192 0 L 0 0 L 24 48 L 192 48 Z"
            fill="url(#metalBase)" stroke="url(#metalEdge)"
            stroke-width="3" vector-effect="non-scaling-stroke"/>
    </svg>
    <div class="panel-fs-inner">
      <svg width="15" height="15" viewBox="0 0 24 24" fill="none"
           stroke="#cbd5e1" stroke-width="2" stroke-linecap="round">
        <path d="M8 3H5a2 2 0 00-2 2v3m18 0V5a2 2 0 00-2-2h-3m0 18h3a2 2 0 002-2v-3M3 16v3a2 2 0 002 2h3"/>
      </svg>
      <span id="fsLabel">Fullscreen</span>
    </div>
  </button>

  <!-- bottom metallic shelf -->
  <div class="bottom-shelf">
    <svg class="shelf-svg" viewBox="0 0 1000 88" preserveAspectRatio="none" aria-hidden="true">
      <path d="M 0 35 L 300 35 L 320 65 L 680 65 L 700 35 L 1000 35 L 1000 88 L 0 88 Z"
            fill="url(#metalBase)" stroke="url(#metalEdge)"
            stroke-width="2.5" vector-effect="non-scaling-stroke"/>
      <path d="M 0 38 L 298 38 L 318 68 L 682 68 L 702 38 L 1000 38"
            fill="none" stroke="#1e293b" stroke-width="3"
            vector-effect="non-scaling-stroke" opacity="0.6"/>
    </svg>
    <div class="shelf-content">
      <div class="shelf-left">
        <button class="glass-btn">Feedback</button>
      </div>
      <div class="shelf-center">
        <button class="glass-btn">Download</button>
      </div>
      <div class="shelf-right">
        <span class="more-games-label">More Games</span>
        <svg width="22" height="22" viewBox="0 0 24 24" style="filter:drop-shadow(0 0 6px rgba(255,255,255,0.55))">
          <path d="M12 2 L14.5 9.5 L22 12 L14.5 14.5 L12 22 L9.5 14.5 L2 12 L9.5 9.5 Z" fill="#e2e8f0"/>
        </svg>
      </div>
    </div>
  </div>

  <script>
    var gameInstance = UnityLoader.instantiate("gameContainer", "Build/slope.json", {
      onProgress: UnityProgress,
      Module: { onRuntimeInitialized: function () { UnityProgress(gameInstance, "complete"); } }
    });
    (function () {
      var btn = document.getElementById("fsBtn");
      var lbl = document.getElementById("fsLabel");
      var gc  = document.getElementById("gameContainer");
      function upd() {
        var fs = !!document.fullscreenElement;
        lbl.textContent = fs ? "Exit Fullscreen" : "Fullscreen";
        btn.setAttribute("aria-label", fs ? "Exit fullscreen" : "Enter fullscreen");
      }
      btn.addEventListener("click", function () {
        if (!document.fullscreenElement) { gc.requestFullscreen && gc.requestFullscreen(); }
        else { document.exitFullscreen && document.exitFullscreen(); }
      });
      document.addEventListener("fullscreenchange", upd);
      upd();
    }());
  </script>
</body>
</html>
"""), encoding="utf-8")
print("index.html OK")

# ─────────────────────────────────────────────────────────────────────────────
#  style.css
# ─────────────────────────────────────────────────────────────────────────────
(ROOT / "TemplateData" / "style.css").write_text(textwrap.dedent("""\
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;600;700;900&display=swap');

/* ── Reset & base ────────────────────────────────────────────────────────── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body {
  width: 100%; height: 100%;
  overflow: hidden;
  background: #0a1118;
  color: #fff;
  font-family: Orbitron, 'Arial Black', Arial, sans-serif;
  user-select: none;
}

/* ── Game canvas ─────────────────────────────────────────────────────────── */
#gameContainer {
  position: fixed;
  inset: 0;
  width: 100%; height: 100%;
  background: #0a1118;
}
#gameContainer canvas {
  width: 100% !important;
  height: 100% !important;
  display: block;
}

/* ── Background layers (overlaid on game during loading, visible around canvas) */
.bg-dots, .bg-grid, .bg-vignette, .laser { position: fixed; inset: 0; pointer-events: none; z-index: 1; }

.bg-dots {
  opacity: 0.40;
  background-image: radial-gradient(rgba(255,255,255,0.15) 1px, transparent 1px);
  background-size: 4px 4px;
}

.bg-grid {
  opacity: 0.60;
  background-image:
    linear-gradient(rgba(34,197,94,0.20) 1px, transparent 1px),
    linear-gradient(90deg, rgba(34,197,94,0.20) 1px, transparent 1px);
  background-size: 60px 60px;
  background-position: center center;
}

.bg-vignette {
  background: radial-gradient(circle at center, transparent 20%, #05090e 100%);
}

.laser {
  inset: auto 0;
  height: 2px;
  background: #dcfce7;
  box-shadow: 0 0 15px 4px #22c55e, 0 0 40px 10px #16a34a;
  opacity: 0.80;
}
.laser-top    { top: 30%; }
.laser-bottom { top: 70%; }

/* ── SVG defs (hidden) ───────────────────────────────────────────────────── */
.svg-defs { position: absolute; width: 0; height: 0; overflow: hidden; }

/* ── Top-left Guest panel ────────────────────────────────────────────────── */
.panel-guest {
  position: fixed;
  top: 0; left: 0;
  width: 256px; height: 64px;
  z-index: 30;
  cursor: pointer;
  filter: drop-shadow(0 5px 15px rgba(0,0,0,0.5));
}
.panel-svg { position: absolute; inset: 0; width: 100%; height: 100%; }
.panel-guest-inner {
  position: absolute;
  inset: 0;
  display: flex;
  align-items: center;
  padding: 0 20px;
  gap: 12px;
}
.guest-icon {
  background: linear-gradient(to bottom, #475569, #1e293b);
  padding: 7px;
  border-radius: 50%;
  border: 1px solid #64748b;
  box-shadow: inset 0 2px 4px rgba(0,0,0,0.8);
  display: flex;
  align-items: center;
  justify-content: center;
}
.guest-label {
  font-family: Orbitron, 'Arial Black', Arial, sans-serif;
  font-size: 1rem;
  font-weight: 700;
  letter-spacing: 0.15em;
  color: #fff;
  text-shadow: 0 2px 2px rgba(0,0,0,0.8);
}

/* ── Top-right Fullscreen panel ──────────────────────────────────────────── */
.panel-fullscreen {
  position: fixed;
  top: 0; right: 0;
  width: 192px; height: 48px;
  z-index: 30;
  background: none;
  border: none;
  cursor: pointer;
  filter: drop-shadow(0 5px 15px rgba(0,0,0,0.5));
}
.panel-fs-inner {
  position: absolute;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  padding-left: 16px;
  gap: 8px;
}
.panel-fs-inner span {
  font-family: Orbitron, 'Arial Black', Arial, sans-serif;
  font-size: 0.75rem;
  font-weight: 700;
  letter-spacing: 0.08em;
  color: #fff;
  text-shadow: 0 1px 2px rgba(0,0,0,0.8);
}

/* ── Glass neon button (used in bottom shelf) ────────────────────────────── */
.glass-btn {
  position: relative;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border: 2px solid #a3ffb3;
  border-radius: 999px;
  overflow: hidden;
  padding: 0 28px;
  height: 36px;
  color: #fff;
  font-family: Orbitron, 'Arial Black', Arial, sans-serif;
  font-size: 0.72rem;
  font-weight: 800;
  letter-spacing: 0.10em;
  text-transform: uppercase;
  cursor: pointer;
  background: none;
  transition: transform 0.1s ease, box-shadow 0.15s ease;
}
.glass-btn::before {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(to bottom, #32b53a, #0d5916, #147a21);
  box-shadow: inset 0 -6px 15px rgba(0,0,0,0.6), inset 0 0 10px rgba(34,197,94,0.5);
}
.glass-btn::after {
  content: '';
  position: absolute;
  top: 2%; left: 3%; right: 3%;
  height: 40%;
  background: linear-gradient(to bottom, rgba(255,255,255,0.50), rgba(255,255,255,0.05));
  border-radius: 999px 999px 200px 200px;
}
.glass-btn span, .glass-btn { isolation: isolate; }
.glass-btn:active { transform: scale(0.98); }
.glass-btn:hover { box-shadow: 0 0 20px rgba(74,222,128,0.5); }

/* ── Bottom metallic shelf ───────────────────────────────────────────────── */
.bottom-shelf {
  position: fixed;
  bottom: 0; left: 0;
  width: 100%; height: 88px;
  z-index: 30;
  pointer-events: none;
}
.shelf-svg {
  position: absolute;
  bottom: 0;
  width: 100%; height: 100%;
  filter: drop-shadow(0 -10px 20px rgba(0,0,0,0.8));
  pointer-events: auto;
}
.shelf-content {
  position: absolute;
  inset: 0;
  display: flex;
  align-items: flex-end;
  pointer-events: none;
}
.shelf-left, .shelf-center, .shelf-right {
  pointer-events: auto;
  display: flex;
  align-items: flex-end;
  padding-bottom: 12px;
}
.shelf-left   { flex: 1; justify-content: flex-start; padding-left:  32px; }
.shelf-center { width: 400px; justify-content: center; }
.shelf-right  { flex: 1; justify-content: flex-end;   padding-right: 32px; gap: 10px; align-items: center; }

.more-games-label {
  font-family: Orbitron, 'Arial Black', Arial, sans-serif;
  font-size: 0.82rem;
  font-weight: 700;
  letter-spacing: 0.10em;
  color: #fff;
  text-shadow: 0 2px 2px rgba(0,0,0,0.8);
  cursor: pointer;
}

/* ── Loading overlay ─────────────────────────────────────────────────────── */
.loading-overlay {
  position: fixed;
  inset: 0;
  z-index: 50;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: opacity 280ms ease;
  /* same layered background as body */
  background: #0a1118;
}
.loading-overlay.is-hidden { opacity: 0; pointer-events: none; }

.loading-card {
  width: min(380px, 88vw);
  border: 2px solid #a3ffb3;
  border-radius: 8px;
  padding: 28px 24px;
  background: rgba(5, 9, 14, 0.96);
  box-shadow: 0 0 30px rgba(34,197,94,0.35), 0 0 60px rgba(34,197,94,0.12), inset 0 0 40px rgba(0,40,0,0.5);
}

.loading-title {
  font-family: Orbitron, 'Arial Black', Arial, sans-serif;
  font-size: 1.4rem;
  font-weight: 900;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: #39ff14;
  text-shadow: 0 0 10px #39ff14, 0 0 24px #22c55e;
  margin-bottom: 4px;
}

.loading-subtitle {
  font-family: Orbitron, Arial, sans-serif;
  font-size: 0.72rem;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: rgba(200,255,180,0.70);
  margin-bottom: 20px;
}

.loading-track {
  width: 100%; height: 10px;
  border-radius: 3px;
  overflow: hidden;
  background: rgba(0,40,0,0.80);
  border: 1px solid rgba(34,197,94,0.25);
}

.loading-fill {
  width: 0; height: 100%;
  border-radius: inherit;
  background: linear-gradient(90deg, #16a34a, #39ff14);
  box-shadow: 0 0 14px rgba(57,255,20,0.7);
  transition: width 120ms linear;
}

.loading-percent {
  margin-top: 8px;
  text-align: right;
  font-family: Orbitron, Arial, sans-serif;
  font-size: 0.72rem;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: rgba(200,255,180,0.70);
}
"""), encoding="utf-8")
print("style.css OK")

# ─────────────────────────────────────────────────────────────────────────────
#  UnityProgress.js  (loading overlay, same structure, updated classes)
# ─────────────────────────────────────────────────────────────────────────────
(ROOT / "TemplateData" / "UnityProgress.js").write_text(textwrap.dedent("""\
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
    title.textContent = "Slope\\u2122: Premium Edition";

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
"""), encoding="utf-8")
print("UnityProgress.js OK")
