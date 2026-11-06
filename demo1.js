// Demo 1: tile scenes (play once in view, replay on hover/focus) and the stage studio.
{
const section = document.querySelector("#demo-ppt");
const reduceMotion = matchMedia("(prefers-reduced-motion: reduce)").matches;
const tiles = [...section.querySelectorAll("[data-tile]")];
const playing = new Set();

function play(tile) {
  playing.add(tile);
  tile.classList.remove("played");
  void tile.offsetWidth;
  tile.classList.add("played");
  Promise.allSettled(tile.getAnimations({ subtree: true }).map(a => a.finished)).then(() => playing.delete(tile));
}

if (!reduceMotion) {
  section.classList.add("js-armed");
  const tileObserver = new IntersectionObserver(entries => {
    entries.filter(entry => entry.isIntersecting)
      .sort((a, b) => tiles.indexOf(a.target) - tiles.indexOf(b.target))
      .forEach((entry, order) => {
        tileObserver.unobserve(entry.target);
        setTimeout(() => play(entry.target), 200 + order * 250);
      });
  }, { threshold: 0.7 });
  tiles.forEach(tile => tileObserver.observe(tile));

  const replay = tile => {
    if (!tile.classList.contains("played") || playing.has(tile)) return;
    playing.add(tile);
    tile.classList.add("replay", "blurring");
    setTimeout(() => { play(tile); tile.classList.remove("blurring"); }, 160);
  };
  tiles.forEach(tile => {
    tile.addEventListener("pointerenter", event => { if (event.pointerType === "mouse") replay(tile); });
    tile.addEventListener("focus", () => replay(tile));
  });
}

const studio = section.querySelector("[data-studio]");
const steps = [...studio.querySelectorAll("[data-step]")];
const panels = [...studio.querySelectorAll(".stage-panel")];
const progress = studio.querySelector(".studio-progress i");
const playButton = studio.querySelector("[data-play]");
let current = 0;
let timer = null;

function show(n) {
  current = (n + panels.length) % panels.length;
  steps.forEach((step, i) => step.setAttribute("aria-selected", String(i === current)));
  steps.forEach((step, i) => step.tabIndex = i === current ? 0 : -1);
  panels.forEach((panel, i) => panel.toggleAttribute("data-active", i === current));
  tiles.forEach((tile, i) => tile.classList.toggle("is-current", i === current));
  progress.style.width = `${(current + 1) / panels.length * 100}%`;
}

function autoplay(on) {
  clearInterval(timer);
  timer = null;
  playButton.setAttribute("aria-pressed", String(on));
  playButton.querySelector("span").textContent = on ? "暂停" : "自动回放";
  if (!on) return;
  if (current === panels.length - 1) show(0);
  timer = setInterval(() => {
    if (current === panels.length - 1) autoplay(false);
    else show(current + 1);
  }, 4800);
}

steps.forEach((step, i) => {
  step.addEventListener("click", () => { autoplay(false); show(i); });
  step.addEventListener("keydown", event => {
    const move = { ArrowRight: 1, ArrowLeft: -1 }[event.key];
    if (!move) return;
    event.preventDefault();
    autoplay(false);
    show(current + move);
    steps[current].focus();
  });
});
studio.querySelector("[data-prev]").addEventListener("click", () => { autoplay(false); show(current - 1); });
studio.querySelector("[data-next]").addEventListener("click", () => { autoplay(false); show(current + 1); });
playButton.addEventListener("click", () => autoplay(!timer));

// Tile links point at #stage-N, so a click (or tap) jumps to the studio on that stage.
const fromHash = () => {
  const match = location.hash.match(/^#stage-(\d+)$/);
  if (match && panels[match[1]]) { autoplay(false); show(Number(match[1])); }
};
addEventListener("hashchange", fromHash);
tiles.forEach((tile, i) => tile.addEventListener("click", () => { autoplay(false); show(i); }));
show(0);
fromHash();

if (!reduceMotion && !location.hash.startsWith("#stage-")) {
  const studioObserver = new IntersectionObserver(entries => {
    if (!entries[0].isIntersecting) return;
    studioObserver.disconnect();
    if (current === 0) autoplay(true);
  }, { threshold: 0.45 });
  studioObserver.observe(studio);
}
}
