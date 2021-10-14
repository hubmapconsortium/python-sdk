import entity


class dataset(entity):
    def __init__(self, created_timestamp, created_by_user_displayname, created_by_user_email, created_by_user_sub, uuid,
                 hubmap_id, last_modified_user_timestamp, last_modified_user_sub, last_modified_user_email,
                 last_modified_user_displayname, entity_type, registered_doi, doi_url, creators, contacts, antibodies,
                 description, data_access_level, contains_human_genetic_sequences, status, title, data_types, upload,
                 collections, contributors, direct_ancestors, published_timestamp, published_user_displayname,
                 published_user_sub, published_user_email, ingest_metadata, local_directory_rel_path, group_uuid,
                 group_name, previous_revision_uuid, next_revision_uuid, thumbnail_file_to_add, thumbnail_file,
                 thumbnail_file_to_remove):
        super().__init__(created_timestamp, created_by_user_displayname, created_by_user_email, created_by_user_sub,
                         uuid, hubmap_id, last_modified_user_timestamp, last_modified_user_sub,
                         last_modified_user_email, last_modified_user_displayname, entity_type)
        self.registered_doi = registered_doi
        self.doi_url = doi_url
        self.creators = creators
        self.contacts = contacts
        self.antibodies = antibodies
        self.description = description
        self.data_access_level = data_access_level
        self.contains_human_genetic_sequences = contains_human_genetic_sequences
        self.status = status
        self.title = title
        self.data_types = data_types
        self.upload = upload
        self.collections = collections
        self.contributors = contributors
        self.direct_ancestors = direct_ancestors
        self.published_timestamp = published_timestamp
        self.published_user_displayname = published_user_displayname
        self.published_user_sub = published_user_sub
        self.published_user_email = published_user_email
        self.ingest_metadata = ingest_metadata
        self.local_directory_rel_path = local_directory_rel_path
        self.group_uuid = group_uuid
        self.group_name = group_name
        self.previous_revision_uuid = previous_revision_uuid
        self.next_revision_uuid = next_revision_uuid
        self.thumbnail_file = thumbnail_file
        self.thumbnail_file_to_add = thumbnail_file_to_add
        self.thumbnail_file_to_remove = thumbnail_file_to_remove
