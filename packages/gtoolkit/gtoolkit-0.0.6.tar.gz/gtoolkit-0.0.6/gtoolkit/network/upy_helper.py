"""
    上传文件到又拍云
"""
import hmac
import base64
import hashlib
import datetime
import requests
from loguru import logger


class UPYUpload:
    session = requests.session()

    def __init__(self, bucket: str, username: str, password: str):
        self._bucket = bucket
        self._username = username
        self._password = password

    @staticmethod
    def utc_date():
        return datetime.datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')

    def sign_str(self, method, uri, policy=None):
        utc_date = self.utc_date()
        key = hashlib.md5(self._password.encode(encoding='utf-8')).hexdigest()
        if policy is None:
            msg = method + "&" + uri + "&" + utc_date
        else:
            msg = method + "&" + uri + "&" + utc_date + "&" + policy
        h = hmac.new(bytes(key, 'utf-8'), bytes(msg, 'utf-8'), digestmod='sha1')
        return "UPYUN " + self._username + ":" + str(base64.b64encode(h.digest()), 'utf-8')

    def upload(self, local_path, remote_path):
        url = 'http://v0.api.upyun.com/' + self._bucket + remote_path

        headers = {
            'Date': self.utc_date(),
            'Authorization': self.sign_str("PUT", "/" + self._bucket + remote_path)
        }

        try:
            with open(local_path, 'rb') as f:
                resp = self.__class__.session.put(url, data=f, headers=headers, timeout=60)

            if resp.status_code == 200:
                return True
            else:
                return False
        except Exception as e:
            logger.error(f'上传失败：{e}')
            return False
