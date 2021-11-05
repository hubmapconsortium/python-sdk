from hubmap_sdk import sdk_helper


class SearchSdk:

    def __init__(self, token, service_url=#https://search-api.hubmapconsortium.org/):
         ''):
        self.token = token
        if service_url.endswith('/'):
            self.search_url = service_url
        else:
            self.search_url = service_url + '/'
        self.header = {'Authorization': 'Bearer ' + self.token}

    def assaytypes(self, key=None):
        url = f"{self.search_url}assaytype"
        output = sdk_helper.make_request('get', self, url, optional_argument=key)
        return output

    def assayname(self, name):
        url = f"{self.search_url}assaytype/{name}"
        output = sdk_helper.make_request('get', self, url)
        return output

    def search(self, data):
        url = f"{self.search_url}search"
        output = sdk_helper.make_request('post', self, url, data=data)
        return output

    def search_by_index(self, data, index_without_prefix):
        url = f"{self.search_url}{index_without_prefix}/search"
        output = sdk_helper.make_request('post', self, url, data=data)
        return output


    def count(self, data):
        url = f"{self.search_url}count"
        output = sdk_helper.make_request('get', self, url, data=data)
        return output

    def count_by_index(self, data, index_without_previs):
        url = f"{self.search_url}{index_without_previs}/count"
        output = sdk_helper.make_request('get', self, url, data=data)
        return output

    def indices(self):
        url = f"{self.search_url}indices"
        output = sdk_helper.make_request('get', self, url)
        indices = output['indices']
        return indices

    def status(self):
        url = f"{self.search_url}status"
        output = sdk_helper.make_request('get', self, url)
        return output

    def reindex(self, uuid):
        url = f"{self.search_url}reindex/{uuid}"
        output = sdk_helper.make_request('put', self, url)
        if output[1] == 202:
            return output[0]
        else:
            return f"reindex failed for uuid: {uuid}"

    def reindex_all(self):
        url = f"{self.search_url}reindex-all"
        output = sdk_helper.make_request('put', self, url)
        if output[1] == 202:
            return output[0]
        else:
            return f"reindex-all failed"
