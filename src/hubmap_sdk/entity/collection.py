import entity


class collection(entity):
    def __init__(self, created_timestamp, created_by_user_displayname, created_by_user_email, created_by_user_sub, uuid,
                 hubmap_id, last_modified_user_timestamp, last_modified_user_sub, last_modified_user_email, datasets,
                 last_modified_user_displayname, entity_type, registered_doi, doi_url, creators, contacts, title,):
        super().__init__(created_timestamp, created_by_user_displayname, created_by_user_email, created_by_user_sub,
                         uuid, hubmap_id, last_modified_user_timestamp, last_modified_user_sub,
                         last_modified_user_email, last_modified_user_displayname, entity_type)
        self.datasets = datasets
        self.registered_doi = registered_doi
        self.doi_url = doi_url
        self.creators = creators
        self.contacts = contacts
        self.title = title


