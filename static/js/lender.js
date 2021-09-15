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

  let failNum = 0;

Quagga.onDetected(success => {
    const code = success.codeResult.code;
    // window.alert(code);

    jancode.value = code;

    sendForm.submit();
})

function failread(){
  failNum++;
  console.log(failNum);
}