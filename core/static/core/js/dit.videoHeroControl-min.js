(()=>{var t={335:t=>{class e{constructor(t,e,s={}){this.video=t,this.controlBtn=e,this.playClass=s.playClass||"atlas-hero__video-control-play",this.pauseClass=s.pauseClass||"atlas-hero__video-control-pause",this.init()}init(){this.controlBtn.addEventListener("click",(()=>{this.toggleVideoPlayPause()}))}toggleVideoPlayPause(){this.video.paused?(this.video.play(),this.updateButton(this.pauseClass,"Pause video","Pause"),this.controlBtn.setAttribute("aria-pressed","true"),document.getElementById("js-video-status").textContent="Video playing"):(this.video.pause(),this.updateButton(this.playClass,"Play video","Play"),this.controlBtn.setAttribute("aria-pressed","false"),document.getElementById("js-video-status").textContent="Video paused")}updateButton(t,e,s){this.controlBtn.classList.remove(this.playClass,this.pauseClass),this.controlBtn.classList.add(t),this.controlBtn.setAttribute("aria-label",e),this.controlBtn.querySelector(".atlas-hero__video-control-icon span").textContent=s}}document.addEventListener("DOMContentLoaded",(()=>{const t=document.getElementById("js-atlas-video"),s=document.getElementById("js-video-control");t&&new e(t,s)})),t.exports=e}},e={};!function s(o){var a=e[o];if(void 0!==a)return a.exports;var i=e[o]={exports:{}};return t[o](i,i.exports,s),i.exports}(335)})();
//# sourceMappingURL=dit.videoHeroControl-min.js.map