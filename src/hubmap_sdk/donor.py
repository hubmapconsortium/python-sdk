from hubmap_sdk import Entity


class Donor(Entity):
    def __init__(self, instance):
        super().__init__(instance)
        for key in instance:
            setattr(self, key, instance[key])
        # if instance['registered_doi'] is not None:
        #     self.registered_doi = instance['registered_doi']
        # if instance['doi_url'] is not None:
        #     self.doi_url = instance['doi_url']
        # if instance['creators'] is not None:
        #     self.creators = instance['creators']
        # if instance['contacts'] is not None:
        #     self.contacts = instance['contacts']
        # if instance['description'] is not None:
        #     self.description = instance['description']
        # if instance['data_access_level'] is not None:
        #     self.data_access_level = instance['data_access_level']
        # if instance['image_files'] is not None:
        #     self.image_files = instance['image_files']
        # if instance['image_files_to_remove'] is not None:
        #     self.image_files_to_remove = instance['image_files_to_remove']
        # if instance['image_files_to_add'] is not None:
        #     self.image_files_to_add = instance['image_files_to_add']
        # if instance['protocol_url'] is not None:
        #     self.protocol_url = instance['protocol_url']
        # if instance['metadata'] is not None:
        #     self.metadata = instance['metadata']
        # if instance['submission_id'] is not None:
        #     self.submission_id = instance['submission_id']
        # if instance['lab_donor_id'] is not None:
        #     self.lab_donor_id = instance['lab_donor_id']
        # if instance['group_name'] is not None:
        #     self.group_uuid = instance['group_uuid']
        # if instance['group_name'] is not None:
        #     self.group_name = instance['group_name']
        # if instance['label'] is not None:
        #     self.label = instance['label']
