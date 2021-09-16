Quagga.init({
    inputStream: {
      name: 'Live',
      type: 'LiveStream',
      target: document.querySelector('#interactive'),
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
      readers: ['ean_reader']
    },
    locate: true,
  }, (err) => {
    if(!err) {
      Quagga.start();
    }
  })

  const sendForm = document.getElementById('sendForm');
  const jancode = document.getElementById('jan');

  const errorstext = document.getElementById('errorsText');

Quagga.onDetected(success => {
    const code = success.codeResult.code;
    jancode.value = code;

    sendForm.submit();
})

// errorstext.addEventListener('getSelection', (e) => {
//   console.log(e.target.value);

//   const errorsNum = e.target.value;
//   if(errorsNum == -1) {
//     errorstext.value = 'お求めの本のデータが存在しない可能性があります、管理者にお問い合わせください。'
//   } else if(errorsNum == 0) {
//     errorstext.value = 'JANコードの読み取りに失敗しました、もう一度お願いいたします。'
//   } else if(errorsNum == 1) {
//     errorstext.value = 'データが一致しませんでした、お手数ですが再度お願いいたします。';
//   } else if(errorsNum == 2) {
//     errorstext.value = '貸出可能冊数に達しています。現在貸し出すことができません。'
//   }
//   errorstext.type = 'text';
// })