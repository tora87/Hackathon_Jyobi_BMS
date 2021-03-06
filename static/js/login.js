let canvas = null;
let ctx = null;
let errorcount = 0;

canvas = document.getElementById( 'mycanvas' );
ctx = canvas.getContext( '2d' );

const file_image = document.getElementById( 'file-image' );
const student_number = document.getElementById('studentNumber');
const student_name = document.getElementById('studentName');
const error_text = document.getElementById('errorText');
let check = false;

file_image.addEventListener( 'change', selectReadFile, false );

function selectReadFile( e ){
    const file = e.target.files;
    const reader = new FileReader();
    reader.onload = function(){
        readDrawImg( reader, canvas, 0, 0 );
    }
    reader.readAsDataURL( file[0] );
}

function readDrawImg( reader, canvas, x, y ){
    const img = readImg( reader );
    img.onload = function(){
        const w = img.width;
        const h = img.height;

        const resize = resizeWidthHeight( 1024, w, h );
        drawImgOnCav( canvas, img, x, y, resize.w, resize.h );
    }
}

function readImg( reader ){
    const result_dataURL = reader.result;
    const img = new Image();
    img.src = result_dataURL;

    return img;
}

function drawImgOnCav( canvas, img, x, y, w, h ){
    canvas.width = w;
    canvas.height = h;
    ctx.drawImage( img, x, y, w, h );

    checkQRCode();
}

function resizeWidthHeight( target_length_px, w0, h0 ){
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
    console.log("checkQRcode")
    try{
        student_number.value = '';
        student_name.value = '';
        error_text.innerText = '';

        const imageData = ctx.getImageData( 0, 0, canvas.width, canvas.height );
        const code = jsQR( imageData.data, canvas.width, canvas.height );

        if( code ){
            const regexNum = new RegExp('^[A-Za-z0-9]{1,10}$','g');
    
            const bytes = code.binaryData;
            const text_decoder = new TextDecoder('utf-8');
            const str = text_decoder.decode(Uint8Array.from(bytes).buffer);
    
            const splitStr = str.split("+");
    
            if (regexNum.test(splitStr[0])) {
                if(splitStr[1].length <= 40){
                    student_number.value = splitStr[0];
                    student_name.value = splitStr[1];
                    check = true;
                } else {
                    error_text.innerText = `???????????????????????????`;
                }
            }else{
                error_text.innerText = `?????????????????????????????????`;
            }
        }else{
            error_text.innerText = "QR????????????????????????????????????????????????\n ??????????????????????????????";
        }
    } catch(error){
        console.log(error);
        errorcount++;
        if(errorcount <= 3){
        error_text.innerText = `${error}\n????????????????????????????????????????????????????????????????????????`;
        }
        error_text.innerText = `??????????????????????????????\n ????????????????????????????????????`;
    }
}
const selected_file_name = document.getElementById('selected-file-name');

file_image.addEventListener('change',() => {
    const file = file_image.files[0];
    selected_file_name.innerText = file.name;
})

const login_btn = document.getElementById('login-btn');
const login_form = document.getElementById('stInformation');
login_btn.addEventListener('click',() => {
    if(file_image.files[0] !== undefined && check) {
        error_text.innerText = '';
        login_form.submit();
    }else{
        error_text.innerText = 'QR????????????????????????????????????????????????'
    }
})