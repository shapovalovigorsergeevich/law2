
const header=document.querySelector('.header');
window.addEventListener('scroll',()=>header.classList.toggle('scrolled',scrollY>60));
const io=new IntersectionObserver(entries=>entries.forEach(e=>e.isIntersecting&&e.target.classList.add('visible')),{threshold:.1});
document.querySelectorAll('.reveal').forEach(el=>io.observe(el));

const modal=document.getElementById('modal');
document.querySelectorAll('[data-consult]').forEach(a=>a.addEventListener('click',e=>{e.preventDefault();modal.classList.add('open')}));
document.querySelector('[data-close]').addEventListener('click',()=>modal.classList.remove('open'));
modal.addEventListener('click',e=>{if(e.target===modal)modal.classList.remove('open')});

const form=document.getElementById('leadForm');
form.addEventListener('submit',e=>{
 e.preventDefault();
 const data=Object.fromEntries(new FormData(form));
 const subject=encodeURIComponent('Заявка с сайта — '+data.name);
 const body=encodeURIComponent(`Имя: ${data.name}\nТелефон: ${data.phone}\nВопрос: ${data.message}`);
 window.location.href=`mailto:info@shapovalov-law.ru?subject=${subject}&body=${body}`;
});
document.querySelector('.burger').addEventListener('click',()=>{
 const menu=document.querySelector('.menu');
 const open=menu.dataset.open==='1';
 menu.dataset.open=open?'0':'1';
 menu.style.display=open?'none':'flex';
 menu.style.position='absolute';menu.style.top='82px';menu.style.left='0';menu.style.right='0';
 menu.style.padding='20px';menu.style.background='#0a121b';menu.style.flexDirection='column';
});
