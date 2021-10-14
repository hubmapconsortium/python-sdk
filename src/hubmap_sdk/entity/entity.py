class entity:

    def __init__(self, created_timestamp, created_by_user_displayname, created_by_user_email, created_by_user_sub, uuid,
                 hubmap_id, last_modified_user_timestamp, last_modified_user_sub, last_modified_user_email,
                 last_modified_user_displayname, entity_type):
        self.created_timestamp = created_timestamp
        self.created_by_user_displayname = created_by_user_displayname
        self.created_by_user_email = created_by_user_email
        self.created_by_user_sub = created_by_user_sub
        self.uuid = uuid
        self.hubmap_id = hubmap_id
        self.last_modified_user_timestamp = last_modified_user_timestamp
        self.last_modified_user_sub = last_modified_user_sub
        self.last_modified_user_displayname = last_modified_user_displayname
        self.last_modified_user_email = last_modified_user_email
        self.entity_type = entity_type
