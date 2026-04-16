import time
import requests


class WeChatNotifier:
    TOKEN_URL = "https://api.weixin.qq.com/cgi-bin/token"
    SEND_URL = "https://api.weixin.qq.com/cgi-bin/message/template/send"

    def __init__(self, app_id: str, app_secret: str, template_id: str, user_openid: str):
        self.app_id = app_id
        self.app_secret = app_secret
        self.template_id = template_id
        self.user_openid = user_openid
        self._token = None
        self._token_expires_at = 0

    def _get_access_token(self) -> str:
        if self._token and time.time() < self._token_expires_at:
            return self._token

        url = (
            f"{self.TOKEN_URL}?grant_type=client_credential"
            f"&appid={self.app_id}&secret={self.app_secret}"
        )
        resp = requests.get(url)
        data = resp.json()
        self._token = data["access_token"]
        self._token_expires_at = time.time() + data.get("expires_in", 7200) - 60
        return self._token

    def send(self, message: str) -> bool:
        try:
            token = self._get_access_token()
            url = f"{self.SEND_URL}?access_token={token}"
            payload = {
                "touser": self.user_openid,
                "template_id": self.template_id,
                "data": {
                    "first": {"value": message},
                    "keyword1": {"value": time.strftime("%Y-%m-%d %H:%M:%S")},
                    "remark": {"value": "Dota 2 Auto Accept"},
                },
            }
            resp = requests.post(url, json=payload)
            result = resp.json()
            if result.get("errcode", -1) != 0:
                print(f"WeChat send error: {result.get('errmsg', 'unknown')}")
                return False
            return True
        except Exception as e:
            print(f"WeChat notification failed: {e}")
            return False
