import entity


class sample(entity):
    def __init__(self, created_timestamp, created_by_user_displayname, created_by_user_email, created_by_user_sub, uuid,
                 hubmap_id, last_modified_user_timestamp, last_modified_user_sub, last_modified_user_email,
                 last_modified_user_displayname, entity_type, registered_doi, doi_url, creators, contacts, description,
                 data_access_level, specimen_type, specimen_type_other, protocol_url, group_uuid, group_name, organ,
                 organ_other, direct_ancestor_uuid, submission_id, lab_tissue_sample_id, rui_location, metadata, visit,
                 image_files, image_files_to_remove, image_files_to_add, metadata_files, metadata_files_to_add,
                 metadata_files_to_remove):
        super().__init__(created_timestamp, created_by_user_displayname, created_by_user_email, created_by_user_sub,
                         uuid, hubmap_id, last_modified_user_timestamp, last_modified_user_sub,
                         last_modified_user_email, last_modified_user_displayname, entity_type)
        self.registered_doi = registered_doi
        self.doi_url = doi_url
        self.creators = creators
        self.contacts = contacts
        self.description = description
        self.data_access_level = data_access_level
        self.specimen_type = specimen_type
        self.specimen_type_other = specimen_type_other
        self.protocol_url = protocol_url
        self.group_uuid = group_uuid
        self.group_name = group_name
        self.organ = organ
        self.organ_other = organ_other
        self.direct_ancestor_uuid = direct_ancestor_uuid
        self.submission_id = submission_id
        self.lab_tissue_sample_id = lab_tissue_sample_id
        self.rui_location = rui_location
        self.metadata = metadata
        self.visit = visit
        self.image_files = image_files
        self.image_files_to_add = image_files_to_add
        self.image_files_to_remove = image_files_to_remove
        self.metadata_files = metadata_files
        self.metadata_files_to_add = metadata_files_to_add
        self.metadata_files_to_remove = metadata_files_to_remove
