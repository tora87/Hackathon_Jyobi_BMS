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

  const sendForm = document.getElementById('sendForm');
  sendForm.innerHTML += `<p>hello</p>`;


Quagga.onDetected(success => {
    const code = success.codeResult.code;
    window.alert(code);

    const name = document.getElementById('name');
    name.value = code;
    console.log(code);

    // const sendForm = document.getElementById('sendForm');
    console.log(sendForm);

    // sendForm.submit();
})