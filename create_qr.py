from flask import Flask, Blueprint, render_template, redirect, request, url_for, session
import qrcode
import os
from smtplib import SMTP
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

from databases import create_qr_db
import slack_send_message

# 有原 担当
qr = Blueprint('create_qr', __name__, url_prefix='/generate-qr')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "\\Hackathon_Jyobi_BMS\\"


# url http://127.0.0.1:5000/generate-qr/
# qrコード送信時、
# qr = makeQR()
# qr.generate_qr_code(student_id='any', student_name="any")
# flg = slack_send_message.send_message_for_email(message_list = [
#         {"email": "your_email_address@morijyobi.ac.jp", "message": "any message for send"}
#     ]
# )

@qr.route('/', methods=['GET'])
def make_qr():
    if "user_id" not in session:  # ? セッションの有無
        return redirect("/")
    user_data = create_qr_db.select_all_user()
    number_scope = create_qr_db.select_number_scope()
    user_list = []
    for array in user_data:
        user_list.append({
            'user_id': array[0],
            'name': array[1],
            'email': array[2],
        })
    return render_template('qr.html', user_data=user_list, number_scope=number_scope)

@qr.route('/search', methods=['POST'])
def make_qr_searchuser():
    if "user_id" not in session:  # ? セッションの有無
        return redirect("/")
    selectnum = request.form.get("selectnum")
    keywords = request.form.get("keywords")
    if selectnum != '':
        user_data = create_qr_db.select_search_user(selectnum)
    if keywords is not None:
        user_data = create_qr_db.select_keyword_user(keywords)
    if keywords is not None and selectnum != '':
        user_data = create_qr_db.select_key_num_user(selectnum,keywords)
    number_scope = create_qr_db.select_number_scope()
    user_list = []
    for array in user_data:
        user_list.append({
            'user_id': array[0],
            'name': array[1],
            'email': array[2],
        })
    return render_template('qr.html', user_data=user_list, number_scope=number_scope)

@qr.route('/', methods=['POST'])
def send_qr():
    if "user_id" not in session:  # ? セッションの有無
        return redirect("/")

    # クライアント側から送られてきたデータから、選択されたユーザの学籍番号(student_id)を取得する
    user_id = request.form.get('user_id')
    user_id = is_integer(s=user_id)

    if not user_id:
        return redirect(url_for('create_qr.make_qr'))

    # user_id = 4204101  # テスト用
    user_data = create_qr_db.select_for_generation_user_data(student_id=int(user_id))
    if user_data is None:
        # 該当する学籍番号が存在しなかった場合
        return redirect(url_for('create_qr.make_qr'))

    qr = makeQR()
    qr.generate_qr_code(student_id=int(user_data[0]), student_name=str(user_data[1]))

    flg = slack_send_message.send_message_for_email(mail_message=[
        {"email": user_data[2], "message": "新たに生成されたQRコードです。\n次回ログインからはこちらを使用してください。"}
    ])

    if flg:
        return render_template('home.html')  # ホーム画面を表示する処理を作成次第、そちらへ変更する
    else:
        return redirect(url_for('create_qr.make_qr'))


class makeQR:
    """
    任意のデータを含んだQRコードを生成する
    """

    def __init__(self):
        self.output = BASE_DIR + '/static/images/qrcode.png'
        self.qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_Q, box_size=10, border=4, )

    def generate_qr_code(self, **kwargs: 'student_id, student_name'):
        """
        受け取った引数を、QRコードとして生成する。static/images/qrcode.pngとして保存される

        Parameters
        ----------
        kwargs['student_id'] : integer
            対象の生徒の学籍番号。
        kwargs['student_name'] : string
            対象の生徒の名前。
        """
        self.qr.add_data(str(kwargs['student_id']) + '+' + str(kwargs['student_name']))
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
        if 'Subject' in kwargs:
            self.subject = kwargs['Subject']
        else:
            self.subject = "BMSシステムからのお知らせ"
        if 'body' in kwargs:
            self.body = kwargs['body']
        else:
            self.body = " このメールは自動送信です。\n\n BMSシステムへログインする際に使用できるQRコードを添付いたします。\n"
        if 'id' in kwargs:
            self.ID = kwargs['id']  # 固定のアドレスに変更も可
        else:
            self.id = " "  # 固定のメールアドレス記入場所
        if 'password' in kwargs:
            self.PASS = kwargs['password']
        else:
            self.PASS = " "  # 固定のメールアドレス
        self.HOST = "smtp.gmail.com"
        self.PORT = 587

    def send_email(self, sender_email_address: 'recipient email_address') -> 'error or None':
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
        try:
            img_data = open(BASE_DIR + '\\static\\images\\qrcode.png', 'rb')
            msg.attach(MIMEImage(img_data.read()))
        except IndexError as e:
            return e
        except IOError as e:
            return e
        msg["Subject"] = self.subject
        msg["From"] = self.ID
        msg["To"] = sender_email_address
        server = SMTP(self.HOST, self.PORT)
        server.starttls()

        server.login(self.ID, self.PASS)

        server.send_message(msg)

        server.quit()

        return None


def is_integer(s: 'str'):
    """
    引数で受け取った値が１０進数の整数値に変換可能か判定する。変換可能ならば、変換して値を返す。

    Parameters
    ---------
    s : string
        判定する文字列

    Return
    ---------
    data : False or integer
        変換不可能ならFalse, 変換可能なら返還後の整数値
    """
    try:
        int(s, 10)
    except ValueError as e:
        return False
    else:
        return int(s, 10)


if __name__ == '__main__':
    # text_subject = "テスト送信" text_body = "BMSシステム内の、メール送信機能のテストです。\nQRコードが添付されていれば成功です。" email = Email(
    # Subject=text_subject, body=text_body, id="r.arihara.sys20sub@gmail.com", password="111000oooiii")  #
    # 送信元のメールアドレス、パスワードを記入 return_value = email.send_email("r.arihara.sys20@morijyobi.ac.jp")  # 送信先のメールアドレスを記入 if
    # return_value is not None: print("エラー: メール送信時にエラーが発生しました\n", return_value)

    qr = makeQR()
    qr.generate_qr_code(student_id='4204101', student_name="有原隆乃介")
