dit=window.dit||{},dit.cookieBanner=new function(){this.init=function(t){window.addEventListener("DOMContentLoaded",function(){this.banner=document.getElementById(t.bannerId),this.prompt=document.getElementById(t.promptId),this.thanks=document.getElementById(t.thanksId),this.acceptAll=document.getElementById(t.acceptAllId),this.dismiss=document.getElementById(t.dismissId);const i=document.getElementById("privacyCookieDomain");this.cookieOptions={path:"/",domain:!!i&&i.getAttribute("value"),secure:"https:"===window.location.protocol,days:365},this.bindEvents()}.bind(this))},this.buildCookieString=function(t,i,e){void 0===e&&(e={});let n=t+"="+i;return e.path&&(n+="; path="+e.path),e.domain&&(n+="; domain="+e.domain),e.secure&&(n+="; Secure"),e.days&&(n+="; max-age=60*60*24*"+e.days),n},this.setCookie=function(t,i){document.cookie=this.buildCookieString(t,i,this.cookieOptions)},this.handleAcceptAll=function(){this.setCookie("cookie_preferences_set","true"),this.setCookie("cookies_policy",JSON.stringify({essential:!0,settings:!0,usage:!0,campaigns:!0})),this.prompt.remove(),this.thanks.style.display="block"},this.handleDismiss=function(){this.banner.remove()},this.bindEvents=function(){this.acceptAll.addEventListener("click",this.handleAcceptAll.bind(this)),this.dismiss.addEventListener("click",this.handleDismiss.bind(this))}};
//# sourceMappingURL=maps/dit.cookieBanner-min.js.map
