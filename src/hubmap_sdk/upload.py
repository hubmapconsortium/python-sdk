from hubmap_sdk import Entity


class Upload(Entity):
    def __init__(self, created_timestamp, created_by_user_displayname, created_by_user_email, created_by_user_sub, uuid,
                 hubmap_id, last_modified_user_timestamp, last_modified_user_sub, last_modified_user_email,
                 last_modified_user_displayname, entity_type, description, title, status, validation_message,
                 group_uuid, group_name, dataset_uuids_to_link, dataset_uuids_to_unlink, datasets):
        super().__init__(created_timestamp, created_by_user_displayname, created_by_user_email, created_by_user_sub,
                         uuid, hubmap_id, last_modified_user_timestamp, last_modified_user_sub,
                         last_modified_user_email, last_modified_user_displayname, entity_type)
        if description is not None:
            self.description = description
        if title is not None:
            self.title = title
        if status is not None:
            self.status = status
        if validation_message is not None:
            self.validation_message = validation_message
        if group_uuid is not None:
            self.group_uuid = group_uuid
        if group_name is not None:
            self.group_name = group_name
        if datasets is not None:
            self.dataset = datasets
        if dataset_uuids_to_link is not None:
            self.dataset_uuids_to_link = dataset_uuids_to_link
        if dataset_uuids_to_unlink is not None:
            self.dataset_uuids_to_unlink = dataset_uuids_to_unlink
