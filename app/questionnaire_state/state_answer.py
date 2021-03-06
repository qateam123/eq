from werkzeug.datastructures import MultiDict

from app.data_model.answer_store import Answer
from app.questionnaire_state.state_item import StateItem


class StateAnswer(StateItem):
    def __init__(self, item_id, schema_item):
        super().__init__(item_id=item_id, schema_item=schema_item)
        # typed value
        self.value = None
        # actual user input
        self.input = None
        self.other = None

    def update_state(self, user_input):

        # Clear any previous value and validation results
        self.value = None
        self.is_valid = True
        self.errors = []
        # Get the user input
        # Todo, there shouldn't be a need for both self.input and self.value, but self.value gets changed later in the code
        self.input = self.schema_item.get_user_input(user_input)
        self.value = self.schema_item.get_user_input(user_input)
        self.other = self.schema_item.get_other_value(user_input)
        if self.schema_item.type == 'Radio' and self.input:
            self._restore_other_value(user_input)

    def _restore_other_value(self, user_input):
        # Get radio options from the schema.
        for option in self.schema_item.options:
            # If the radio answer has an Other option...
            if 'other' in option:

                other_option = option

                schema_options = [option['value'] for option in self.schema_item.options]

                if self.input not in schema_options:
                    # Input is not a pre-defined answer so it must be the user-entered value for other
                    self.input = option['value']
                    self.value = option['value']
                    self.other = self.schema_item.get_user_input(user_input)

                elif self.input == other_option['value'] and isinstance(user_input, MultiDict):
                    # User selected other but typed in a value which is already in schema
                    other_input_field = user_input.getlist(self.id)[-1:]
                    if other_input_field:
                        value = other_input_field[0]
                        if value in schema_options:
                            self.input = value
                            self.value = value
                            self.other = None

    def get_answers(self):
        return [self]

    def flatten(self):
        return Answer(
            block_id=self.parent.parent.parent.id,
            answer_id=self.id,
            answer_instance=self.answer_instance,
            group_id=self.schema_item.container.container.container.container.id,
            group_instance=self.group_instance,
            value=self.value,
        )
