from hubmap_sdk import Entity


class Donor(Entity):
    def __init__(self, created_timestamp, created_by_user_displayname, created_by_user_email, created_by_user_sub, uuid,
                 hubmap_id, last_modified_user_timestamp, last_modified_user_sub, last_modified_user_email,
                 last_modified_user_displayname, entity_type, registered_doi, doi_url, creators, contacts, description,
                 data_access_level, image_files, image_files_to_add, image_files_to_remove, protocol_url, metadata,
                 submission_id, lab_donor_id, group_uuid, group_name, label):
        super().__init__(created_timestamp, created_by_user_displayname, created_by_user_email, created_by_user_sub,
                         uuid, hubmap_id, last_modified_user_timestamp, last_modified_user_sub,
                         last_modified_user_email, last_modified_user_displayname, entity_type)
        if registered_doi is not None:
            self.registered_doi = registered_doi
        if doi_url is not None:
            self.doi_url = doi_url
        if creators is not None:
            self.creators = creators
        if contacts is not None:
            self.contacts = contacts
        if description is not None:
            self.description = description
        if data_access_level is not None:
            self.data_access_level = data_access_level
        if image_files is not None:
            self.image_files = image_files
        if image_files_to_remove is not None:
            self.image_files_to_remove = image_files_to_remove
        if image_files_to_add is not None:
            self.image_files_to_add = image_files_to_add
        if protocol_url is not None:
            self.protocol_url = protocol_url
        if metadata is not None:
            self.metadata = metadata
        if submission_id is not None:
            self.submission_id = submission_id
        if lab_donor_id is not None:
            self.lab_donor_id = lab_donor_id
        if group_name is not None:
            self.group_uuid = group_uuid
        if group_name is not None:
            self.group_name = group_name
        if label is not None:
            self.label = label
