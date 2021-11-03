from hubmap_sdk import Donor, Sample, Collection, Upload, Dataset, sdk_helper
import requests

"""
The entity-api class is the mechanism by which functions of the entity api are interacted. 
Create an instance of the class and give it the optional arguments 'token' and 'service_url'. Token is a Globus
nexus authentication token, and service_url is the base url to the entity webservice you would like to use. These are
 "https://entity-apihubmapconsortium.org" for the production sever, "https://entity-api.dev.hubmapconsortium.org" for 
 the DEV server, "https://entity-api.test.hubmapconsortium.org" for the TEST server, 
 "https://entity-api.stage.hubmapconsortium.org" for the STAGE server or use a localhost. If no token is given, only 
 functionality designated for public access will be usable. If no service_url is given, all requests will be made 
 against the production server
"""


class EntitySdk:
    def __init__(self, token=None, service_url=#'https://entity-api.hubmapconsortium.org/'):
        ''):
        self.token = token
        if service_url.endswith('/'):
            self.entity_url = service_url
        else:
            self.entity_url = service_url + '/'
        self.header = {'Authorization': 'Bearer ' + self.token}

    # Using an instance of the EntitySdk class with appropriate authentication token, service_url as well as the
    # entity_type ('donor', 'sample', etc) and a dictionary containing the data for the new entity, an entity will be
    # created via the entity-api. If the entity is created successfully, a new instance of the class corresponding to
    # the desired entity_type will be returned. If creation fails, an exception will be raised with the error message
    # from entity-api.
    def create_entity(self, entity_type, data):
        # The create entity action requires a valid token
        if self.token is None:
            raise Exception("The entity-api instance used does not have a token attribute. A valid token is required"
                            "to create an entity")

        # If an entity_type given is not one of the accepted entity types, an exception will be raised.
        if entity_type.lower() not in ['donor, sample, dataset, upload, collection']:
            raise Exception("Accepted entity types are (case-insensitive):" +
                            " 'donor', 'sample', 'dataset', 'upload', or 'collection'")

        # If the request to entity-api fails, an exception will be raised.
        r = requests.post(self.entity_url + 'entities/' + entity_type, headers=self.header, json=data)

        # If the request to entity-api is successfully made, however a 300-599 response code is returned, an exception
        # Is raised
        if r.status_code > 299:
            err = r.json()['error']
            error = f"{r.status_code} {err}"
            raise Exception(error)

        # Upon a satisfactory response from entity-api, a new instance of the desired class will be created and returned
        output = r.json()
        if entity_type.lower == "donor":
            new_donor = Donor(output)
            return new_donor
        if entity_type.lower() == "dataset":
            new_dataset = Dataset(output)
            return new_dataset
        if entity_type.lower() == 'sample':
            new_sample = Sample(output)
            return new_sample
        if entity_type.lower() == 'upload':
            new_upload = Upload(output)
            return new_upload
        if entity_type.lower() == 'collection':
            new_collection = Collection(output)
            return new_collection

    # returns the version, build, and neo4j_connection status and prints the same information out.
    def get_status(self):
        try:
            r = requests.get(self.entity_url + 'status')

        # if the request fails, in this case an error is not raised. The error message is instead returned since this
        # may be a desired outcome.
        except Exception as e:
            print(e)
            return e
        output = r.json()
        if r.status_code < 300:
            print('version: ' + output['version'] + ', build: ' + output['build'] + ', neo4j_connecton:'
                  + output['neo4j_connection'])
        return output

    # Takes an id (HuBMAP id or UUID) for a sample or dataset and will return a list of organs that are ancestors to
    # the given sample or Dataset. This method does not require authorization, however if a token is given, it must be
    # valid, and if no token is given or if the token does not belong to HuBMAP-Read group, ancestor organ info will
    # only be returned for public entities.
    def get_ancestor_organs(self, identification):
        url = f"{self.entity_url}entities/{identification}/ancestor-organs"
        output = sdk_helper.make_request('get', self, url)
        organs_list = []
        for item in output:
            organ = Sample(item)
            organs_list.append(organ)
        return organs_list
        # if 5 == 4:
        #    if self.token is None:
        #        r = requests.get(self.entity_url + 'entities/' + identification + '/ancestor-organs')
        #    else:
        #        r = requests.get(self.entity_url + 'entities/' + identification + '/ancestor-organs',
        #                         headers=self.header)
        #    if r.status_code > 299:
        #        err = r.json()['error']
        #        error = f"{r.status_code} {err}"
        #        raise Exception(error)
        #    else:
        #        return r.json()

    # takes the id of an entity (HuBMAP ID or UUID) and returns an instance of the entity corresponding to the ID given
    def get_entity_by_id(self, identification, query_filter=None):
        url = f"{self.entity_url}entities/{identification}"
        r = sdk_helper.make_request('get', self, url, query_filter)
        # if 5 == 4:
        #     if self.token is None:
        #         if query_filter is None:
        #             r = requests.get(self.entity_url + "entities/" + identification)
        #         else:
        #             r = requests.get(self.entity_url + "entities/" + identification + "?property=" + query_filter)
        #     else:
        #         if query_filter is None:
        #             r = requests.get(self.entity_url + "entities/" + identification, headers=self.header)
        #         else:
        #             r = requests.get(self.entity_url + "entities/" + identification + "?property=" + query_filter,
        #                              headers=self.header)
        #     if r.status_code > 399:
        #         err = r.json()['error']
        #         raise Exception(err)

        entity_type = r['entity_type']
        if entity_type.lower() == 'dataset':
            new_instance = Dataset(r)
        if entity_type.lower() == 'donor':
            new_instance = Donor(r)
        if entity_type.lower() == 'sample':
            new_instance = Sample(r)
        if entity_type.lower() == 'collection':
            new_instance = Collection(r)
        if entity_type.lower() == 'upload':
            new_instance = Upload(r)
        return new_instance

    # Takes in an id (HuBMAP ID or UUID) and returns a dictionary with the provenance tree above the given ID.
    # Optionally accepts an integer "depth" which will limit the size of the returned tree.
    def get_entity_provenance(self, identification, depth=None):
        url = f"{self.entity_url}entities/{identification}/provenance"
        r = sdk_helper.make_request('get', self, url, depth)
        # if 5 == 4:
        #     if self.token is None:
        #         if depth is None:
        #             r = requests.get(self.entity_url + "entities/" + identification + "/provenance")
        #         else:
        #             r = requests.get(self.entity_url + "entities/" +
        #                              identification + "/provenance" + "?depth=" + depth)
        #     else:
        #         if depth is None:
        #             r = requests.get(self.entity_url + "entities/" + identification +
        #                              "/provenance", headers=self.header)
        #         else:
        #             r = requests.get(self.entity_url + "entities/" + identification + "/provenance" + "?depth=" +
        #                              depth, headers=self.header)
        #     if r.status_code > 399:
        #         err = r.json()['error']
        #         raise Exception(err)
        return r

    # returns a list of all available entity types as defined in the schema yaml
    # https://raw.githubusercontent.com/hubmapconsortium/entity-api/test-release/entity-api-spec.yaml
    # A token is not required, but if one if given, it must be valid.
    def get_entity_types(self):
        url = f"{self.entity_url}entity-types/"
        r = sdk_helper.make_request('get', self, url)
        # if 5 == 4:
        #     if self.token is None:
        #         r = requests.get(self.entity_url + "entity-types/")
        #     else:
        #         r = requests.get(self.entity_url + "entity-types/", headers=self.header)
        #     if r.status_code > 399:
        #         err = r.json()['error']
        #         raise Exception(err)
        return r

    # Takes as input an entity type and returns a list of all entities within that given type. Optionally, rather than
    # Returning all of the information about the entities, it is possible to filter such that only a certain property
    # is returned for each. This is given by the value "property_key". For example, you could retrieve a list of all
    # donors, and chose to only have the uuid of each included in the list with
    # get_entities_by_type('donor', property_key='uuid')
    def get_entities_by_type(self, entity_type, property_key=None):
        url = f"{self.entity_url}{entity_type}/entities"
        r = sdk_helper.make_request('get', self, url, property_key)
        # if 5 == 4:
        #     if self.token is None:
        #         raise Exception("A token is required for get_entities_by_type. The instance of entity-api calling "
        #                         "get_entities_by_type has a token value of None")
        #     else:
        #         if property_key is None:
        #             r = requests.get(self.entity_url + entity_type + "/entities", headers=self.header)
        #         else:
        #             r = requests.get(self.entity_url + entity_type + "/entities?property=" + property_key,
        #                              headers=self.header)
        #     if r.status_code > 399:
        #         err = r.json()['error']
        #         raise Exception(err)
        return r

    # Takes an id (HuBMAP ID or UUID) for a collection. Returns the details of the collection in the form of a
    # dictionary with the attached datasets. If no token, or a valid token with no HuBMAP-Read group membership, then
    # only a public collection will be returned, as well as only public datasets.
    def get_collection(self, identification):
        url = f"{self.entity_url}collections/{identification}"
        r = sdk_helper.make_request('get', self, url)
        # if 5 == 4:
        #     if self.token is None:
        #         r = requests.get(self.entity_url + "collections/" + identification)
        #     else:
        #         r = requests.get(self.entity_url + "collections/" + identification, headers=self.header)
        #     if r.status_code > 399:
        #         err = r.json()['error']
        #         raise Exception(err)
        return r

    # Returns a list of all public collections. No token is required, however if one is provided, it must be valid.
    # Results can be filtered to only show individual properties with an optional argument 'property_key' which is none
    # by default. For example, to return a list of all public collections but to only have the uuid of each, call
    # get_collections('uuid')
    def get_collections(self, property_key=None):
        url = f"{self.entity_url}collections"
        r = sdk_helper.make_request('get', self, url, property_key)
        # if 5 == 4:
        #     if self.token is None:
        #         if property_key is None:
        #             r = requests.get(self.entity_url + "collections")
        #         else:
        #             r = requests.get(self.entity_url + "collections" + property_key)
        #     else:
        #         if property_key is None:
        #             r = requests.get(self.entity_url + "collections", headers=self.header)
        #         else:
        #             r = requests.get(self.entity_url + "collections" + property_key, headers=self.header)
        #
        #     if r.status_code > 399:
        #         err = r.json()['error']
        #         raise Exception(err)
        return r

    # Creates multiple samples from the same source. Accepts a dictionary containing the information of the new entity
    # and an integer designating how many samples to create. Returns a list of the newly created sample objects.
    # 'direct_ancestor_uuid' is a required field in the dictionary. An example of a valid call would be:
    # create_multiple_samples(5, data) where data is the dictionary containing the information about the new entities.
    # A token is required.
    def create_multiple_samples(self, count, data):
        result = []
        r = requests.post(self.entity_url + "entities/multiple-samples/" + count, headers=self.header, json=data)
        if r.status_code > 299:
            err = r.json()['error']
            raise Exception(err)
        else:
            sample_list = r.json()
            for output in sample_list:
                sample_instance = EntitySdk.create_sample(output)
                result.append(sample_instance)
        return result

    # Updates the properties of a given entity. Accepts the id (HuBMAP ID or UUID) for the target entity to update, as
    # well as a dictionary with the new/updated properties for the entity. A token is required to update an entity. An
    # object is returned of the relevant class containing all the information of the entity.
    def update_entity(self, identification, data):
        r = requests.put(self.entity_url + 'entities/' + identification, headers=self.header, json=data)
        output = r.json()
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

    # Returns a list of all the ancestors of a given entity. Accepts an id (HuBMAP ID or UUID) for the target entity.
    # Optionally accepts an argument "property_key" which allows filtering by a specific property. For example, to
    # return a list of ancestors for a given entity and only returning the UUID's, use get_ancestors(id, 'UUID'). No
    # Token is required, however if a token is given, it must be valid. If no token is given or token is not for a user
    # in the Hubmap-Read group, ancestors will only be returned for public entities
    def get_ancestors(self, identification, property_key=None):
        url = f"{self.entity_url}ancestors/{identification}"
        r = sdk_helper.make_request('get', self, url, property_key)
        # if 5 == 4:
        #     if self.token is None:
        #         if property_key is None:
        #             r = requests.get(self.entity_url + "ancestors/" + identification)
        #         else:
        #             r = requests.get(self.entity_url + "ancestors/" + identification + "?property=" + property_key)
        #     else:
        #         if property_key is None:
        #             r = requests.get(self.entity_url + "ancestors/" + identification, headers=self.header)
        #         else:
        #             r = requests.get(self.entity_url + "ancestors/" + identification + "?property=" + property_key,
        #                              headers=self.header)
        #     if r.status_code > 399:
        #         err = r.json()['error']
        #         raise Exception(err)
        return r

    # Returns a list of all the descendants of a given entity. Accepts an id (HuBMAP ID or UUID) for the target entity.
    # Optionally accepts an argument "property_key" which allows filtering by a specific property. For example, to
    # return a list of descendants for a given entity and only returning the UUID's, use get_descendants(id, 'UUID'). No
    # Token is required, however if a token is given, it must be valid. If no token is given or token is not for a user
    # in the Hubmap-Read group, descendants will only be returned for public entities
    def get_descendants(self, identification, property_key=None):
        url = f"{self.entity_url}descendants/{identification}"
        r = sdk_helper.make_request('get', self, url, property_key)
        # if 5 == 4:
        #     if self.token is None:
        #         if property_key is None:
        #             r = requests.get(self.entity_url + "descendants/" + identification)
        #         else:
        #             r = requests.get(self.entity_url + "descendants/" + identification + "?property=" + property_key)
        #     else:
        #         if property_key is None:
        #             r = requests.get(self.entity_url + "descendants/" + identification, headers=self.header)
        #         else:
        #             r = requests.get(self.entity_url + "descendants/" + identification + "?property=" + property_key,
        #                              headers=self.header)
        #     if r.status_code > 399:
        #         err = r.json()['error']
        #         raise Exception(err)
        return r

    # Returns a list of the parents of a given entity. Accepts an id (HuBMAP ID or UUID) for the target entity.
    # Optionally accepts an argument "property_key" which allows filtering by a specific property. For example, to
    # return a list of parents for a given entity and only returning the UUID's, use get_parents(id, 'UUID'). No
    # Token is required, however if a token is given, it must be valid. If no token is given or token is not for a user
    # in the Hubmap-Read group, parents will only be returned for public entities
    def get_parents(self, identification, property_key=None):
        url = f"{self.entity_url}parents/{identification}"
        r = sdk_helper.make_request('get', self, url, property_key)
        # if 5 == 4:
        #     if self.token is None:
        #         if property_key is None:
        #             r = requests.get(self.entity_url + 'parents/' + identification)
        #         else:
        #             r = requests.get(self.entity_url + 'parents/' + identification + '?property=' + property_key)
        #     else:
        #         if property_key is None:
        #             r = requests.get(self.entity_url + 'parents/' + identification, headers=self.header)
        #         else:
        #             r = requests.get(self.entity_url + 'parents/' + identification + '?property=' + property_key,
        #                              headers=self.header)
        #     if r.status_code > 399:
        #         err = r.json()['error']
        #         raise Exception(err)
        return r

    # Returns a list of the children of a given entity. Accepts an id (HuBMAP ID or UUID) for the target entity.
    # Optionally accepts an argument "property_key" which allows filtering by a specific property. For example, to
    # return a list of children for a given entity and only returning the UUID's, use get_children(id, 'UUID'). No
    # Token is required, however if a token is given, it must be valid. If no token is given or token is not for a user
    # in the Hubmap-Read group, children will only be returned for public entities
    def get_children(self, identification, property_key=None):
        url = f"{self.entity_url}children/{identification}"
        r = sdk_helper.make_request('get', self, url, property_key)
        # if 5 == 4:
        #     if self.token is None:
        #         if property_key is None:
        #             r = requests.get(self.entity_url + 'children/' + identification)
        #         else:
        #             r = requests.get(self.entity_url + 'children/' + identification + '?property=' + property_key)
        #     else:
        #         if property_key is None:
        #             r = requests.get(self.entity_url + 'children/' + identification, headers=self.header)
        #         else:
        #             r = requests.get(self.entity_url + 'children/' + identification + '?property=' + property_key,
        #                              headers=self.header)
        #     if r.status_code > 399:
        #         err = r.json()['error']
        #         raise Exception(err)
        return r

    # Returns a list of the previous revisions of a given entity. Accepts an id (HuBMAP ID or UUID) for the target
    # entity. Optionally accepts an argument "property_key" which allows filtering by a specific property. For example,
    # to return a list of  previous revisions for a given entity and only returning the UUID's, use
    # get_previous_revisions(id, 'UUID'). No token is required, however if a token is given, it must be valid. If no
    # token is given or token is not for a user in the Hubmap-Read group, previous revisions will only be returned for
    # public entities
    def get_previous_revisions(self, identification, property_key=None):
        url = f"{self.entity_url}previous_revisions/{identification}"
        r = sdk_helper.make_request('get', self, url, property_key)
        # if 5 == 4:
        #     if self.token is None:
        #         if property_key is None:
        #             r = requests.get(self.entity_url + 'previous_revisions/' + identification)
        #         else:
        #             r = requests.get(self.entity_url + 'previous_revisions/' + identification + '?property=' +
        #                                  property_key)
        #     else:
        #         if property_key is None:
        #             r = requests.get(self.entity_url + 'previous_revisions/' + identification, headers=self.header)
        #         else:
        #             r = requests.get(self.entity_url + 'previous_revisions/' + identification + '?property=' +
        #                              property_key, headers=self.header)
        #     if r.status_code > 399:
        #         err = r.json()['error']
        #         raise Exception(err)
        return r

    # Returns a list of the next revisions of a given entity. Accepts an id (HuBMAP ID or UUID) for the target
    # entity. Optionally accepts an argument "property_key" which allows filtering by a specific property. For example,
    # to return a list of  next revisions for a given entity and only returning the UUID's, use
    # get_next_revisions(id, 'UUID'). No token is required, however if a token is given, it must be valid. If no
    # token is given or token is not for a user in the Hubmap-Read group, next revisions will only be returned for
    # public entities
    def get_next_revisions(self, identification, property_key=None):
        url = f"{self.entity_url}next_revisions/{identification}"
        r = sdk_helper.make_request('get', self, url, property_key)
        # if 5 == 4:
        #     if self.token is None:
        #         if property_key is None:
        #             r = requests.get(self.entity_url + 'next_revisions/' + identification)
        #         else:
        #             r = requests.get(self.entity_url + 'next_revisions/' + identification + '?property=' + property_key)
        #     else:
        #         if property_key is None:
        #             r = requests.get(self.entity_url + 'next_revisions/' + identification, headers=self.header)
        #         else:
        #             r = requests.get(self.entity_url + 'next_revisions/' + identification + '?property=' + property_key,
        #                              headers=self.header)
        #     if r.status_code > 399:
        #         err = r.json()['error']
        #         raise Exception(err)
        return r

    # Accepts an id (HuBMAP ID or UUID) for a collection and a list of datasets. Links each dataset in the list to the
    # target collection. Requires a valid Token. Returns a string "Successfully added all the specified datasets to the
    # target collection" if successful.
    def add_datasets_to_collection(self, identification, list_of_datasets):
        dataset_list = list_of_datasets
        dataset_dictionary = {'dataset_uuids': dataset_list}
        r = requests.put(self.entity_url + 'collections/' + identification + '/add-datasets', headers=self.header,
                         json=dataset_dictionary)
        if r.status_code > 399:
            err = r.json()['error']
            raise Exception(err)
        else:
            return "success"

    # Returns the globus url for an entity given by an id (HuBMAP ID or UUID). A token is not required, but if one is
    # given it must be valid. If a token is not given, or if the user does not have HuBMAP-Read group access, a globus
    # url will only be returned for public entities
    def get_globus_url(self, identification):
        url = f"{self.entity_url}entities/{identification}/globus-url"
        r = sdk_helper.make_request('get', self, url)
        # if 5 == 4:
        #     if self.token is None:
        #         r = requests.get(self.entity_url + 'entities/' + identification + '/globus-url')
        #     else:
        #         r = requests.get(self.entity_url + 'entities/' + identification + '/globus-url', headers=self.header)
        #     if r.status_code > 399:
        #         err = r.json()['error']
        #         raise Exception(err)
        return r

    # Returns a dataset object corresponding to a given id (HuBMAP ID or UUID). A token is not required, but if one is
    # provided, it must be valid. If a token is not given, or if the user does not have HuBMAP-Read group access, then
    # the last published dataset will be returned.
    def get_dataset_latest_revision(self, identification):
        url = f"{self.entity_url}datasets/{identification}/latest-revision"
        r = sdk_helper.make_request('get', self, url)
        # if 5 == 4:
        #     if self.token is None:
        #         r = requests.get(self.entity_url + 'datasets/' + identification + '/latest-revision')
        #     else:
        #         r = requests.get(self.entity_url + 'datasets/' + identification + '/latest-revision',
        #                          headers=self.header)
        #     if r.status_code > 399:
        #         err = r.json()['error']
        #         raise Exception(err)
        new_dataset = EntitySdk.create_dataset(r)
        return new_dataset

    # Takes an id to a dataset (HuBMAP ID or UUID) and returns the revision number as an integer. If the dataset of the
    # given id is not a revision of any other dataset, it will return 1. If it is the first revision of an original
    # dataset, it will return 2, and so on. A token is not required, however if a token is provided it must be valid.
    # If there is no token or the user does not have HuBMAP-Read group access, and the ID is for an unpublished dataset,
    # an error will be raised.
    def get_dataset_revision_number(self, identification):
        url = f"{self.entity_url}datasets/{identification}/revision"
        r = sdk_helper.make_request('get', self, url)
        # if 5 == 4:
        #     if self.token is None:
        #         r = requests.get(self.entity_url + 'datasets/' + identification + '/revision')
        #     else:
        #         r = requests.get(self.entity_url + 'datasets/' + identification + '/revision', headers=self.header)
        #     if r.status_code > 399:
        #         err = r.json()
        #         raise Exception(err)
        return r

    # Retracts a published dataset. Accepts an id (HuBMAP ID or UUID) and a string retraction_reason. A token is
    # required and the user must have HuBMAP-Data-Admin access. Adds retraction reason as a property to the dataset, and
    # ads a property sub_status which is set to "retracted". Returns an dataset object for the given id with the new
    # properties.
    def retract_dataset(self, identification, retraction_reason):
        retract_json = {'retraction_reason': retraction_reason}
        r = requests.get(self.entity_url + 'datasets/' + identification + '/retract', headers=self.header,
                         json=retract_json)
        if r.status_code > 399:
            err = r.json()
            raise Exception(err)
        else:
            new_dataset = EntitySdk.create_dataset(r.json())
            return new_dataset

    # Returns a list of all revisions from a given id (HuBMAP ID or UUID). The id can be for any revision in the chain.
    # For example, if a given is for the third revision out of 7, it will return revisions 1 through 7. The list will be
    # ordered from most recent to oldest revision. An optional boolean parameter include_dataset allows the entire
    # dataset for each revision to be included in the list. By default this is false. No token is required, however if a
    # token is given it must be valid. If no token is given, or if the user does not have HuBMAP-Read group access, only
    # public datasets will be returned. If the id given itself is not public, and a token with read access is not given,
    # an error will be raised.
    def get_revisions_list(self, identification, include_dataset=False):
        if self.token is None:
            if include_dataset is False:
                r = requests.get(self.entity_url + 'datasets/' + identification + '/revisions')
            else:
                r = requests.get(self.entity_url + 'datasets/' + identification + '/revisions?include_dataset=True')
        else:
            if include_dataset is False:
                r = requests.get(self.entity_url + 'datasets/' + identification + '/revisions', headers=self.header)
            else:
                r = requests.get(self.entity_url + 'datasets/' + identification + '/revisions?include_dataset=True',
                                 headers=self.header)
        if r.status_code > 399:
            err = r.json()
            raise Exception(err)
        else:
            return r.json()

    @staticmethod
    def create_sample(output):
        new_sample = Sample(created_timestamp=output['created_timestamp'],
                            created_by_user_displayname=output['created_by_user_displayname'],
                            created_by_user_email=output['created_by_user_email'],
                            created_by_user_sub=output['created_by_user_sub'], uuid=output['uuid'],
                            hubmap_id=output['hubmap_id'],
                            last_modified_user_timestamp=output['last_modified_user_timestamp'],
                            last_modified_user_sub=output['last_modified_user_sub'],
                            last_modified_user_email=output['last_modified_user_email'],
                            last_modified_user_displayname=output['last_modified_user_displayname'],
                            entity_type=output['entity_type'],
                            registered_doi=output['registered_doi'], doi_url=output['doi_url'],
                            creators=output['creators'], contacts=output['contacts'],
                            description=output['description'], data_access_level=output['data_access_level'],
                            specimen_type=output['specimen_type'],
                            specimen_type_other=output['specimen_type_other'],
                            protocol_url=output['protocol_url'], group_uuid=output['group_uuid'],
                            group_name=output['group_name'], organ=output['organ'],
                            organ_other=output['organ_other'],
                            direct_ancestor_uuid=output['direct_ancestor_uuid'],
                            submission_id=output['submission_id'],
                            lab_tissue_sample_id=output['lab_tissue_sample_id'],
                            rui_location=output['rui_location'], metadata=output['metadata'],
                            visit=output['visit'], image_files=output['image_files'],
                            image_files_to_remove=output['image_files_to_remove'],
                            image_files_to_add=output['image_files_to_add'],
                            metadata_files=output['metadata_files'],
                            metadata_files_to_add=output['metadata_files_to_add'],
                            metadata_files_to_remove=output['metadata_files_to_remove'])
        return new_sample

    @staticmethod
    def create_donor(output):
        new_donor = Donor(created_timestamp=output['created_timestamp'],
                          created_by_user_displayname=output['created_by_user_displayname'],
                          created_by_user_email=output['created_by_user_email'],
                          created_by_user_sub=output['created_by_user_sub'], uuid=output['uuid'],
                          hubmap_id=output['hubmap_id'],
                          last_modified_user_timestamp=output['last_modified_user_timestamp'],
                          last_modified_user_sub=output['last_modified_user_sub'],
                          last_modified_user_email=output['last_modified_user_email'],
                          last_modified_user_displayname=output['last_modified_user_displayname'],
                          entity_type=output['entity_type'], registered_doi=output['registered_doi'],
                          doi_url=output['doi_url'], creators=output['creators'], contacts=output['contacts'],
                          description=output['description'], data_access_level=output['data_access_level'],
                          image_files=output['image_files'], image_files_to_add=output['image_files_to_add'],
                          image_files_to_remove=output['image_files_to_remove'],
                          protocol_url=output['protocol'], metadata=output['metadata'],
                          submission_id=output['submission_id'], lab_donor_id=output['lab_donor_id'],
                          group_uuid=output['group_uuid'], group_name=output['group_name'],
                          label=output['label'])
        return new_donor

    @staticmethod
    def create_dataset(output):
        new_dataset = Dataset(created_timestamp=output['created_timestamp'],
                              created_by_user_displayname=output['created_by_user_displayname'],
                              created_by_user_email=output['created_by_user_email'],
                              created_by_user_sub=output['created_by_user_sub'], uuid=output['uuid'],
                              hubmap_id=['hubmap_id'],
                              last_modified_user_timestamp=output['last_modified_user_timestamp'],
                              last_modified_user_email=output['last_modified_user_email'],
                              last_modified_user_sub=output['last_modified_user_sub'],
                              last_modified_user_displayname=output['last_modified_user_displayname'],
                              entity_type=output['entity_type'], registered_doi=output['registered_doi'],
                              doi_url=output['doi_url'], creators=output['creators'],
                              contacts=output['contact'], antibodies=output['antibodies'],
                              description=output['description'], data_access_level=output['data_access_level'],
                              contains_human_genetic_sequences=output['contains_human_genetic_sequences'],
                              status=output['status'], title=output['title'], data_types=output['data_types'],
                              upload=output['upload'], collections=output['collections'],
                              contributors=output['contributors'], direct_ancestors=output['direct_ancestors'],
                              published_timestamp=output['published_timestamp'],
                              published_user_displayname=output['published_user_displayname'],
                              published_user_sub=output['published_user_sub'],
                              published_user_email=output['published_user_email'],
                              ingest_metadata=output['ingest_metadata'],
                              local_directory_rel_path=output['local_directory_rel_path'],
                              group_uuid=output['group_uuid'], group_name=output['group_name'],
                              previous_revision_uuid=output['previous_revision_uuid'],
                              next_revision_uuid=output['next_revision_uuid'],
                              thumbnail_file=output['thumbnail_file'],
                              thumbnail_file_to_add=output['thumbnail_file_to_add'],
                              thumbnail_file_to_remove=output['thumbnail_file_to_remove'])
        return new_dataset

    @staticmethod
    def create_upload(output):
        new_upload = Upload(created_timestamp=output['created_timestamp'],
                            created_by_user_displayname=output['created_by_user_displayname'],
                            created_by_user_email=output['created_by_user_email'],
                            created_by_user_sub=output['created_by_user_sub'], uuid=output['uuid'],
                            hubmap_id=output['hubmap_id'],
                            last_modified_user_timestamp=output['last_modified_user_timestamp'],
                            last_modified_user_sub=output['last_modified_user_sub'],
                            last_modified_user_email=output['last_modified_user_email'],
                            last_modified_user_displayname=output['last_modified_user_displayname'],
                            entity_type=output['entity_type'], description=output['description'],
                            title=output['title'], status=output['status'],
                            validation_message=output['validation_message'], group_uuid=output['group_uuid'],
                            group_name=output['group_name'],
                            dataset_uuids_to_link=output['dataset_uuids_to_link'],
                            dataset_uuids_to_unlink=output['dataset_uuids_to_unlink'],
                            datasets=output['datasets'])
        return new_upload

    @staticmethod
    def create_collection(output):
        new_collection = Collection(created_timestamp=output['created_timestamp'],
                                    created_by_user_displayname=output['created_by_user_displayname'],
                                    created_by_user_email=output['created_by_user_email'],
                                    created_by_user_sub=output['created_by_user_sub'], uuid=output['uuid'],
                                    hubmap_id=output['hubmap_id'],
                                    last_modified_user_timestamp=output['last_modified_user_timestamp'],
                                    last_modified_user_sub=output['last_modified_user_sub'],
                                    last_modified_user_email=output['last_modified_user_email'],
                                    last_modified_user_displayname=output['last_modified_user_displayname'],
                                    datasets=output['datasets'], entity_type=output['entity_type'],
                                    registered_doi=output['registered_doi'], doi_url=output['doi_url'],
                                    creators=output['creators'], contacts=output['contacts'],
                                    title=output['title'])
        return new_collection
