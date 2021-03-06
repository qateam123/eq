from app.schema.answer import Answer
from app.schema.exceptions import QuestionnaireException
from app.validation.error_messages import error_messages


class Questionnaire(object):
    def __init__(self):
        self.id = None
        self.title = None
        self.survey_id = None
        self.description = None
        self.groups = []
        self.children = self.groups
        self.items_by_id = {}
        self.introduction = None
        self.aliases = {}
        self.theme = None
        self.data_version = None
        self.messages = {}

    def add_group(self, group):
        if group not in self.groups:
            self.groups.append(group)
            group.container = self

    def get_item_by_id(self, item_id):
        if item_id == self.id:
            return self
        elif item_id in self.items_by_id.keys():
            return self.items_by_id[item_id]
        else:
            raise QuestionnaireException('Unknown id \'{}\''.format(item_id))

    def item_exists(self, item_id):
        return item_id in self.items_by_id.keys()

    def register(self, item):
        if self.item_exists(item.id):
            raise QuestionnaireException('{} is a duplicate id'.format(item.id))

        self.items_by_id[item.id] = item

        # Build the two-way relationship
        item.questionnaire = self

    def register_aliases(self):
        for item in self.items_by_id.values():
            self._register_alias(item)

    def _register_alias(self, item):
        # Register the alias if the item has one
        if isinstance(item, Answer) and item.alias is not None:
            if item.alias not in self.aliases.keys():
                self.aliases[item.alias] = {
                    "answer_id": item.id,
                    "repeats": item.type == 'Checkbox' or item.container.type == 'RepeatingAnswer',
                }
            elif self.aliases[item.alias] != item.id:
                raise QuestionnaireException('{} is not a unique alias'.format(item.alias))

    def unregister(self, item_id):
        if item_id in self.items_by_id.keys():
            del self.items_by_id[item_id]

    def get_error_message(self, error, item_id):
        schema_item = self.get_item_by_id(item_id)

        # Try get the error message from the item
        if error in schema_item.messages.keys():
            return schema_item.messages[error]

        # Try get the error message from the questionnaire
        if error in self.messages.keys():
            return self.messages[error]

        # Error message has not been overwritten by the author, use the default
        return error_messages[error]
