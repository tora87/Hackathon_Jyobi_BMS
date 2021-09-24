const sendForm = document.getElementById('sendForm');
const jancode = document.getElementById('jan');

let jancode_list = [];

Quagga.init({
    inputStream: {
      name: 'Live',
      type: 'LiveStream',
      target: document.querySelector('#photo-area'),
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

let count = 0;

Quagga.onDetected(success => {
    const code = success.codeResult.code;
    jancode.value = code;

    jancode_list.push(code);

    for(let i = 1; i < jancode_list.length; i++){
      if(jancode_list[i-1] == jancode_list[i]) {
        count++;
      }
    }

    if(count >= 200){
      sendForm.submit();
    }
})

Quagga.onProcessed(data => {
  const ctx = Quagga.canvas.ctx.overlay;
  const canvas = Quagga.canvas.dom.overlay;

  if (!data) { 
    return; 
  }

  if (data.boxes) {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    const hasNotRead = box => box !== data.box;
    data.boxes.filter(hasNotRead).forEach(box => {
      Quagga.ImageDebug.drawPath(box, { x: 0, y: 1 }, ctx, { color: 'green', lineWidth: 2 });
    });

    if (data.box) {  
      Quagga.ImageDebug.drawPath(data.box, { x: 0, y: 1 }, ctx, { color: 'blue', lineWidth: 2 });
    }

    if (data.codeResult && data.codeResult.code) {
      Quagga.ImageDebug.drawPath(data.line, { x: 'x', y: 'y' }, ctx, { color: 'red', lineWidth: 3 });
    }
  }
})
