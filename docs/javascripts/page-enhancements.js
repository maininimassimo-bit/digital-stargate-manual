document.addEventListener("DOMContentLoaded", () => {
  const content = document.querySelector(".md-content__inner");
  if (!content) return;

  const firstHeading = content.querySelector(":scope > h1");
  if (!firstHeading) return;

  // Homepage excluded: it already has its dedicated visual header.
  if (document.querySelector(".dsg-hero")) return;

  const pathParts = window.location.pathname
    .split("/")
    .filter(Boolean)
    .map((part) => decodeURIComponent(part).replace(/[-_]/g, " "));

  const breadcrumb = document.createElement("nav");
  breadcrumb.className = "dsg-breadcrumb";
  breadcrumb.setAttribute("aria-label", "Percorso pagina");

  const home = document.createElement("a");
  home.href = new URL("./", document.baseURI).href;
  home.textContent = "Home";
  breadcrumb.appendChild(home);

  const visibleParts = pathParts.slice(-2);
  visibleParts.forEach((part, index) => {
    const sep = document.createElement("span");
    sep.className = "dsg-breadcrumb__sep";
    sep.textContent = "›";
    breadcrumb.appendChild(sep);

    const label = document.createElement("span");
    label.textContent = index === visibleParts.length - 1
      ? firstHeading.textContent.trim()
      : part.replace(/\b\w/g, (letter) => letter.toUpperCase());
    breadcrumb.appendChild(label);
  });

  content.insertBefore(breadcrumb, firstHeading);

  // Build previous/next navigation from the visible primary navigation.
  const navLinks = [...document.querySelectorAll(".md-nav--primary a.md-nav__link")]
    .filter((link) => {
      const href = link.getAttribute("href");
      return href && !href.startsWith("#") && link.textContent.trim();
    });

  const currentUrl = new URL(window.location.href);
  const normalize = (url) => {
    const parsed = new URL(url, document.baseURI);
    return parsed.pathname.replace(/index\.html$/, "").replace(/\/+$/, "");
  };

  const currentPath = normalize(currentUrl.href);
  const currentIndex = navLinks.findIndex((link) => normalize(link.href) === currentPath);

  if (currentIndex === -1) return;

  const previous = navLinks[currentIndex - 1];
  const next = navLinks[currentIndex + 1];
  if (!previous && !next) return;

  const pageNav = document.createElement("nav");
  pageNav.className = "dsg-page-nav";
  pageNav.setAttribute("aria-label", "Navigazione tra le pagine");

  const createCard = (link, label, direction) => {
    const card = document.createElement("a");
    card.href = link.href;

    const small = document.createElement("span");
    small.className = "dsg-page-nav__label";
    small.textContent = direction === "previous" ? `← ${label}` : `${label} →`;

    const title = document.createElement("span");
    title.className = "dsg-page-nav__title";
    title.textContent = link.textContent.trim();

    card.append(small, title);
    return card;
  };

  if (previous) pageNav.appendChild(createCard(previous, "Pagina precedente", "previous"));
  if (next) pageNav.appendChild(createCard(next, "Pagina successiva", "next"));

  content.appendChild(pageNav);
});
