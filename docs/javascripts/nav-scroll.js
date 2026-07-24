document.addEventListener("DOMContentLoaded", function () {
  const tabs = document.querySelector(".md-tabs__inner");
  if (!tabs) return;

  tabs.addEventListener("wheel", function (event) {
    if (Math.abs(event.deltaY) > Math.abs(event.deltaX)) {
      tabs.scrollLeft += event.deltaY;
      event.preventDefault();
    }
  }, { passive: false });

  const active = tabs.querySelector(".md-tabs__link--active");
  if (active) {
    active.scrollIntoView({ behavior: "instant", block: "nearest", inline: "center" });
  }
});
