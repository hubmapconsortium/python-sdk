import entity
class donor(entity):
    def __init__(self, created_timestamp, created_by_user_displayname, created_by_user_email, created_by_user_sub, uuid, hubmap_id, last_modified_user_timestamp, last_modified_user_sub, last_modified_user_email, last_modified_user_displayname, entity_type):
        super().__init__(created_timestamp, created_by_user_displayname, created_by_user_email, created_by_user_sub, uuid, hubmap_id, last_modified_user_timestamp, last_modified_user_sub, last_modified_user_email, last_modified_user_displayname, entity_type)
        self.