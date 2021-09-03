from slack_bolt import App
from slack_sdk.errors import SlackApiError
import os

try:
    import slack_bot_token_file as token_file
except KeyError as e:
    print(e)
    exit()

app = App(
    token=token_file.token,
)

FILE_NAME = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "\\Hackathon_Jyobi_BMS\\static\\images" \
                                                                          "\\qrcode.png"


def send_message_for_email(mail_message: list) -> 'bool':
    """
    リストでメールアドレス、メッセージを渡すとslack_botで送信する

    Parameters
    ----------
    mail_message
        [dict1, dict2, dict3...]
    mail_message[any]
        {'email': string: mail_address, 'message': string: send_message }
    """
    for array in mail_message:
        data = get_user_id_for_email(email_addr=array['email'])
        if not data['ok']:
            exit()
        try:
            # app.client.chat_postMessage(channel=data['user']['id'], text=array['message'])  # メッセージも送信可能
            app.client.files_upload(channels=data['user']['id'], initial_comment="This is the QR code you need to log "
                                                                                 "in to the BMS system", file=FILE_NAME)
            return True
        except SlackApiError as err:
            print(err)
            return False


def get_user_id_for_email(email_addr):
    try:
        id_dict = app.client.users_lookupByEmail(email=email_addr)
    except SlackApiError:
        print('The user_id corresponding to the email address used was not found.')
        return {'ok': False}
    return id_dict


if __name__ == '__main__':
    message_list = [
        {"email": "r.arihara.sys20@morijyobi.ac.jp", "message": "いつまでも送られないQRコードの恨み"}
    ]
    send_message_for_email(message_list)
