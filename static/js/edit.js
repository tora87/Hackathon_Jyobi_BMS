document.addEventListener('DOMContentLoaded',() => {
  const inputElements = document.querySelectorAll('input');
  const stocknum = document.getElementById('stock');
  const edit_btn = document.getElementById('edit-btn');
  const err_text = document.getElementById('add-error-text');
  const form = document.getElementById('form-edit');

  stocknum.addEventListener('focusout', () => {
    if (stocknum.value < stocknum.min) {
      stocknum.value = stocknum.min;
    }
  })

  edit_btn.addEventListener('click',() => {
    form.action = edit_btn.formAction;
    let statusArray = [];
    let status = false;
    inputElements.forEach( el => {
      if(el.value == '' || el.value.length == 0){
        el.style.border = '1px solid #f00';
        status = false;
      }else {
        el.style.border = '1px solid #000';
        status = true;
      }

      statusArray.push(status);
    })

    if(statusArray.includes(false)){
      err_text.innerText = '未入力項目があります';
    } else {
      err_text.innerText = '';
      form.submit();
    }
  })
});
