document.addEventListener('DOMContentLoaded',() => {
  const header_height = document.querySelector('.header').offsetHeight;
  const header_bottom_height = document.querySelector('.header-bottom').offsetHeight;
  const device_height = window.innerHeight;
  const title_height = document.querySelector('.page-title').offsetHeight;
  const home_container = document.querySelector('.container.home');
  const home_container_height = device_height - header_height - header_bottom_height - title_height;

  home_container.style.height = `${home_container_height}px`;
  console.log(home_container.style.height)
})