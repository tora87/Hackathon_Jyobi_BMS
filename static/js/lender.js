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

Quagga.onDetected(success => {
    const code = success.codeResult.code;
    jancode.value = code;

    sendForm.submit();
})
