from donor import donor
from sample import sample
from upload import upload
from collection import collection
from dataset import dataset
import requests


class entity_api:
    def __init__(self, token=None, location=None):
        self.token = token
        self.location = location
        self.header = {'Authorization': 'Bearer ' + self.token}
        if self.location.lower() == "prod" or self.location is None:
            self.entity_url = "entity-api.hubmapconsortium.org/"
        if self.location.lower == "test":
            self.entity_url = "entity-api.test.hubmapconsortium.org/"
        if self.location.lower() == "dev":
            self.entity_url = "entity-api.dev.hubmapconsortium.org/"
        if self.location.lower() == "stage":
            self.entity_url = "entity-api.stage.hubmapconsortium.org/"
        if self.location.lower() == "localhost":
            self.entity_url = "localhost:8383"
        else:
            raise Exception("Argument 'location' if included must be case-insensitive: 'LOCALHOST', 'DEV', 'TEST', "
                            "'STAGE', or 'PROD'. If not included, it will be assumed as 'PROD'")

    # Using an instance of entity-api class with appropriate authentication token, location ('TEST', 'PROD', 'DEV', etc)
    # as well as the entity_type ('donor', 'sample', etc) and a dictionary containing the data for the new entity, an
    # entity will be created via the entity-api. If the entity is created successfully, a new instance of the class
    # corresponding to the desired entity will be returned. If creation fails, an exception will be raised with the
    # error message from entity-api.
    def create_entity(self, entity_type, data):
        header = {'Authorization': 'Bearer ' + self.token}
        if entity_type.lower() not in ['donor, sample, dataset, upload, collection']:
            raise Exception("Accepted entity types are (case-insensitive):" +
                            " 'donor', 'sample', 'dataset', 'upload', or 'collection'")
        if self.token is None:
            raise Exception("The entity-api instance used does not have a token attribute. A valid token is required"
                            "to create an entity")
        url = self.entity_url + 'entities/' + entity_type
        try:
            r = requests.post(url, headers=header, json=data)
        except Exception as e:
            raise Exception(e)
        if r.status_code < 400:
            output = r.json()
            if entity_type.lower == "donor":
                new_donor = entity_api.create_donor(output)
                return new_donor
            if entity_type.lower() == "dataset":
                new_dataset = entity_api.create_dataset(output)
                return new_dataset
            if entity_type.lower() == 'sample':
                new_sample = entity_api.create_sample(output)
                return new_sample
            if entity_type.lower() == 'upload':
                new_upload = entity_api.create_upload(output)
                return new_upload
            if entity_type.lower() == 'collection':
                new_collection = entity_api.create_collection(output)
                return new_collection
        else:
            err = r.json()['error']
            raise Exception(err)

    # returns "Hello! This is HuBMAP Entity API service :)". It is a convenient way to verify that the desired server
    # is operational without requiring any particular authorization
    def index(self):
        try:
            r = requests.get(self.entity_url)
        except Exception as e:
            raise Exception(e)
        return r

    # returns the version, build, and neo4j_connection status and prints the same information out.
    def get_status(self):
        try:
            r = requests.get(self.entity_url + 'status')
        except Exception as e:
            print(e)
            return e
        output = r.json()
        if r.status_code < 400:
            print('version: ' + output['version'] + ', build: ' + output['build'] + ', neo4j_connecton:'
                  + output['neo4j_connection'])
        return output

    def get_ancestor_organs(self, identification):
        if self.token is None:
            try:
                r = requests.get(self.entity_url + 'entities/' + identification + '/ancestor-organs')
            except Exception as e:
                raise Exception(e)
        else:
            try:
                r = requests.get(self.entity_url + 'entities/' + identification + '/ancestor-organs',
                                 headers=self.header)
            except Exception as e:
                raise Exception(e)
        if r.status_code > 399:
            err = r.json()['error']
            raise Exception(err)
        else:
            return r.json()

    # takes the id of an entity (HuBMAP ID or UUID) and returns a
    def get_entity_by_id(self, identification, query_filter=None):
        if self.token is None:
            if query_filter is None:
                try:
                    r = requests.get(self.entity_url + "entities/" + identification)
                except Exception as e:
                    raise Exception(e)
            else:
                try:
                    r = requests.get(self.entity_url + "entities/" + identification + "?property=" + query_filter)
                except Exception as e:
                    raise Exception(e)
        else:
            if query_filter is None:
                try:
                    r = requests.get(self.entity_url + "entities/" + identification, headers=self.header)
                except Exception as e:
                    raise Exception(e)
            else:
                try:
                    r = requests.get(self.entity_url + "entities/" + identification + "?property=" + query_filter,
                                     headers=self.header)
                except Exception as e:
                    raise Exception(e)
        if r.status_code > 399:
            err = r.json()['error']
            raise Exception(err)
        else:
            return r.json()

    # Takes in an id (HuBMAP ID or UUID) and returns a dictionary with the provenance tree above the given ID.
    # Optionally accepts an integer "depth" which will limit the size of the returned tree.
    def get_entity_provenance(self, identification, depth=None):
        if self.token is None:
            if depth is None:
                try:
                    r = requests.get(self.entity_url + "entities/" + identification + "/provenance")
                except Exception as e:
                    raise Exception(e)
            else:
                try:
                    r = requests.get(self.entity_url + "entities/" +
                                     identification + "/provenance" + "?depth=" + depth)
                except Exception as e:
                    raise Exception(e)
        else:
            if depth is None:
                try:
                    r = requests.get(self.entity_url + "entities/" + identification +
                                     "/provenance", headers=self.header)
                except Exception as e:
                    raise Exception(e)
            else:
                try:
                    r = requests.get(self.entity_url + "entities/" + identification + "/provenance" + "?depth=" +
                                     depth, headers=self.header)
                except Exception as e:
                    raise Exception(e)
        if r.status_code > 399:
            err = r.json()['error']
            raise Exception(err)
        else:
            return r.json()

    def get_entity_types(self):
        if self.token is None:
            try:
                r = requests.get(self.entity_url + "entity-types/")
            except Exception as e:
                raise Exception(e)
        else:
            try:
                r = requests.get(self.entity_url + "entity-types/", headers=self.header)
            except Exception as e:
                raise Exception(e)
        if r.status_code > 399:
            err = r.json()['error']
            raise Exception(err)
        else:
            return r.json()

    def get_entities_by_type(self, entity_type, property_key=None):
        if self.token is None:
            raise Exception("A token is required for get_entities_by_type. The instance of entity-api calling "
                            "get_entities_by_type has a token value of None")
        else:
            if property_key is None:
                try:
                    r = requests.get(self.entity_url + entity_type + "/entities", headers=self.header)
                except Exception as e:
                    raise Exception(e)
            else:
                try:
                    r = requests.get(self.entity_url + entity_type + "/entities?property=" + property_key,
                                     headers=self.header)
                except Exception as e:
                    raise Exception(e)
        if r.status_code > 399:
            err = r.json()['error']
            raise Exception(err)
        else:
            return r.json()

    def get_collection(self, identification):
        if self.token is None:
            try:
                r = requests.get(self.entity_url + "collections/" + identification)
            except Exception as e:
                raise Exception(e)
        else:
            try:
                r = requests.get(self.entity_url + "collections/" + identification, headers=self.header)
            except Exception as e:
                raise Exception(e)
        if r.status_code > 399:
            err = r.json()['error']
            raise Exception(err)
        else:
            return r.json()

    def get_collections(self, property_key=None):
        if self.token is None:
            if property_key is None:
                try:
                    r = requests.get(self.entity_url + "collections")
                except Exception as e:
                    raise Exception(e)
            else:
                try:
                    r = requests.get(self.entity_url + "collections" + property_key)
                except Exception as e:
                    raise Exception(e)
        else:
            if property_key is None:
                try:
                    r = requests.get(self.entity_url + "collections", headers=self.header)
                except Exception as e:
                    raise Exception(e)
            else:
                try:
                    r = requests.get(self.entity_url + "collections" + property_key, headers=self.header)
                except Exception as e:
                    raise Exception(e)

        if r.status_code > 399:
            err = r.json()['error']
            raise Exception(err)
        else:
            return r.json()

    def create_multiple_samples(self, count, data):
        result = []
        try:
            r = requests.post(self.entity_url + "entities/multiple-samples/" + count, headers=self.header, json=data)
        except Exception as e:
            raise Exception(e)
        if r.status_code > 399:
            err = r.json()['error']
            raise Exception(err)
        else:
            sample_list = r.json()
            for output in sample_list:
                sample_instance = entity_api.create_sample(output)
                result.append(sample_instance)
        return result

    def update_entity(self, identification, data):
        try:
            r = requests.put(self.entity_url + 'entities/' + identification, headers=self.header, json=data)
        except Exception as e:
            raise Exception(e)
        output = r.json()
        if output['entity_type'].lower() == 'dataset':
            new_instance = entity_api.create_dataset(output)
        if output['entity_type'].lower() == 'donor':
            new_instance = entity_api.create_donor(output)
        if output['entity_type'].lower() == 'sample':
            new_instance = entity_api.create_sample(output)
        if output['entity_type'].lower() == 'collection':
            new_instance = entity_api.create_collection(output)
        if output['entity_type'].lower() == 'upload':
            new_instance = entity_api.create_upload(output)
        return new_instance

    def get_ancestors(self, identification, property_key):
        if self.token is None:
            if property_key is None:
                try:
                    r = requests.get(self.entity_url + "ancestors/" + identification)
                except Exception as e:
                    raise Exception(e)
            else:
                try:
                    r = requests.get(self.entity_url + "ancestors/" + identification + "?property=" + property_key)
                except Exception as e:
                    raise Exception(e)
        else:
            if property_key is None:
                try:
                    r = requests.get(self.entity_url + "ancestors/" + identification, headers=self.header)
                except Exception as e:
                    raise Exception(e)
            else:
                try:
                    r = requests.get(self.entity_url + "ancestors/" + identification + "?property=" + property_key,
                                     headers=self.header)
                except Exception as e:
                    raise Exception(e)
        if r.status_code > 399:
            err = r.json()['error']
            raise Exception(err)
        else:
            return r.json()

    def get_descendants(self, identification, property_key):
        if self.token is None:
            if property_key is None:
                try:
                    r = requests.get(self.entity_url + "descendants/" + identification)
                except Exception as e:
                    raise Exception(e)
            else:
                try:
                    r = requests.get(self.entity_url + "descendants/" + identification + "?property=" + property_key)
                except Exception as e:
                    raise Exception(e)
        else:
            if property_key is None:
                try:
                    r = requests.get(self.entity_url + "descendants/" + identification, headers=self.header)
                except Exception as e:
                    raise Exception(e)
            else:
                try:
                    r = requests.get(self.entity_url + "descendants/" + identification + "?property=" + property_key,
                                     headers=self.header)
                except Exception as e:
                    raise Exception(e)
        if r.status_code > 399:
            err = r.json()['error']
            raise Exception(err)
        else:
            return r.json()

    def get_parents(self, identification, property_key):
        if self.token is None:
            if property_key is None:
                try:
                    r = requests.get(self.entity_url + 'parents/' + identification)
                except Exception as e:
                    raise Exception(e)
            else:
                try:
                    r = requests.get(self.entity_url + 'parents/' + identification + '?property=' + property_key)
                except Exception as e:
                    raise Exception(e)
        else:
            if property_key is None:
                try:
                    r = requests.get(self.entity_url + 'parents/' + identification, headers=self.header)
                except Exception as e:
                    raise Exception(e)
            else:
                try:
                    r = requests.get(self.entity_url + 'parents/' + identification + '?property=' + property_key,
                                     headers=self.header)
                except Exception as e:
                    raise Exception(e)
        if r.status_code > 399:
            err = r.json()['error']
            raise Exception(err)
        else:
            return r.json()

    @staticmethod
    def create_sample(output):
        new_sample = sample(created_timestamp=output['created_timestamp'],
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
        new_donor = donor(created_timestamp=output['created_timestamp'],
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
        new_dataset = dataset(created_timestamp=output['created_timestamp'],
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
        new_upload = upload(created_timestamp=output['created_timestamp'],
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
        new_collection = collection(created_timestamp=output['created_timestamp'],
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
