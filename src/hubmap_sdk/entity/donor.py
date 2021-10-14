import entity


class donor(entity):
    def __init__(self, created_timestamp, created_by_user_displayname, created_by_user_email, created_by_user_sub, uuid,
                 hubmap_id, last_modified_user_timestamp, last_modified_user_sub, last_modified_user_email,
                 last_modified_user_displayname, entity_type, registered_doi, doi_url, creators, contacts, description,
                 data_access_level, image_files, image_files_to_add, image_files_to_remove, protocol_url, metadata,
                 submission_id, lab_donor_id, group_uuid, group_name, label):
        super().__init__(created_timestamp, created_by_user_displayname, created_by_user_email, created_by_user_sub,
                         uuid, hubmap_id, last_modified_user_timestamp, last_modified_user_sub,
                         last_modified_user_email, last_modified_user_displayname, entity_type)
        self.registered_doi = registered_doi
        self.doi_url = doi_url
        self.creators = creators
        self.contacts = contacts
        self.description = description
        self.data_access_level = data_access_level
        self.image_files = image_files
        self.image_files_to_remove = image_files_to_remove
        self.image_files_to_add = image_files_to_add
        self.protocol_url = protocol_url
        self.metadata = metadata
        self.submission_id = submission_id
        self.lab_donor_id = lab_donor_id
        self.group_uuid = group_uuid
        self.group_name = group_name
        self.label = label
