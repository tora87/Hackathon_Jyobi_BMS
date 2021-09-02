from flask import Flask, Blueprint, render_template
import qrcode
import os

# 有原 担当
qr = Blueprint('create_qr', __name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "\\Hackathon_Jyobi_BMS\\"
print(BASE_DIR)


@qr.route('/')
def make_qr(request):
    if request.method == 'get':
        print('this is login page.')
        return render_template('qr.html')
    elif request.method == 'post':
        student_id = request.form.post['student_id']
        qr_code = makeQR()
        qr_code.generate_qr_code(student_id)
        return render_template('qr.html')


class makeQR:
    """
    任意のデータを含んだQRコードを生成する
    generated_qr_code()に、任意の数の引数(文字列)を与えると、static/images/ に
    qrcode.pngが生成される
    """
    def __init__(self):
        self.output = BASE_DIR + '/static/images/qrcode.png'
        self.qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_Q, box_size=10, border=4, )

    def generate_qr_code(self, *args: 'student_number, student_name') -> 'qr_images.png':
        text = ""
        self.qr.add_data([text + data for data in args])
        self.qr.make(fit=True)
        img = self.qr.make_image(fill_color="black", back_color="white")
        img.save(self.output)


if __name__ == '__main__':
    app = makeQR()
    app.generate_qr_code("4204101", "有原隆乃介")
