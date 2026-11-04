const tabs=[...document.querySelectorAll(".demo-tab")];
const panels=[...document.querySelectorAll(".demo-panel")];
tabs.forEach(tab=>tab.addEventListener("click",()=>{
  const target=tab.dataset.panel;
  tabs.forEach(item=>{
    const active=item===tab;
    item.classList.toggle("active",active);
    item.setAttribute("aria-selected",String(active));
  });
  panels.forEach(panel=>{panel.hidden=panel.id!==target;});
}));
