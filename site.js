(function(){
  var hover = window.matchMedia && matchMedia('(hover:hover) and (pointer:fine)').matches;
  // Header-Schatten beim Scrollen
  var hd=document.querySelector('.hd');
  function sc(){if(hd)hd.classList.toggle('scrolled',window.scrollY>8);}
  sc();window.addEventListener('scroll',sc,{passive:true});

  // Dropdowns: Klick öffnet/schliesst, Hover mit Verzögerung beim Verlassen
  var dds=[].slice.call(document.querySelectorAll('[data-dd]'));
  function setOpen(d,o){d.classList.toggle('open',o);d.querySelector('button').setAttribute('aria-expanded',o?'true':'false');}
  function closeAll(except){dds.forEach(function(d){if(d!==except)setOpen(d,false);});}
  dds.forEach(function(d){
    var b=d.querySelector('button'),t=null;
    b.addEventListener('click',function(e){e.stopPropagation();var o=!d.classList.contains('open');closeAll(d);setOpen(d,o);});
    if(hover){
      d.addEventListener('mouseenter',function(){clearTimeout(t);closeAll(d);setOpen(d,true);});
      d.addEventListener('mouseleave',function(){clearTimeout(t);t=setTimeout(function(){setOpen(d,false);},450);});
    }
    d.addEventListener('focusout',function(e){if(!d.contains(e.relatedTarget))setOpen(d,false);});
  });
  document.addEventListener('click',function(e){if(!e.target.closest('[data-dd]'))closeAll();});

  // Mobile-Menü
  var mb=document.querySelector('.menu-btn'),mn=document.getElementById('mnav');
  function mOpen(o){if(!mb||!mn)return;mn.classList.toggle('open',o);mb.setAttribute('aria-expanded',o?'true':'false');mb.textContent=o?'Schliessen':'Menü';document.body.classList.toggle('menu-open',o);}
  if(mb&&mn){mb.addEventListener('click',function(){mOpen(!mn.classList.contains('open'));});
    mn.addEventListener('click',function(e){if(e.target.closest('a'))mOpen(false);});}
  document.addEventListener('keydown',function(e){if(e.key==='Escape'){closeAll();if(mn&&mn.classList.contains('open')){mOpen(false);mb.focus();}}});

  // ChatGPT-Frage kopieren
  [].forEach.call(document.querySelectorAll('[data-copy]'),function(cb){
    var pt=document.getElementById(cb.getAttribute('data-copy')),ok=cb.parentNode.querySelector('.copy-ok');
    cb.addEventListener('click',function(){var txt=pt.textContent.trim();
      function selTxt(){try{var r=document.createRange();r.selectNodeContents(pt);var s=getSelection();s.removeAllRanges();s.addRange(r);if(ok)ok.textContent='Markiert. Jetzt kopieren.';}catch(e){}}
      try{navigator.clipboard.writeText(txt).then(function(){if(ok)ok.textContent='Kopiert. Jetzt in ChatGPT einfügen.';},selTxt);}catch(e){selTxt();}});
  });

  // Formular: in der Vorschau nicht senden
  var live=/(^|\.)seenery\.ch$|netlify\.app$/.test(location.hostname);
  if(!live){[].forEach.call(document.querySelectorAll('[data-check-form]'),function(f){f.addEventListener('submit',function(e){e.preventDefault();var m=f.querySelector('.form-msg');if(m)m.textContent='Vorschau: Das Formular wird hier nicht gesendet. Auf seenery.ch geht die Anfrage direkt an die Automation.';});});}

  // Vorschau: Telefon/Mail nicht auslösen (sonst weisse Seite im Vorschaufenster)
  if(!live){document.addEventListener('click',function(e){var a=e.target.closest('a[href^="tel:"],a[href^="mailto:"]');if(!a)return;e.preventDefault();var n=document.querySelector('.preview-note');if(!n){n=document.createElement('div');n.className='preview-note';n.setAttribute('role','status');document.body.appendChild(n);}n.textContent='Vorschau: Auf seenery.ch öffnet dieser Link '+(a.href.indexOf('tel:')===0?'den Anruf.':'Ihr E-Mail-Programm.');clearTimeout(n._t);n._t=setTimeout(function(){n.remove();},3500);});}

  // Farbwelt-Umschalter (nur in der Vorschau vorhanden)
  var sw=document.querySelector('.theme-sw');
  if(sw){var bs=[].slice.call(sw.querySelectorAll('button[data-t]'));
    function mark(v){bs.forEach(function(b){b.setAttribute('aria-pressed',b.dataset.t===v?'true':'false');});}
    function carry(v){[].forEach.call(document.querySelectorAll('a[href*=".html"]'),function(a){var h=a.getAttribute('href');if(/^https?:/.test(h))return;var p=h.split('#'),base=p[0].split('?')[0];a.setAttribute('href',base+'?t='+v+(p[1]?'#'+p[1]:''));});}
    mark(document.documentElement.getAttribute('data-theme')||'b');carry(document.documentElement.getAttribute('data-theme')||'b');
    if(innerWidth<700)sw.classList.add('min');var x=sw.querySelector('.x'),o=sw.querySelector('.open-sw');if(x)x.addEventListener('click',function(){sw.classList.add('min');});if(o)o.addEventListener('click',function(){sw.classList.remove('min');});
    bs.forEach(function(b){b.addEventListener('click',function(){var v=b.dataset.t;document.documentElement.setAttribute('data-theme',v);mark(v);carry(v);try{localStorage.setItem('seenery-theme',v);}catch(e){}});});}
})();
