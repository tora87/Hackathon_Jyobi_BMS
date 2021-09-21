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

    console.log(code);

    // sendForm.submit();
})

Quagga.onProcessed(data => {
  const ctx = Quagga.canvas.ctx.overlay;
  const canvas = Quagga.canvas.dom.overlay;

  if (!data) { return; }

  // 認識したバーコードを囲む
  if (data.boxes) {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    const hasNotRead = box => box !== data.box;
    data.boxes.filter(hasNotRead).forEach(box => {
      Quagga.ImageDebug.drawPath(box, { x: 0, y: 1 }, ctx, { color: 'green', lineWidth: 2 });
    });

     // 読み取ったバーコードを囲む
     if (data.box) {
      Quagga.ImageDebug.drawPath(data.box, { x: 0, y: 1 }, ctx, { color: 'blue', lineWidth: 2 });
    }

    // 読み取ったバーコードに線を引く
    if (data.codeResult && data.codeResult.code) {
      Quagga.ImageDebug.drawPath(data.line, { x: 'x', y: 'y' }, ctx, { color: 'red', lineWidth: 3 });
    }
}
})
