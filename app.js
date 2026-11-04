const revisions={
  v001:{status:"NEEDS REVISION",state:"needs",number:"REVISION 01 / 18",title:"重要 caveat 与来源细节缺失",text:"首轮盲审指出流动性数字缺少“estimated”限定、来源注释被导航遮挡，且 AWM 页面漏掉关键的 $3.0T 资产管理规模。",evidence:"发现 → 修订 → 再渲染。早期差距影响方法和内容，不靠清零几何告警放行。",image:"assets/v001-contact-sheet.png",alt:"v001 初版演示缩略图"},
  v013:{status:"PASS · MID-RUN",state:"pass",number:"REVISION 13 / 18",title:"中途评审通过，但工作仍继续",text:"v013 reviewer 认为 15 页故事、核心数字、期间、标签与 caveat 已达标。后续修改仍触发重新检查，v015 发现总计舍入说明缺失。",evidence:"状态随当前产物更新；一次 PASS 不会冻结剩余修改。",image:"assets/v013-contact-sheet.png",alt:"v013 中途评审通过时的演示缩略图"},
  v017:{status:"NEEDS REVISION",state:"needs",number:"REVISION 17 / 18",title:"“net” 在最后一页丢了",text:"盲审发现 slide 15 把来源里的 “$5.0 billion … net repurchases” 写成 “repurchased $5.0B of common stock”。“net” 会改变业务含义，必须补回。",evidence:"来源标签差距 → 修订 slide 15 → v018 重渲染并复核。",image:"assets/v017-slide-15.png",alt:"v017 slide 15 漏掉 net 的版本"},
  v018:{status:"PASS · FINAL",state:"pass",number:"REVISION 18 / 18",title:"修正后，独立复核通过",text:"v018 保留了 “net repurchases”。coverage reviewer 确认页数准确、关键盈利 caveat 易懂，引用数字与期间一致；唯一的图表建议是把 slide 9 的 -20% 与 +30% 放到以 0 为中心的比较图中；评审将其列为可选改进。",evidence:"15 slides · quality map 3/3 pass · renderer warnings 0。",image:"assets/v018-slide-15.png",alt:"v018 slide 15 修正后的版本"}
};
const buttons=[...document.querySelectorAll(".revision")];
function showRevision(key){const r=revisions[key];document.getElementById("revisionStatus").textContent=r.status;document.getElementById("revisionStatus").className=`status ${r.state}`;document.getElementById("revisionVersion").textContent=r.number;document.getElementById("revisionTitle").textContent=r.title;document.getElementById("revisionText").textContent=r.text;document.getElementById("revisionEvidence").textContent=r.evidence;const img=document.getElementById("revisionImage");img.src=r.image;img.alt=r.alt;buttons.forEach(b=>b.classList.toggle("active",b.dataset.rev===key));}
buttons.forEach(b=>b.addEventListener("click",()=>showRevision(b.dataset.rev)));

