import requests


def make_request(method_type, instance, url, optional_argument=None, data=None):
    if optional_argument is None:
        optional_argument = ''
    if data is None:
        if instance.token is None:
            if method_type == 'get':
                r = requests.get(url + optional_argument)
            if method_type == 'put':
                r = requests.get(url + optional_argument)
            if method_type == 'post':
                r = requests.get(url + optional_argument)
        else:
            if method_type == 'get':
                r = requests.get(url + optional_argument, headers=instance.header)
            if method_type == 'put':
                r = requests.get(url + optional_argument, headers=instance.header)
            if method_type == 'post':
                r = requests.get(url + optional_argument, headers=instance.header)
    else:
        if instance.token is None:
            if method_type == 'get':
                r = requests.get(url + optional_argument, json=data)
            if method_type == 'put':
                r = requests.get(url + optional_argument, json=data)
            if method_type == 'post':
                r = requests.get(url + optional_argument, json=data)
        else:
            if method_type == 'get':
                r = requests.get(url + optional_argument, headers=instance.header, json=data)
            if method_type == 'put':
                r = requests.get(url + optional_argument, headers=instance.header, json=data)
            if method_type == 'post':
                r = requests.get(url + optional_argument, headers=instance.header, json=data)
    if r.status_code > 299:
        if r.status_code == 401:
            raise Exception("401 Authorization Required. No Token or Invalid Token Given")
        err = r.json()['error']
        error = err
        raise Exception(error)
    else:
        try:
            return r.json()
        except:
            return r.text

