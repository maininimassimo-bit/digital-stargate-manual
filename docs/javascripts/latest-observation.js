(() => {
  const ALADIN_SRC = "https://aladin.cds.unistra.fr/AladinLite/api/v3/latest/aladin.js";
  const DATA_PATH = "data/realtime/latest-observation.json";

  const formatNumber = (value, decimals = 0) => {
    const number = Number(value);
    if (!Number.isFinite(number)) return "—";
    return number.toLocaleString("it-IT", {
      minimumFractionDigits: decimals,
      maximumFractionDigits: decimals
    });
  };

  const formatCoordinate = (value, suffix) => {
    const number = Number(value);
    return Number.isFinite(number) ? `${formatNumber(number, 4)}° ${suffix}` : "Risoluzione per nome";
  };

  const injectStyles = () => {
    if (document.getElementById("dsg-latest-observation-styles")) return;

    const style = document.createElement("style");
    style.id = "dsg-latest-observation-styles";
    style.textContent = `
      .dsg-showcase__media {
        position: relative;
        overflow: hidden;
        background: #07162d;
      }

      .dsg-showcase__sky,
      .dsg-showcase__sky-canvas {
        position: absolute;
        inset: 0;
        width: 100%;
        height: 100%;
        min-height: 25rem;
      }

      .dsg-showcase__sky {
        background: center / cover no-repeat url("../assets/images/osservatorio-hero.jpg");
      }

      .dsg-showcase__sky-canvas {
        z-index: 1;
      }

      .dsg-showcase__sky-shade {
        position: absolute;
        inset: 0;
        z-index: 2;
        pointer-events: none;
        background:
          linear-gradient(90deg, rgba(5, 18, 42, 0.04), rgba(5, 18, 42, 0.48)),
          linear-gradient(180deg, rgba(5, 18, 42, 0.18), transparent 38%, rgba(5, 18, 42, 0.42));
      }

      .dsg-showcase__sky-status {
        position: absolute;
        z-index: 4;
        top: 1rem;
        left: 1rem;
        display: inline-flex;
        align-items: center;
        gap: 0.45rem;
        padding: 0.48rem 0.7rem;
        border: 1px solid rgba(125, 190, 255, 0.28);
        border-radius: 999px;
        background: rgba(5, 18, 42, 0.78);
        color: #b9e8ff;
        font-size: 0.62rem;
        font-weight: 800;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        backdrop-filter: blur(8px);
      }

      .dsg-showcase__sky-status::before {
        content: "";
        width: 0.45rem;
        height: 0.45rem;
        border-radius: 50%;
        background: #67d6ff;
        box-shadow: 0 0 0.75rem rgba(103, 214, 255, 0.85);
      }

      .dsg-showcase__sky-panel {
        position: absolute;
        z-index: 4;
        right: 1rem;
        bottom: 1rem;
        width: min(18rem, calc(100% - 2rem));
        padding: 0.8rem 0.9rem;
        border: 1px solid rgba(125, 190, 255, 0.22);
        border-radius: 0.8rem;
        background: rgba(5, 18, 42, 0.80);
        color: rgba(235, 247, 255, 0.84);
        font-size: 0.66rem;
        backdrop-filter: blur(10px);
      }

      .dsg-showcase__sky-panel strong {
        display: block;
        margin-bottom: 0.4rem;
        color: #ffffff;
        font-size: 0.9rem;
      }

      .dsg-showcase__sky-meta {
        display: grid;
        grid-template-columns: auto 1fr;
        gap: 0.2rem 0.65rem;
      }

      .dsg-showcase__sky-meta span:nth-child(odd) {
        color: #75d5ff;
        font-weight: 750;
        text-transform: uppercase;
      }

      .dsg-showcase__sky.is-loading::before {
        content: "";
        position: absolute;
        z-index: 3;
        top: 50%;
        left: 50%;
        width: 2.4rem;
        height: 2.4rem;
        margin: -1.2rem 0 0 -1.2rem;
        border: 2px solid rgba(130, 190, 255, 0.22);
        border-top-color: #75d5ff;
        border-radius: 50%;
        animation: dsg-sky-spin 0.9s linear infinite;
      }

      .dsg-showcase__sky.is-fallback .dsg-showcase__sky-status::before {
        background: #ffbd59;
        box-shadow: 0 0 0.75rem rgba(255, 189, 89, 0.72);
      }

      .dsg-showcase__sky .aladin-location,
      .dsg-showcase__sky .aladin-fov,
      .dsg-showcase__sky .aladin-zoomControl,
      .dsg-showcase__sky .aladin-fullScreenControl,
      .dsg-showcase__sky .aladin-layersControl-container,
      .dsg-showcase__sky .aladin-gotoControl-container,
      .dsg-showcase__sky .aladin-shareControl-container {
        display: none !important;
      }

      @keyframes dsg-sky-spin {
        to { transform: rotate(360deg); }
      }

      @media (max-width: 760px) {
        .dsg-showcase__sky,
        .dsg-showcase__sky-canvas,
        .dsg-showcase__media {
          min-height: 19rem;
        }

        .dsg-showcase__sky-panel {
          right: 0.75rem;
          bottom: 0.75rem;
          left: 0.75rem;
          width: auto;
        }
      }
    `;
    document.head.appendChild(style);
  };

  const loadAladin = () => {
    if (window.A?.aladin && window.A?.init) return Promise.resolve();

    const existing = document.querySelector(`script[src="${ALADIN_SRC}"]`);
    if (existing) {
      if (existing.dataset.loaded === "true") return Promise.resolve();
      return new Promise((resolve, reject) => {
        existing.addEventListener("load", resolve, { once: true });
        existing.addEventListener("error", reject, { once: true });
      });
    }

    return new Promise((resolve, reject) => {
      const script = document.createElement("script");
      script.src = ALADIN_SRC;
      script.charset = "utf-8";
      script.async = true;
      script.addEventListener("load", () => {
        script.dataset.loaded = "true";
        resolve();
      }, { once: true });
      script.addEventListener("error", reject, { once: true });
      document.head.appendChild(script);
    });
  };

  const setText = (selector, value) => {
    const element = document.querySelector(selector);
    if (element && value !== undefined && value !== null) element.textContent = value;
  };

  const applyData = (data) => {
    const metrics = data.metrics || {};
    setText(".dsg-showcase__content h2", data.target?.name || "Ultima osservazione");

    const metricValues = document.querySelectorAll(".dsg-showcase__metrics strong");
    if (metricValues[0]) metricValues[0].textContent = `${formatNumber(metrics.integration_hours, 2)} h`;
    if (metricValues[1]) metricValues[1].textContent = formatNumber(metrics.completed_frames, 0);
    if (metricValues[2]) metricValues[2].textContent = `${formatNumber(metrics.rms_total_arcsec, 3)}″`;

    const reportLink = document.querySelector(".dsg-showcase__content .md-button");
    if (reportLink && data.report_url) reportLink.href = new URL(data.report_url, document.baseURI).href;
  };

  const buildTarget = (data) => {
    const ra = Number(data.target?.ra_deg);
    const dec = Number(data.target?.dec_deg);
    if (Number.isFinite(ra) && Number.isFinite(dec)) return `${ra} ${dec}`;
    return data.target?.name || "LDN 1320";
  };

  const updatePanel = (panel, data) => {
    panel.querySelector("strong").textContent = data.target?.name || "Ultima osservazione";
    panel.querySelector("[data-sky-survey]").textContent = data.sky_view?.survey || "P/DSS2/color";
    panel.querySelector("[data-sky-fov]").textContent = `${formatNumber(data.sky_view?.field_of_view_deg || 1.5, 1)}°`;
    panel.querySelector("[data-sky-ra]").textContent = formatCoordinate(data.target?.ra_deg, "RA");
    panel.querySelector("[data-sky-dec]").textContent = formatCoordinate(data.target?.dec_deg, "DEC");
  };

  const enableFallback = (sky, canvas, status, fallbackUrl) => {
    sky.classList.remove("is-loading");
    sky.classList.add("is-fallback");
    status.textContent = "Immagine di fallback";
    canvas.style.display = "none";
    if (fallbackUrl) {
      sky.style.backgroundImage = `linear-gradient(90deg, rgba(5,18,42,.10), rgba(5,18,42,.62)), url("${fallbackUrl}")`;
      sky.style.backgroundSize = "cover";
      sky.style.backgroundPosition = "center";
    }
  };

  const initLatestObservation = async () => {
    const media = document.querySelector(".dsg-showcase__media");
    if (!media || media.dataset.dynamicSkyReady === "true") return;
    media.dataset.dynamicSkyReady = "true";

    injectStyles();
    media.setAttribute("aria-label", "Mappa dinamica dell'ultima osservazione astronomica");
    media.innerHTML = `
      <div id="dsg-latest-sky" class="dsg-showcase__sky is-loading">
        <div id="dsg-latest-sky-canvas" class="dsg-showcase__sky-canvas" aria-label="Vista astronomica interattiva"></div>
        <div class="dsg-showcase__sky-shade" aria-hidden="true"></div>
        <span class="dsg-showcase__sky-status">Caricamento survey</span>
        <div class="dsg-showcase__sky-panel">
          <strong>Ultima osservazione</strong>
          <div class="dsg-showcase__sky-meta">
            <span>Survey</span><span data-sky-survey>—</span>
            <span>FOV</span><span data-sky-fov>—</span>
            <span>RA</span><span data-sky-ra>—</span>
            <span>DEC</span><span data-sky-dec>—</span>
          </div>
        </div>
      </div>
    `;

    const sky = media.querySelector("#dsg-latest-sky");
    const canvas = media.querySelector("#dsg-latest-sky-canvas");
    const status = media.querySelector(".dsg-showcase__sky-status");
    const panel = media.querySelector(".dsg-showcase__sky-panel");

    let data;
    try {
      const response = await fetch(new URL(DATA_PATH, document.baseURI), { cache: "no-store" });
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      data = await response.json();
      applyData(data);
      updatePanel(panel, data);
    } catch (error) {
      console.warn("Digital StarGate: latest observation data unavailable", error);
      enableFallback(sky, canvas, status, new URL("assets/images/osservatorio-hero.jpg", document.baseURI).href);
      return;
    }

    const fallbackUrl = data.fallback_image
      ? new URL(data.fallback_image, document.baseURI).href
      : new URL("assets/images/osservatorio-hero.jpg", document.baseURI).href;

    try {
      await loadAladin();
      await window.A.init;

      window.A.aladin("#dsg-latest-sky-canvas", {
        survey: data.sky_view?.survey || "P/DSS2/color",
        target: buildTarget(data),
        fov: Number(data.sky_view?.field_of_view_deg) || 1.5,
        projection: "SIN",
        cooFrame: "equatorial",
        showReticle: true,
        showZoomControl: false,
        showFullscreenControl: false,
        showLayersControl: false,
        showGotoControl: false,
        showShareControl: false,
        showSimbadPointerControl: false
      });

      sky.classList.remove("is-loading");
      status.textContent = `Survey attiva · FOV ${formatNumber(data.sky_view?.field_of_view_deg || 1.5, 1)}°`;
    } catch (error) {
      console.warn("Digital StarGate: Aladin Lite unavailable", error);
      enableFallback(sky, canvas, status, fallbackUrl);
    }
  };

  if (window.document$?.subscribe) {
    window.document$.subscribe(initLatestObservation);
  } else if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initLatestObservation, { once: true });
  } else {
    initLatestObservation();
  }
})();
