import requests
from wiliot.cloud_apis.security import security
import json
import logging
import urllib.parse
import os

log_level = logging.INFO


class WiliotCloudError(Exception):
    pass


class Client:
    def __init__(self, oauth_username=None, oauth_password=None, api_key=None,
                 env='', api_version='v1', log_file=None, logger_=None):
        # The caller must provide either a set of oauth username abd password or an API key
        if api_key is None and (oauth_password is None or oauth_username is None):
            raise Exception('Provide either an API key or a username and password')

        self.env = env+"/" if env != '' and env != 'prod' else ''
        api_path = f"https://api.wiliot.com/{self.env}{api_version}/"
        self.base_path = api_path + self.client_path
        self.headers = {
            "accept": "application/json",
            "Content-Type": "application/json"
        }
        self.auth_obj = security.WiliotAuthentication(api_path,
                                                      oauth_username=oauth_username,
                                                      oauth_password=oauth_password,
                                                      api_key=api_key)
        self.headers["Authorization"] = self.auth_obj.get_token()
        if logger_ is None:
            self.logger = logging.getLogger()
            self.logger.setLevel(log_level)
        else:
            self.logger = logging.getLogger(logger_)

        if not self.logger.hasHandlers():
            if log_file is not None:
                self.handler = logging.FileHandler(log_file)
            else:
                self.handler = logging.StreamHandler()
            self.handler.setLevel(log_level)
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            self.handler.setFormatter(formatter)
            self.logger.addHandler(self.handler)

    def _renew_token(self):
        if self.auth_obj.token_expired():
            self.headers["Authorization"] = self.auth_obj.get_token()

    def _get(self, path, params=None):
        self._renew_token()
        response = requests.get(self.base_path+path, headers=self.headers, params=params)
        message = response.json()
        if isinstance(message, str):
            message = {"data": message}
        message.update({'status_code': response.status_code})
        if response.status_code != 200:
            raise WiliotCloudError(message)
        return message

    def _get_file(self, path, out_file, params=None):
        """
        A version of _get which expects to get back a text/csv and requires the user to provide a file
        pointer to write the content to
        """
        self._renew_token()
        response = requests.get(self.base_path+path, headers=self.headers, params=params)
        out_file.write(response.text)
        if response.status_code != 200:
            raise WiliotCloudError(response.text)
        return response.ok

    def _put(self, path, payload):
        self._renew_token()
        response = requests.put(self.base_path+urllib.parse.quote(path), headers=self.headers, data=json.dumps(payload))
        message = response.json()
        if isinstance(message,str):
            message = {"data":message}
        message.update({'status_code':response.status_code})
        if response.status_code != 200:
            raise WiliotCloudError(message)
        return message

    def _post(self, path, payload, params=None, files=None):
        self._renew_token()
        response = requests.post(self.base_path+urllib.parse.quote(path), headers=self.headers,
                                 data=json.dumps(payload) if payload is not None else None,
                                 params=params)
        message = response.json()
        if isinstance(message,str):
            message = {"data":message}
        message.update({'status_code':response.status_code})
        if response.status_code != 200:
            raise WiliotCloudError(message)
        return message

    def _post_with_files(self, path, files, payload=None, params=None):
        self._renew_token()
        if payload is None:
            payload = {}
        self.headers.pop('Content-Type', None)
        response = requests.request("POST", self.base_path+urllib.parse.quote(path), headers=self.headers,
                                    data=payload,
                                    params=params,
                                    files=files)
        message = response.json()
        if isinstance(message, str):
            message = {"data": message}
        message.update({'status_code': response.status_code})
        if response.status_code != 200:
            raise WiliotCloudError(message)
        return message

    def _delete(self, path, payload=None):
        self._renew_token()
        response = requests.delete(self.base_path + urllib.parse.quote(path), headers=self.headers,
                                   data=json.dumps(payload) if payload is not None else None)
        if response.status_code != 200:
            raise WiliotCloudError(response.text)
        message = response.json()
        return message
