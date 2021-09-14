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

Quagga.onDetected(success => {
  const jancordEl = document.getElementById('jancord');
  const book_nameEl = document.getElementById('book-name');
  const authorEl = document.getElementById('author');
  const book_amountEl = document.getElementById('book_amount');
  const err_text = document.getElementById('add-error-text');
  const code = success.codeResult.code;
  window.alert(code);

  const canvas = document.querySelector('.drawingBuffer');
  canvas.height = 0;

  jancordEl.value = code;

  let jancord,book_name,author,book_amount;

  const getData = async(code) => {
    await fetch(`https://www.googleapis.com/books/v1/volumes?q=isbn=${code}`)
    .then(result => {
      return result.json();
    })
    .then(data => {
      if(data['totalItems'] > 0) {
        if(data['items'].length == 1){
          book_name = data['items']['volumeInfo']['title'];
          author = data['items']['volumeInfo']['authors'][0];
        }else{
          book_name = data['items'][0]['volumeInfo']['title'];
          author = data['items'][0]['volumeInfo']['authors'][0];
        }

        book_nameEl.value = book_name;
        authorEl.value = author;

      }else {
        err_text.innerHTML = 'お探しの本はありませんでした。';
      }
    })
    .catch(err => {
      console.log(err);
    }) 
  }

  getData(code);
})