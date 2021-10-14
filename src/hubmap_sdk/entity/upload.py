import entity


class upload(entity):
    def __init__(self, created_timestamp, created_by_user_displayname, created_by_user_email, created_by_user_sub, uuid,
                 hubmap_id, last_modified_user_timestamp, last_modified_user_sub, last_modified_user_email,
                 last_modified_user_displayname, entity_type, description, title, status, validation_message,
                 group_uuid, group_name, dataset_uuids_to_link, dataset_uuids_to_unlink, datasets):
        super().__init__(created_timestamp, created_by_user_displayname, created_by_user_email, created_by_user_sub,
                         uuid, hubmap_id, last_modified_user_timestamp, last_modified_user_sub,
                         last_modified_user_email, last_modified_user_displayname, entity_type)
        self.description = description
        self.title = title
        self.status = status
        self.validation_message = validation_message
        self.group_uuid = group_uuid
        self.group_name = group_name
        self.dataset = datasets
        self.dataset_uuids_to_link = dataset_uuids_to_link
        self.dataset_uuids_to_unlink = dataset_uuids_to_unlink
