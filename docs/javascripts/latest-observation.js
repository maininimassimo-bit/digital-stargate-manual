(() => {
  'use strict';

  const ALADIN_SRC = "https://aladin.cds.unistra.fr/AladinLite/api/v3/latest/aladin.js";
  const DATA_PATH = "data/realtime/latest-observation.json";

  const formatNumber = (value, decimals = 0) => {
    const number = typeof value === "number" ? value : NaN;
    if (!Number.isFinite(number)) return "—";
    return number.toLocaleString("it-IT", { minimumFractionDigits: decimals, maximumFractionDigits: decimals });
  };

  const formatCoordinate = (value) => {
    const number = typeof value === "number" ? value : NaN;
    return Number.isFinite(number) ? `${formatNumber(number, 4)}°` : "Non disponibile";
  };

  const injectStyles = () => {
    if (document.getElementById("dsg-latest-observation-styles")) return;
    const style = document.createElement("style");
    style.id = "dsg-latest-observation-styles";
    style.textContent = `
      .dsg-showcase__media{position:relative;overflow:hidden;background:#07162d}
      .dsg-showcase__sky,.dsg-showcase__sky-canvas{position:absolute;inset:0;width:100%;height:100%;min-height:22rem}
      .dsg-showcase__sky{background:center/cover no-repeat url("../assets/images/osservatorio-hero.jpg")}
      .dsg-showcase__sky-canvas{z-index:1}.dsg-showcase__sky-shade{position:absolute;inset:0;z-index:2;pointer-events:none;background:linear-gradient(90deg,rgba(5,18,42,.04),rgba(5,18,42,.25)),linear-gradient(180deg,rgba(5,18,42,.14),transparent 38%,rgba(5,18,42,.28))}
      .dsg-showcase__sky-status{position:absolute;z-index:4;top:1rem;left:1rem;display:inline-flex;align-items:center;gap:.45rem;padding:.48rem .7rem;border:1px solid rgba(125,190,255,.28);border-radius:999px;background:rgba(5,18,42,.78);color:#b9e8ff;font-size:.62rem;font-weight:800;letter-spacing:.08em;text-transform:uppercase;backdrop-filter:blur(8px)}
      .dsg-showcase__sky-status::before{content:"";width:.45rem;height:.45rem;border-radius:50%;background:#67d6ff;box-shadow:0 0 .75rem rgba(103,214,255,.85)}
      .dsg-showcase__sky.is-loading::before{content:"";position:absolute;z-index:3;top:50%;left:50%;width:2.4rem;height:2.4rem;margin:-1.2rem 0 0 -1.2rem;border:2px solid rgba(130,190,255,.22);border-top-color:#75d5ff;border-radius:50%;animation:dsg-sky-spin .9s linear infinite}
      .dsg-showcase__sky.is-fallback .dsg-showcase__sky-status::before{background:#ffbd59;box-shadow:0 0 .75rem rgba(255,189,89,.72)}
      .dsg-showcase__sky .aladin-location,.dsg-showcase__sky .aladin-fov,.dsg-showcase__sky .aladin-zoomControl,.dsg-showcase__sky .aladin-fullScreenControl,.dsg-showcase__sky .aladin-layersControl-container,.dsg-showcase__sky .aladin-gotoControl-container,.dsg-showcase__sky .aladin-shareControl-container{display:none!important}
      @keyframes dsg-sky-spin{to{transform:rotate(360deg)}}
      @media(max-width:760px){.dsg-showcase__sky,.dsg-showcase__sky-canvas,.dsg-showcase__media{min-height:18rem}}
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
      script.src = ALADIN_SRC; script.charset = "utf-8"; script.async = true;
      script.addEventListener("load", () => { script.dataset.loaded = "true"; resolve(); }, { once: true });
      script.addEventListener("error", () => { script.remove(); reject(new Error("Aladin script unavailable")); }, { once: true });
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
  };

  const coordinates = data => {
    const ra = data.target?.ra_deg, dec = data.target?.dec_deg;
    return typeof ra === 'number' && Number.isFinite(ra) && ra >= 0 && ra < 360
      && typeof dec === 'number' && Number.isFinite(dec) && dec >= -90 && dec <= 90
      && data.target?.epoch === 'J2000' ? [ra, dec] : null;
  };

  const updatePanel = (data) => {
    setText("[data-sky-survey]", data.sky_view?.survey || "P/DSS2/color");
    setText("[data-sky-fov]", `${formatNumber(data.sky_view?.field_of_view_deg || 1.5, 1)}°`);
    const pair = coordinates(data);
    setText("[data-sky-ra]", pair ? formatCoordinate(pair[0]) : "Non disponibile");
    setText("[data-sky-dec]", pair ? formatCoordinate(pair[1]) : "Non disponibile");
    setText("[data-sky-session]", data.session_id || "Non disponibile");
    setText("[data-sky-source]", data.target?.coordinate_source || data.coordinate_source || "unavailable");
  };

  const enableFallback = (sky, canvas, status, fallbackUrl) => {
    sky.classList.remove("is-loading"); sky.classList.add("is-fallback"); status.textContent = "Immagine di fallback"; canvas.style.display = "none";
    if (fallbackUrl) { sky.style.backgroundImage = `linear-gradient(90deg,rgba(5,18,42,.10),rgba(5,18,42,.42)),url("${fallbackUrl}")`; sky.style.backgroundSize = "cover"; sky.style.backgroundPosition = "center"; }
  };

  const initialize = async ({ events } = {}) => {
    const media = document.querySelector(".dsg-showcase__media");
    if (!media || media.dataset.dynamicSkyReady === "true") return;
    media.dataset.dynamicSkyReady = "true"; injectStyles(); media.classList.add("is-loading");
    media.innerHTML = `<div id="dsg-latest-sky" class="dsg-showcase__sky is-loading"><div id="dsg-latest-sky-canvas" class="dsg-showcase__sky-canvas" aria-label="Vista astronomica interattiva"></div><div class="dsg-showcase__sky-shade" aria-hidden="true"></div><span class="dsg-showcase__sky-status">Caricamento survey</span></div>`;
    const sky = media.querySelector("#dsg-latest-sky"), canvas = media.querySelector("#dsg-latest-sky-canvas"), status = media.querySelector(".dsg-showcase__sky-status");
    let viewer = null, renderedKey = null, loading = false, stopped = false;
    const section = media.closest('.dsg-latest-observation');
    const button = section?.querySelector('[data-latest-sky-refresh]');
    const note = section?.querySelector('[data-latest-sky-note]');
    const bounded = (promise, milliseconds) => {
      let timer;
      return Promise.race([promise, new Promise((_,reject) => {timer=setTimeout(()=>reject(new Error('Timeout')),milliseconds);})]).finally(()=>clearTimeout(timer));
    };
    const unavailable = (message, data = {}) => {
      renderedKey = null;
      enableFallback(sky, canvas, status, new URL('assets/images/osservatorio-hero.jpg',document.baseURI).href);
      status.textContent = message;
      if (note) note.textContent = data.session_id
        ? `Sessione ${data.session_id}: coordinate J2000 non disponibili nei dati importati. Nessun centro astronomico dedotto.`
        : 'Dati dell’ultima sessione non disponibili. Riprova con Aggiorna.';
      media.classList.remove('is-loading','is-ready'); media.classList.add('is-degraded');
    };
    const refresh = async () => {
      if (loading || stopped || !media.isConnected) return;
      loading=true;
      if (button) button.disabled=true;
      const controller=new AbortController();
      const timeout=setTimeout(()=>controller.abort(),12000);
      let data;
      try {
        const response=await fetch(new URL(DATA_PATH,document.baseURI),{cache:'no-store',signal:controller.signal});
        if (!response.ok) throw new Error(`HTTP ${response.status}`);
        const payload=await response.json();
        if (payload?.schema_version !== '1.2' || !/^\d{4}-\d{2}-\d{2}_\d{4}-\d{2}-\d{2}$/.test(payload.session_id)) throw new Error('Invalid latest observation');
        data=payload;
        if (stopped || !media.isConnected) return;
        applyData(data); updatePanel(data);
        events?.emit('latest-observation-data-ready',{target:data.target?.name || null,source:DATA_PATH});
        const pair=coordinates(data);
        if (!pair) {unavailable('Coordinate non disponibili',data);return;}
        const fov=typeof data.sky_view?.field_of_view_deg==='number' && data.sky_view.field_of_view_deg>0 && data.sky_view.field_of_view_deg<=180 ? data.sky_view.field_of_view_deg : 1.5;
        const survey=data.sky_view?.survey || 'P/DSS2/color';
        const key=JSON.stringify([data.session_id,...pair,survey,fov]);
        if (key===renderedKey) return;
        await bounded(loadAladin().then(()=>window.A.init),15000);
        if (stopped || !media.isConnected) return;
        canvas.style.display='';
        if (!viewer) viewer=window.A.aladin('#dsg-latest-sky-canvas',{survey,target:`${pair[0]} ${pair[1]}`,fov,projection:'SIN',cooFrame:'equatorial',showReticle:true,showZoomControl:false,showFullscreenControl:false,showLayersControl:false,showGotoControl:false,showShareControl:false,showSimbadPointerControl:false});
        else {viewer.gotoRaDec(...pair);viewer.setFoV(fov);viewer.setBaseImageLayer(survey);}
        renderedKey=key;
        sky.classList.remove('is-loading','is-fallback'); media.classList.remove('is-loading','is-degraded');media.classList.add('is-ready');
        status.textContent=`Survey attiva · FOV ${formatNumber(fov,1)}°`;
        if (note) note.textContent=`Sessione ${data.session_id} · coordinate J2000 dai dati importati. Aggiornamento automatico ogni 60 secondi.`;
      } catch (error) {
        console.warn('Digital StarGate: latest observation unavailable',error);
        if (stopped || !media.isConnected) return;
        if (!data) {applyData({});updatePanel({});}
        unavailable(data ? 'Survey non disponibile' : 'Dati non disponibili');
        if (data && note) note.textContent=`Sessione ${data.session_id}: coordinate pubblicate disponibili, survey temporaneamente non disponibile.`;
      } finally {clearTimeout(timeout);loading=false;if(button)button.disabled=false;}
    };
    const onVisible=()=>{if (!document.hidden) refresh();};
    button?.addEventListener('click',refresh);
    document.addEventListener('visibilitychange',onVisible);
    const timer=setInterval(()=>{
      if (!media.isConnected) {stopped=true;clearInterval(timer);document.removeEventListener('visibilitychange',onVisible);return;}
      if (!document.hidden) refresh();
    },60000);
    await refresh();
  };

  if (window.DSG?.components) { window.DSG.components.register({ name:"latest-observation", order:68, initialize }); return; }
  const fallback = () => initialize();
  if (window.document$?.subscribe) window.document$.subscribe(fallback); else if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", fallback, { once:true }); else fallback();
})();
