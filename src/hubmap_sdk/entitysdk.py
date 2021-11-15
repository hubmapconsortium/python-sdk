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
    def __init__(self, token=None, service_url= ''):
        self.token = token
        if service_url.endswith('/'):
            self.entity_url = service_url
        else:
            self.entity_url = service_url + '/'
        if token is not None:
            self.header = {'Authorization': 'Bearer ' + self.token}

    # Using an instance of the EntitySdk class with appropriate authentication token, service_url as well as the
    # entity_type ('donor', 'sample', etc) and a dictionary containing the data for the new entity, an entity will be
    # created via the entity-api. If the entity is created successfully, a new instance of the class corresponding to
    # the desired entity_type will be returned. If creation fails, an exception will be raised with the error message
    # from entity-api.
    def create_entity(self, entity_type, data):
        # If an entity_type given is not one of the accepted entity types, an exception will be raised.
        if entity_type.lower() not in ['donor', 'sample', 'dataset', 'upload', 'collection']:
            raise Exception("Accepted entity types are (case-insensitive):" +
                            " 'donor', 'sample', 'dataset', 'upload', or 'collection'")
        # If the request to entity-api fails, an exception will be raised.
        url = f"{self.entity_url}entities/{entity_type}"
        output = sdk_helper.make_request('post', self, url, data=data)
        # If the request to entity-api is successfully made, but a >299 response code is returned an exception is raised
        # Upon a satisfactory response from entity-api, a new instance of the desired class will be created and returned
        new_instance = sdk_helper.make_entity(output)
        return new_instance

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
            print(f"version: {output['version']}, build: {output['build']}, neo4j_connection: "
                  f"{output['neo4j_connection']}")
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

    # takes the id of an entity (HuBMAP ID or UUID) and returns an instance of the entity corresponding to the ID given
    def get_entity_by_id(self, identification):
        url = f"{self.entity_url}entities/{identification}"
        output = sdk_helper.make_request('get', self, url)
        new_instance = sdk_helper.make_entity(output)
        return new_instance

    # Takes in an id (HuBMAP ID or UUID) and returns a dictionary with the provenance tree above the given ID.
    # Optionally accepts an integer "depth" which will limit the size of the returned tree.
    def get_entity_provenance(self, identification, depth=None):
        url = f"{self.entity_url}entities/{identification}/provenance"
        depth = f"?depth={depth}"
        output = sdk_helper.make_request('get', self, url, depth)
        return output

    # returns a list of all available entity types as defined in the schema yaml
    # https://raw.githubusercontent.com/hubmapconsortium/entity-api/test-release/entity-api-spec.yaml
    # A token is not required, but if one if given, it must be valid.
    def get_entity_types(self):
        url = f"{self.entity_url}entity-types"
        output = sdk_helper.make_request('get', self, url)
        return output

    # Takes as input an entity type and returns a list of all entities within that given type. Optionally, rather than
    # Returning all of the information about the entities, it is possible to filter such that only a certain property
    # is returned for each. This is given by the value "property_key". For example, you could retrieve a list of all
    # donors, and chose to only have the uuid of each included in the list with
    # get_entities_by_type('donor', property_key='uuid')
    def get_entities_by_type(self, entity_type):
        url = f"{self.entity_url}{entity_type}/entities"
        output = sdk_helper.make_request('get', self, url)
        list_of_entities = []
        for item in output:
            new_instance = sdk_helper.make_entity(item)
            list_of_entities.append(new_instance)
        return list_of_entities

    # Takes an id (HuBMAP ID or UUID) for a collection. Returns the details of the collection in the form of a
    # dictionary with the attached datasets. If no token, or a valid token with no HuBMAP-Read group membership, then
    # only a public collection will be returned, as well as only public datasets.
    def get_collection(self, identification):
        url = f"{self.entity_url}collections/{identification}"
        output = sdk_helper.make_request('get', self, url)
        new_instance = Collection(output)
        return new_instance

    # Returns a list of all public collections. No token is required, however if one is provided, it must be valid.
    # Results can be filtered to only show individual properties with an optional argument 'property_key' which is none
    # by default. For example, to return a list of all public collections but to only have the uuid of each, call
    # get_collections('uuid')
    def get_collections(self):
        url = f"{self.entity_url}collections"
        output = sdk_helper.make_request('get', self, url)
        list_of_collections = []
        for item in output:
            new_collection = Collection(item)
            list_of_collections.append(new_collection)
        return list_of_collections

    # Creates multiple samples from the same source. Accepts a dictionary containing the information of the new entity
    # and an integer designating how many samples to create. Returns a list of the newly created sample objects.
    # 'direct_ancestor_uuid' is a required field in the dictionary. An example of a valid call would be:
    # create_multiple_samples(5, data) where data is the dictionary containing the information about the new entities.
    # A token is required.
    def create_multiple_samples(self, count, data):
        result = []
        url = f"{self.entity_url}entities/multiple-samples/{count}"
        output = sdk_helper.make_request('post', self, url, data=data)
        for item in output:
            sample_instance = Sample(item)
            result.append(sample_instance)
        return result

    # Updates the properties of a given entity. Accepts the id (HuBMAP ID or UUID) for the target entity to update, as
    # well as a dictionary with the new/updated properties for the entity. A token is required to update an entity. An
    # object is returned of the relevant class containing all the information of the entity.
    def update_entity(self, identification, data):
        url = f"{self.entity_url}entities/{identification}"
        output = sdk_helper.make_request('put', self, url, data=data)
        new_instance = sdk_helper.make_entity(output)
        return new_instance

    # Returns a list of all the ancestors of a given entity. Accepts an id (HuBMAP ID or UUID) for the target entity.
    # Optionally accepts an argument "property_key" which allows filtering by a specific property. For example, to
    # return a list of ancestors for a given entity and only returning the UUID's, use get_ancestors(id, 'UUID'). No
    # Token is required, however if a token is given, it must be valid. If no token is given or token is not for a user
    # in the Hubmap-Read group, ancestors will only be returned for public entities
    def get_ancestors(self, identification):
        list_of_ancestors = []
        url = f"{self.entity_url}ancestors/{identification}"
        output = sdk_helper.make_request('get', self, url)
        for item in output:
            new_instance = sdk_helper.make_entity(item)
            list_of_ancestors.append(new_instance)
        return list_of_ancestors

    # Returns a list of all the descendants of a given entity. Accepts an id (HuBMAP ID or UUID) for the target entity.
    # Optionally accepts an argument "property_key" which allows filtering by a specific property. For example, to
    # return a list of descendants for a given entity and only returning the UUID's, use get_descendants(id, 'UUID'). No
    # Token is required, however if a token is given, it must be valid. If no token is given or token is not for a user
    # in the Hubmap-Read group, descendants will only be returned for public entities
    def get_descendants(self, identification):
        list_of_descendants = []
        url = f"{self.entity_url}descendants/{identification}"
        output = sdk_helper.make_request('get', self, url)
        for item in output:
            new_instance = sdk_helper.make_entity(item)
            list_of_descendants.append(new_instance)
        return list_of_descendants

    # Returns a list of the parents of a given entity. Accepts an id (HuBMAP ID or UUID) for the target entity.
    # Optionally accepts an argument "property_key" which allows filtering by a specific property. For example, to
    # return a list of parents for a given entity and only returning the UUID's, use get_parents(id, 'UUID'). No
    # Token is required, however if a token is given, it must be valid. If no token is given or token is not for a user
    # in the Hubmap-Read group, parents will only be returned for public entities
    def get_parents(self, identification):
        list_of_parents = []
        url = f"{self.entity_url}parents/{identification}"
        output = sdk_helper.make_request('get', self, url)
        for item in output:
            new_instance = sdk_helper.make_entity(item)
            list_of_parents.append(new_instance)
        return list_of_parents

    # Returns a list of the children of a given entity. Accepts an id (HuBMAP ID or UUID) for the target entity.
    # Optionally accepts an argument "property_key" which allows filtering by a specific property. For example, to
    # return a list of children for a given entity and only returning the UUID's, use get_children(id, 'UUID'). No
    # Token is required, however if a token is given, it must be valid. If no token is given or token is not for a user
    # in the Hubmap-Read group, children will only be returned for public entities
    def get_children(self, identification):
        list_of_children = []
        url = f"{self.entity_url}children/{identification}"
        output = sdk_helper.make_request('get', self, url)
        for item in output:
            new_instance = sdk_helper.make_entity(item)
            list_of_children.append(new_instance)
        return list_of_children

    # Returns a list of the previous revisions of a given entity. Accepts an id (HuBMAP ID or UUID) for the target
    # entity. Optionally accepts an argument "property_key" which allows filtering by a specific property. For example,
    # to return a list of  previous revisions for a given entity and only returning the UUID's, use
    # get_previous_revisions(id, 'UUID'). No token is required, however if a token is given, it must be valid. If no
    # token is given or token is not for a user in the Hubmap-Read group, previous revisions will only be returned for
    # public entities
    def get_previous_revisions(self, identification):
        list_of_previous_revisions = []
        url = f"{self.entity_url}previous_revisions/{identification}"
        output = sdk_helper.make_request('get', self, url)
        for item in output:
            new_instance = sdk_helper.make_entity(item)
            list_of_previous_revisions.append(new_instance)
        return list_of_previous_revisions

    # Returns a list of the next revisions of a given entity. Accepts an id (HuBMAP ID or UUID) for the target
    # entity. Optionally accepts an argument "property_key" which allows filtering by a specific property. For example,
    # to return a list of  next revisions for a given entity and only returning the UUID's, use
    # get_next_revisions(id, 'UUID'). No token is required, however if a token is given, it must be valid. If no
    # token is given or token is not for a user in the Hubmap-Read group, next revisions will only be returned for
    # public entities
    def get_next_revisions(self, identification):
        url = f"{self.entity_url}next_revisions/{identification}"
        output = sdk_helper.make_request('get', self, url)
        new_instance = Dataset(output)
        return new_instance

    # Accepts an id (HuBMAP ID or UUID) for a collection and a list of datasets. Links each dataset in the list to the
    # target collection. Requires a valid Token. Returns a string "Successfully added all the specified datasets to the
    # target collection" if successful.
    def add_datasets_to_collection(self, identification, list_of_datasets):
        dataset_dictionary = {'dataset_uuids': list_of_datasets}
        url = f"{self.entity_url}collections/{identification}/add-datasets"
        sdk_helper.make_request('put', self, url, data=dataset_dictionary)
        return "Successfully added all the specified datasets to the target collection"

    # Returns the globus url for an entity given by an id (HuBMAP ID or UUID). A token is not required, but if one is
    # given it must be valid. If a token is not given, or if the user does not have HuBMAP-Read group access, a globus
    # url will only be returned for public entities
    def get_globus_url(self, identification):
        url = f"{self.entity_url}entities/{identification}/globus-url"
        r = sdk_helper.make_request('get', self, url)
        return r

    # Returns a dataset object corresponding to a given id (HuBMAP ID or UUID). A token is not required, but if one is
    # provided, it must be valid. If a token is not given, or if the user does not have HuBMAP-Read group access, then
    # the last published dataset will be returned.
    def get_dataset_latest_revision(self, identification):
        url = f"{self.entity_url}datasets/{identification}/latest-revision"
        output = sdk_helper.make_request('get', self, url)
        new_dataset = Dataset(output)
        return new_dataset

    # Takes an id to a dataset (HuBMAP ID or UUID) and returns the revision number as an integer. If the dataset of the
    # given id is not a revision of any other dataset, it will return 1. If it is the first revision of an original
    # dataset, it will return 2, and so on. A token is not required, however if a token is provided it must be valid.
    # If there is no token or the user does not have HuBMAP-Read group access, and the ID is for an unpublished dataset,
    # an error will be raised.
    def get_dataset_revision_number(self, identification):
        url = f"{self.entity_url}datasets/{identification}/revision"
        output = sdk_helper.make_request('get', self, url)
        return output

    # Retracts a published dataset. Accepts an id (HuBMAP ID or UUID) and a string retraction_reason. A token is
    # required and the user must have HuBMAP-Data-Admin access. Adds retraction reason as a property to the dataset, and
    # ads a property sub_status which is set to "retracted". Returns an dataset object for the given id with the new
    # properties.
    def retract_dataset(self, identification, retraction_reason):
        retract_json = {'retraction_reason': retraction_reason}
        url = f"{self.entity_url}datasets/{identification}/retract"
        output = sdk_helper.make_request('put', self, url, data=retract_json)
        new_dataset = Dataset(output)
        return new_dataset

    # Returns a list of all revisions from a given id (HuBMAP ID or UUID). The id can be for any revision in the chain.
    # For example, if a given is for the third revision out of 7, it will return revisions 1 through 7. The list will be
    # ordered from most recent to oldest revision. An optional boolean parameter include_dataset allows the entire
    # dataset for each revision to be included in the list. By default this is false. No token is required, however if a
    # token is given it must be valid. If no token is given, or if the user does not have HuBMAP-Read group access, only
    # public datasets will be returned. If the id given itself is not public, and a token with read access is not given,
    # an error will be raised.
    def get_revisions_list(self, identification, include_dataset=False):
        list_of_revisions = []
        if include_dataset != True:
            include_dataset = False
        url = f"{self.entity_url}datasets/{identification}/revisions"
        dataset_include = ''
        if include_dataset:
            dataset_include = '?include_dataset=True'
        output = sdk_helper.make_request('get', self, url, dataset_include)
        for item in output:
            new_instance = Dataset(item)
            list_of_revisions.append(new_instance)

    #Returns a list of all associated organs from a given id (HuBMAP ID or UUID).
    def get_associated_organs_from_dataset(self, identification):
        list_or_organs = []
        url = f"{self.entity_url}datasets/{identification}/organs"
        output = sdk_helper.make_request('get', self, url)
        for item in output:
            new_instance = Dataset(item)
            list_or_organs.append(new_instance)
        return list_or_organs
