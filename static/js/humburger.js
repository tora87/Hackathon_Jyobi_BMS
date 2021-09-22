document.addEventListener('DOMContentLoaded',() => {
  if(document.location.pathname != '/login-top/'){
    const menu_btn = document.querySelector('#menu-btn');
    const menu_content = document.querySelector('#humburger-menu-content');

    menu_btn.addEventListener('click',() => {
      if(menu_btn.classList.contains('active')){
        menu_btn.classList.remove('active');
        menu_content.classList.remove('active');
      }else {
        menu_btn.classList.add('active');
        menu_content.classList.add('active');
      }
    })
  }
})