
window.onscroll = function(){
  var top = window.pageYOffset || document.documentElement.scrollTop;
  var nav = document.getElementsByClassName("navbar")[0];
  if (top > 10) {
    nav.classList.add('shadow-header');
  } else {
    nav.classList.remove('shadow-header');
  }
}

function printHTML() { 
  if (window.print) { 
    window.print();
  }
}

// function de checkbox ingredientes
function selectAll(){
  const all = document.getElementsByName("ingrediente");
  const all_array = [...all];
  let seleccionar = false;
  if (all_array.some(item => !item.checked)) {
    seleccionar = true;  
  }
  all.forEach(item => item.checked = seleccionar);
}
    

function copiarEnlace() {
  var aux = document.createElement('input');
  aux.setAttribute('value', window.location.href.split('?')[0].split('#')[0]);
  document.body.appendChild(aux);
  aux.select();
  document.execCommand('copy');
  document.body.removeChild(aux);
  var aviso = document.createElement('div');
  aviso.setAttribute('id', 'aviso');
  var text = document.createTextNode('Enlace copiada');
  aviso.appendChild(text);
  document.getElementById("titulo").appendChild(aviso);
  window.load = setTimeout('document.getElementById("titulo").removeChild(aviso)', 2000);
}      
