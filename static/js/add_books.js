Quagga.init({
  inputStream: {
    name: 'Live',
    type: 'LiveStream',
    target: document.querySelector('#interactive'), //埋め込んだdivのID
    constraints: {
      facingMode: 'environment',
    },
  },
  locator: {
    patchSize: 'medium',
    halfSample: true,
  },
  numOfWorkers: 2,
  decoder: {
    readers: ['ean_reader'] //ISBNは基本的にこれ（他にも種類あり）
  },
  locate: true,
}, (err) => {
  if(!err) {
    Quagga.start();
  }
})

const jancordEl = document.getElementById('jancord');
const book_nameEl = document.getElementById('book-name');
const authorEl = document.getElementById('author');
const book_amountEl = document.getElementById('book_amount');
const err_text = document.getElementById('add-error-text');
const register_btn = document.getElementById('register-btn');
const form = document.getElementById('form-add');
const inputElements = document.querySelectorAll('input');


//json取得するAPI
const getData = async( code ) => {
  const URL = `https://www.googleapis.com/books/v1/volumes?q=isbn=${code}`
  let result = null;
  await fetch(URL)
  .then( response => response.json() )
  .then( data => {
    if(data['totalItems'] > 0) result = data['items'][0];
  });

  return result;
}

Quagga.onDetected(success => {

  const canvas = document.getElementsByClassName('drawingBuffer')[0];
  canvas.style.width = 0;
  canvas.style.height = 0;

  const code = success.codeResult.code;

  window.alert(code);

  jancordEl.value = code;

  const result = getData(code);

  result.then(data => {
    if( data !== null ) {
      book_nameEl.value = data['volumeInfo']['title'];
      authorEl.value = data['volumeInfo']['authors'][0];
      err_text.innerText = '';
      borderColorInit();
    } else {
      err_text.innerText = '見つかりませんでした';
      authorEl.value = '';
      book_nameEl.value = '';
    }
  })
  .catch(err => {
    console.error(err);
  })
})

const borderColorInit = () => {
  inputElements.forEach(el => {
    el.style.border = '1px solid #000';
  })
}

register_btn.addEventListener('click',() => {
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
});