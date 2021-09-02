from flask import Flask, Blueprint, render_template
import qrcode
import os
from smtplib import SMTP
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart


# 有原 担当
qr = Blueprint('create_qr', __name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "\\Hackathon_Jyobi_BMS\\"


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
    """
    def __init__(self):
        self.output = BASE_DIR + '/static/images/qrcode.png'
        self.qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_Q, box_size=10, border=4, )

    def generate_qr_code(self, **kwargs: 'student_id, student_name') -> 'qr_images.png':
        """
        受け取った引数を、QRコードとして生成する。static/images/qrcode.pngとして保存される

        Parameters
        ----------
        kwargs['student_id'] : integer
            対象の生徒の学籍番号。
        kwargs['student_name'] : string
            対象の生徒の名前。
        """
        text = ""
        self.qr.add_data(kwargs['student_id'] + '+' + kwargs['student_name'])
        self.qr.make(fit=True)
        img = self.qr.make_image(fill_color="black", back_color="white")
        img.save(self.output)


class Email:
    """
    QRコードを添付したhtmlメールを送信する
    """
    def __init__(self, **kwargs):
        """
        コンストラクタ

        Parameters
        ----------
        kwargs['Subject'] : String
            送信するメールの題(タイトル)。
        kwargs['body'] : string
            送信するメールの本題部分。
        kwargs['id'] : string(email)
            送信元のメールアドレス
        kwargs['password'] : password
            送信元のメールアドレスのパスワード
        """
        self.subject = kwargs['Subject']
        self.body = kwargs['body']
        self.ID = kwargs['id']  # 固定のアドレスに変更も可
        self.PASS = kwargs['password']
        self.HOST = "smtp.gmail.com"
        self.PORT = 587

    def send_email(self, sender_email_address: 'recipient email_address'):
        """
        受け取った引数のメールアドレスに宛てて、QRコードを添付したメールを送信する。

        Parameters
        ----------
        sender_email_address : strnig(email)
            送信先のメールアドレス
        """
        msg = MIMEMultipart()
        self.body.replace("\n", "<br>")
        
        msg.attach(MIMEText(self.body, "html"))
        img_data = open(BASE_DIR+'\\static\\images\\qrcode.png', 'rb')
        msg.attach(MIMEImage(img_data.read()))

        msg["Subject"] = self.subject
        msg["From"] = self.ID
        msg["To"] = sender_email_address
        server = SMTP(self.HOST, self.PORT)
        server.starttls()

        server.login(self.ID, self.PASS)

        server.send_message(msg)

        server.quit()


if __name__ == '__main__':
    text_subject = "テスト送信"
    text_body = "BMSシステム内の、メール送信機能のテストです。\nQRコードが添付されていれば成功です。"
    email = Email(Subject=text_subject, body=text_body, id="", password="")  # 送信元のメールアドレス、パスワードを記入
    email.send_email("")  # 送信先のメールアドレスを記入
