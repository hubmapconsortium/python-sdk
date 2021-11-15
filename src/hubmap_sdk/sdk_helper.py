import requests
from hubmap_sdk import Donor, Dataset, Sample, Collection, Upload



def make_entity(output):
    if output['entity_type'].lower() == 'dataset':
        new_instance = Dataset(output)
    if output['entity_type'].lower() == 'donor':
        new_instance = Donor(output)
    if output['entity_type'].lower() == 'sample':
        new_instance = Sample(output)
    if output['entity_type'].lower() == 'collection':
        new_instance = Collection(output)
    if output['entity_type'].lower() == 'upload':
        new_instance = Upload(output)
    return new_instance


def make_request(method_type, instance, url, optional_argument=None, data=None):
    if optional_argument is None:
        optional_argument = ''
    if data is None:
        if instance.token is None:
            if method_type == 'get':
                r = requests.get(url + optional_argument)
            if method_type == 'put':
                r = requests.put(url + optional_argument)
            if method_type == 'post':
                r = requests.post(url + optional_argument)
        else:
            if method_type == 'get':
                r = requests.get(url + optional_argument, headers=instance.header)
            if method_type == 'put':
                r = requests.put(url + optional_argument, headers=instance.header)
            if method_type == 'post':
                r = requests.post(url + optional_argument, headers=instance.header)
    else:
        if not isinstance(data, dict):
            raise Exception("Data given must be a dictionary")
        if instance.token is None:
            if method_type == 'get':
                r = requests.get(url + optional_argument, json=data)
            if method_type == 'put':
                r = requests.put(url + optional_argument, json=data)
            if method_type == 'post':
                r = requests.post(url + optional_argument, json=data)
        else:
            if method_type == 'get':
                r = requests.get(url + optional_argument, headers=instance.header, json=data)
            if method_type == 'put':
                r = requests.put(url + optional_argument, headers=instance.header, json=data)
            if method_type == 'post':
                r = requests.post(url + optional_argument, headers=instance.header, json=data)
    if r.status_code > 299:
        # if r.status_code == 401:
        #     raise Exception("401 Authorization Required. No Token or Invalid Token Given")
        err = r.json()['error']
        error = err
        raise Exception(error)
    else:
        try:
            return r.json()
        except:
            return r.text

