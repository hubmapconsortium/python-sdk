class Entity:

    def __init__(self, created_timestamp, created_by_user_displayname, created_by_user_email, created_by_user_sub, uuid,
                 hubmap_id, last_modified_user_timestamp, last_modified_user_sub, last_modified_user_email,
                 last_modified_user_displayname, entity_type):
        if created_timestamp is not None:
            self.created_timestamp = created_timestamp
        if created_by_user_displayname is not None:
            self.created_by_user_displayname = created_by_user_displayname
        if created_by_user_email is not None:
            self.created_by_user_email = created_by_user_email
        if created_by_user_sub is not None:
            self.created_by_user_sub = created_by_user_sub
        if uuid is not None:
            self.uuid = uuid
        if hubmap_id is not None:
            self.hubmap_id = hubmap_id
        if last_modified_user_timestamp is not None:
            self.last_modified_user_timestamp = last_modified_user_timestamp
        if last_modified_user_sub is not None:
            self.last_modified_user_sub = last_modified_user_sub
        if last_modified_user_displayname is not None:
            self.last_modified_user_displayname = last_modified_user_displayname
        if last_modified_user_email is not None:
            self.last_modified_user_email = last_modified_user_email
        if entity_type is not None:
            self.entity_type = entity_type
