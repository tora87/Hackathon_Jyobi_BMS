console.log('java')
// document.addEventListener('DOMContentloaded', () => {
    console.log("js");
    let canvas = null;
    let ctx = null;

    let num = 0;

    canvas = document.getElementById( 'mycanvas' );
    console.log(canvas)
    ctx = canvas.getContext( '2d' );

    const file_image = document.getElementById( 'file-image' );
    file_image.addEventListener( 'change', selectReadFile, false );

    function selectReadFile( e ){
        console.log(num++ +":selectReadFile");

        const file = e.target.files;
        const reader = new FileReader();
        reader.onload = function(){
            readDrawImg( reader, canvas, 0, 0 );
        }
        reader.readAsDataURL( file[0] );
    }

    function readDrawImg( reader, canvas, x, y ){
        console.log(num++ +":readDrawImg");

        const img = readImg( reader );
        img.onload = function(){
            const w = img.width;
            const h = img.height;

            const resize = resizeWidthHeight( 1024, w, h );
            drawImgOnCav( canvas, img, x, y, resize.w, resize.h );
        }
    }

    function readImg( reader ){
        console.log(num++ +":readImg");

        const result_dataURL = reader.result;
        const img = new Image();
        img.src = result_dataURL;

        return img;
    }

    function drawImgOnCav( canvas, img, x, y, w, h ){
        console.log(num++ +":drawImgOnCav");

        canvas.width = w;
        canvas.height = h;
        ctx.drawImage( img, x, y, w, h );

        checkQRCode();
    }

    function resizeWidthHeight( target_length_px, w0, h0 ){
        console.log(num++ +":resizeWidthHeight");

        const length = Math.max( w0, h0 );
        if( length <= target_length_px ){
            return({
            flag: false,
            w: w0,
            h: h0
            });
        }

        let w1;
        let h1;
        if( w0 >= h0 ){
            w1 = target_length_px;
            h1 = h0 * target_length_px / w0;
        }else{
            w1 = w0 * target_length_px / h0;
            h1 = target_length_px;
        }

        return({
            flag: true,
            w: parseInt( w1 ),
            h: parseInt( h1 )
        });
    }

    function checkQRCode(){
        console.log(num++ +":checkQRCode");

        const imageData = ctx.getImageData( 0, 0, canvas.width, canvas.height );
        const code = jsQR( imageData.data, canvas.width, canvas.height );
        if( code ){
            console.log( code.data)
            console.log( code.binaryData );
            const bytes = code.binaryData;
            const text_decoder = new TextDecoder('shift-jis');
            const str = text_decoder.decode(Uint8Array.from(bytes).buffer);
            console.log(str);

            alert( str );
        }else{
            alert( "No QR Code found." );
        }
    }
// })
