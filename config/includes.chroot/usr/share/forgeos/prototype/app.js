const titles={overview:"System overview",workspaces:"Workspaces",updates:"System updates",recovery:"Recovery"};
const buttons=[...document.querySelectorAll(".nav")];
const views=[...document.querySelectorAll(".view")];
buttons.forEach(button=>button.addEventListener("click",()=>{
  const target=button.dataset.view;
  buttons.forEach(item=>item.classList.toggle("active",item===button));
  views.forEach(view=>view.classList.toggle("active-view",view.id===target));
  document.querySelector("#view-title").textContent=titles[target];
}));
const dialog=document.querySelector("#dialog");
document.querySelector("#new-workspace").addEventListener("click",()=>dialog.showModal());
document.addEventListener("keydown",event=>{
  if((event.ctrlKey||event.metaKey)&&event.key.toLowerCase()==="k"){
    event.preventDefault();
    dialog.showModal();
  }
});
