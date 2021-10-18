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
        if specimen_type is not None:
            self.specimen_type = specimen_type
        if specimen_type_other is not None:
            self.specimen_type_other = specimen_type_other
        if protocol_url is not None:
            self.protocol_url = protocol_url
        if group_uuid is not None:
            self.group_uuid = group_uuid
        if group_name is not None:
            self.group_name = group_name
        if organ is not None:
            self.organ = organ
        if organ_other is not None:
            self.organ_other = organ_other
        if direct_ancestor_uuid is not None:
            self.direct_ancestor_uuid = direct_ancestor_uuid
        if submission_id is not None:
            self.submission_id = submission_id
        if lab_tissue_sample_id is not None:
            self.lab_tissue_sample_id = lab_tissue_sample_id
        if rui_location is not None:
            self.rui_location = rui_location
        if metadata is not None:
            self.metadata = metadata
        if visit is not None:
            self.visit = visit
        if image_files is not None:
            self.image_files = image_files
        if image_files_to_add is not None:
            self.image_files_to_add = image_files_to_add
        if image_files_to_remove is not None:
            self.image_files_to_remove = image_files_to_remove
        if metadata_files is not None:
            self.metadata_files = metadata_files
        if metadata_files_to_add is not None:
            self.metadata_files_to_add = metadata_files_to_add
        if metadata_files_to_remove is not None:
            self.metadata_files_to_remove = metadata_files_to_remove
