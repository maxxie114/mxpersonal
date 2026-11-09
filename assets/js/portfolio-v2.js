(() => {
  const root = document.documentElement;
  const theme = document.getElementById("theme");
  function setTheme(light) {
    root.dataset.theme = light ? "light" : "dark";
    theme.setAttribute("aria-pressed", String(light));
  }
  try {
    setTheme(localStorage.getItem("portfolio-theme") === "light");
  } catch {
    setTheme(false);
  }
  theme.hidden = false;
  theme.addEventListener("click", () => {
    setTheme(root.dataset.theme !== "light");
    try { localStorage.setItem("portfolio-theme", root.dataset.theme); } catch { /* Session-only theme. */ }
  });

  const menu = document.getElementById("menu");
  const nav = document.getElementById("navigation");
  function setMenu(open) {
    nav.classList.toggle("open", open);
    menu.setAttribute("aria-expanded", String(open));
  }
  menu.hidden = false;
  root.classList.add("enhanced");
  menu.addEventListener("click", () => setMenu(!nav.classList.contains("open")));
  document.addEventListener("keydown", event => {
    if (event.key === "Escape" && nav.classList.contains("open")) {
      setMenu(false);
      menu.focus();
    }
  });
  nav.addEventListener("click", () => setMenu(false));
  matchMedia("(max-width:740px)").addEventListener("change", () => setMenu(false));

  const filters = document.querySelector(".filterbar");
  if (filters) {
    filters.hidden = false;
    const cards = [...document.querySelectorAll("[data-filters]")];
    filters.addEventListener("click", event => {
      const button = event.target.closest("[data-filter]");
      if (!button) return;
      const category = button.dataset.filter;
      for (const control of filters.querySelectorAll("button")) {
        control.setAttribute("aria-pressed", String(control === button));
      }
      for (const card of cards) {
        card.hidden = category !== "All" && !card.dataset.filters.split("|").includes(category);
      }
      const count = cards.filter(card => !card.hidden).length;
      document.getElementById("filter-count").textContent = count + (count === 1 ? " project" : " projects");
    });
  }

  const query = document.getElementById("research-query");
  if (query) {
    query.parentElement.hidden = false;
    const items = [...document.querySelectorAll(".research-item")];
    query.addEventListener("input", () => {
      const term = query.value.trim().toLowerCase();
      for (const item of items) item.hidden = !item.textContent.toLowerCase().includes(term);
      const count = items.filter(item => !item.hidden).length;
      document.getElementById("search-status").textContent = term
        ? (count ? count + (count === 1 ? " result" : " results") : "No matching research. Try another title or topic.")
        : "";
    });
  }

  const viewer = document.getElementById("figure-viewer");
  if (viewer && typeof viewer.showModal === "function") {
    const frame = viewer.querySelector(".viewer-image");
    const image = frame.querySelector("img");
    const scale = document.getElementById("figure-scale");
    let opener;
    function setZoom(zoomed) {
      viewer.classList.toggle("zoomed", zoomed);
      scale.textContent = zoomed ? "Fit image" : "Zoom in";
      frame.scrollTo(0, 0);
    }
    for (const trigger of document.querySelectorAll("[data-open-figure]")) {
      trigger.setAttribute("aria-haspopup", "dialog");
      trigger.setAttribute("aria-controls", viewer.id);
      trigger.addEventListener("click", event => {
        if (event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
        event.preventDefault();
        const preview = trigger.closest("figure").querySelector("img");
        image.src = preview.currentSrc || preview.src;
        image.alt = preview.alt;
        frame.style.setProperty("--figure-width", preview.getAttribute("width") + "px");
        opener = trigger;
        setZoom(false);
        viewer.showModal();
      });
    }
    scale.addEventListener("click", () => setZoom(!viewer.classList.contains("zoomed")));
    viewer.addEventListener("click", event => {
      if (event.target === viewer) viewer.close();
    });
    viewer.addEventListener("close", () => opener?.focus({preventScroll:true}));
  }

  const copy = document.getElementById("copy-citation");
  if (copy && navigator.clipboard) {
    copy.hidden = false;
    copy.addEventListener("click", async () => {
      const status = document.getElementById("copy-status");
      try {
        await navigator.clipboard.writeText(document.querySelector("#citation blockquote").textContent);
        status.textContent = " Citation copied.";
      } catch {
        status.textContent = " Select the citation above to copy it manually.";
      }
    });
  }
})();
