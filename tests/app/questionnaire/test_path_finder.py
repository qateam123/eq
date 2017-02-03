import unittest

import pytest

from app.data_model.answer_store import Answer, AnswerStore
from app.questionnaire.location import Location
from app.questionnaire.path_finder import PathFinder
from app.schema_loader.schema_loader import load_schema_file


class TestPathFinder(unittest.TestCase):  # pylint: disable=too-many-public-methods

    def test_next_block(self):
        survey = load_schema_file("1_0102.json")

        current_location = Location(
            block_id="total-retail-turnover",
            group_id="rsi",
            group_instance=0
        )

        next_location = Location(
            block_id="internet-sales",
            group_id="rsi",
            group_instance=0
        )

        path_finder = PathFinder(survey)
        self.assertEqual(path_finder.get_next_location(current_location=current_location), next_location)

    def test_previous_block(self):
        survey = load_schema_file("1_0102.json")

        current_location = Location(
            block_id="internet-sales",
            group_id="rsi",
            group_instance=0
        )

        previous_location = Location(
            block_id="total-retail-turnover",
            group_id="rsi",
            group_instance=0
        )

        path_finder = PathFinder(survey)
        self.assertEqual(path_finder.get_previous_location(current_location=current_location), previous_location)

    def test_introduction_in_path_when_in_schema(self):
        survey = load_schema_file("1_0102.json")

        path_finder = PathFinder(survey)

        blocks = [b.block_id for b in path_finder.get_location_path()]

        self.assertIn('introduction', blocks)

    def test_introduction_not_in_path_when_not_in_schema(self):
        survey = load_schema_file("census_individual.json")

        path_finder = PathFinder(survey)

        blocks = [b.block_id for b in path_finder.get_location_path()]

        self.assertNotIn('introduction', blocks)

    def test_next_with_conditional_path(self):
        survey = load_schema_file("0_star_wars.json")

        expected_path = [
            Location("14ba4707-321d-441d-8d21-b8367366e766", 0, "choose-your-side-block"),
            Location("14ba4707-321d-441d-8d21-b8367366e766", 0, "96682325-47ab-41e4-a56e-8315a19ffe2a"),
            Location("14ba4707-321d-441d-8d21-b8367366e766", 0, "cd3b74d1-b687-4051-9634-a8f9ce10a27d"),
            Location("14ba4707-321d-441d-8d21-b8367366e766", 0, "an3b74d1-b687-4051-9634-a8f9ce10ard"),
            Location("14ba4707-321d-441d-8d21-b8367366e766", 0, "846f8514-fed2-4bd7-8fb2-4b5fcb1622b1"),
        ]

        answer_1 = Answer(
            group_id="14ba4707-321d-441d-8d21-b8367366e766",
            block_id="choose-your-side-block",
            answer_id="ca3ce3a3-ae44-4e30-8f85-5b6a7a2fb23c",
            value="Light Side"
        )

        answer_2 = Answer(
            group_id="14ba4707-321d-441d-8d21-b8367366e766",
            block_id="96682325-47ab-41e4-a56e-8315a19ffe2a",
            answer_id="2e0989b8-5185-4ba6-b73f-c126e3a06ba7",
            value="No"
        )

        answers = AnswerStore()
        answers.add(answer_1)
        answers.add(answer_2)

        current_location = expected_path[1]
        expected_next_location = expected_path[2]

        path_finder = PathFinder(survey, answer_store=answers)
        actual_next_block = path_finder.get_next_location(current_location=current_location)

        self.assertEqual(actual_next_block, expected_next_location)

        current_location = expected_path[2]
        expected_next_location = expected_path[3]

        actual_next_block = path_finder.get_next_location(current_location=current_location)

        self.assertEqual(actual_next_block, expected_next_location)

    def test_routing_basic_path(self):
        survey = load_schema_file("1_0112.json")

        expected_path = [
            Location("rsi", 0, "reporting-period"),
            Location("rsi", 0, "total-retail-turnover"),
            Location("rsi", 0, "internet-sales"),
            Location("rsi", 0, "changes-in-retail-turnover"),
            Location("rsi", 0, "number-of-employees"),
            Location("rsi", 0, "changes-in-employees")
        ]

        path_finder = PathFinder(survey)
        routing_path = path_finder.get_routing_path()

        self.assertEqual(routing_path, expected_path)

    def test_routing_basic_and_conditional_path(self):
        survey = load_schema_file("0_star_wars.json")

        expected_path = [
            Location("14ba4707-321d-441d-8d21-b8367366e766", 0, "choose-your-side-block"),
            Location("14ba4707-321d-441d-8d21-b8367366e766", 0, "923ccc84-9d47-4a02-8ebc-1e9d14fcf10b"),
            Location("14ba4707-321d-441d-8d21-b8367366e766", 0, "26f2c4b3-28ac-4072-9f18-a6a6c6f660db"),
            Location("14ba4707-321d-441d-8d21-b8367366e766", 0, "cd3b74d1-b687-4051-9634-a8f9ce10a27d"),
            Location("14ba4707-321d-441d-8d21-b8367366e766", 0, "an3b74d1-b687-4051-9634-a8f9ce10ard"),
            Location("14ba4707-321d-441d-8d21-b8367366e766", 0, "846f8514-fed2-4bd7-8fb2-4b5fcb1622b1"),
        ]

        answer_1 = Answer(
            group_id="14ba4707-321d-441d-8d21-b8367366e766",
            block_id="choose-your-side-block",
            answer_id="ca3ce3a3-ae44-4e30-8f85-5b6a7a2fb23c",
            value="Dark Side"
        )
        answer_2 = Answer(
            group_id="14ba4707-321d-441d-8d21-b8367366e766",
            block_id="923ccc84-9d47-4a02-8ebc-1e9d14fcf10b",
            answer_id="pel989b8-5185-4ba6-b73f-c126e3a06ba7",
            value="Can I be a pain and have a goodies ship",
        )

        answers = AnswerStore()
        answers.add(answer_1)
        answers.add(answer_2)

        path_finder = PathFinder(survey, answer_store=answers)
        routing_path = path_finder.get_routing_path()

        self.assertEqual(routing_path, expected_path)

    def test_get_next_location_introduction(self):
        survey = load_schema_file("0_star_wars.json")

        path_finder = PathFinder(survey)

        introduction = Location('14ba4707-321d-441d-8d21-b8367366e766', 0, 'introduction')

        next_location = path_finder.get_next_location(current_location=introduction)

        self.assertEqual('choose-your-side-block', next_location.block_id)

    def test_get_next_location_summary(self):
        survey = load_schema_file("0_star_wars.json")

        answer_1 = Answer(
            group_id="14ba4707-321d-441d-8d21-b8367366e766",
            block_id="choose-your-side-block",
            answer_id="ca3ce3a3-ae44-4e30-8f85-5b6a7a2fb23c",
            value="Light Side"
        )
        answer_2 = Answer(
            group_id="14ba4707-321d-441d-8d21-b8367366e766",
            block_id="96682325-47ab-41e4-a56e-8315a19ffe2a",
            answer_id="2e0989b8-5185-4ba6-b73f-c126e3a06ba7",
            value="No",
        )

        answers = AnswerStore()
        answers.add(answer_1)
        answers.add(answer_2)

        path_finder = PathFinder(survey, answer_store=answers)

        current_location = Location('14ba4707-321d-441d-8d21-b8367366e766', 0, 'an3b74d1-b687-4051-9634-a8f9ce10ard')

        next_location = path_finder.get_next_location(current_location=current_location)

        expected_next_location = Location("14ba4707-321d-441d-8d21-b8367366e766", 0, '846f8514-fed2-4bd7-8fb2-4b5fcb1622b1')

        self.assertEqual(expected_next_location, next_location)

        current_location = expected_next_location

        next_location = path_finder.get_next_location(current_location=current_location)

        expected_next_location = Location("14ba4707-321d-441d-8d21-b8367366e766", 0, 'summary')

        self.assertEqual(expected_next_location, next_location)

    def test_get_previous_location_introduction(self):
        survey = load_schema_file("0_star_wars.json")

        path_finder = PathFinder(survey)

        first_location = Location("14ba4707-321d-441d-8d21-b8367366e766", 0, 'choose-your-side-block')

        previous_location = path_finder.get_previous_location(current_location=first_location)

        self.assertEqual('introduction', previous_location.block_id)

    def test_previous_with_conditional_path(self):
        survey = load_schema_file("0_star_wars.json")

        expected_path = [
            Location("14ba4707-321d-441d-8d21-b8367366e766", 0, "choose-your-side-block"),
            Location("14ba4707-321d-441d-8d21-b8367366e766", 0, "923ccc84-9d47-4a02-8ebc-1e9d14fcf10b"),
            Location("14ba4707-321d-441d-8d21-b8367366e766", 0, "26f2c4b3-28ac-4072-9f18-a6a6c6f660db"),
            Location("14ba4707-321d-441d-8d21-b8367366e766", 0, "cd3b74d1-b687-4051-9634-a8f9ce10a27d"),
            Location("14ba4707-321d-441d-8d21-b8367366e766", 0, "an3b74d1-b687-4051-9634-a8f9ce10ard"),
            Location("14ba4707-321d-441d-8d21-b8367366e766", 0, "846f8514-fed2-4bd7-8fb2-4b5fcb1622b1"),
        ]

        answer_1 = Answer(
            group_id="14ba4707-321d-441d-8d21-b8367366e766",
            block_id="choose-your-side-block",
            answer_id="ca3ce3a3-ae44-4e30-8f85-5b6a7a2fb23c",
            value="Dark Side"
        )
        answer_2 = Answer(
            group_id="14ba4707-321d-441d-8d21-b8367366e766",
            block_id="923ccc84-9d47-4a02-8ebc-1e9d14fcf10b",
            answer_id="pel989b8-5185-4ba6-b73f-c126e3a06ba7",
            value="Can I be a pain and have a goodies ship",
        )

        answers = AnswerStore()
        answers.add(answer_1)
        answers.add(answer_2)

        current_location = expected_path[3]
        expected_previous_location = expected_path[2]

        path_finder = PathFinder(survey, answer_store=answers)
        actual_previous_block = path_finder.get_previous_location(current_location=current_location)

        self.assertEqual(actual_previous_block, expected_previous_location)

        current_location = expected_path[2]
        expected_previous_location = expected_path[1]

        actual_previous_block = path_finder.get_previous_location(current_location=current_location)

        self.assertEqual(actual_previous_block, expected_previous_location)

    def test_previous_with_conditional_path_alternative(self):
        survey = load_schema_file("0_star_wars.json")

        expected_path = [
            Location("14ba4707-321d-441d-8d21-b8367366e766", 0, "choose-your-side-block"),
            Location("14ba4707-321d-441d-8d21-b8367366e766", 0, "96682325-47ab-41e4-a56e-8315a19ffe2a"),
            Location("14ba4707-321d-441d-8d21-b8367366e766", 0, "cd3b74d1-b687-4051-9634-a8f9ce10a27d"),
            Location("14ba4707-321d-441d-8d21-b8367366e766", 0, "an3b74d1-b687-4051-9634-a8f9ce10ard"),
            Location("14ba4707-321d-441d-8d21-b8367366e766", 0, "846f8514-fed2-4bd7-8fb2-4b5fcb1622b1"),
        ]

        current_location = expected_path[2]
        expected_previous_location = expected_path[1]

        answer_1 = Answer(
            group_id="14ba4707-321d-441d-8d21-b8367366e766",
            block_id="choose-your-side-block",
            answer_id="ca3ce3a3-ae44-4e30-8f85-5b6a7a2fb23c",
            value="Light Side"
        )
        answer_2 = Answer(
            group_id="14ba4707-321d-441d-8d21-b8367366e766",
            block_id="96682325-47ab-41e4-a56e-8315a19ffe2a",
            answer_id="2e0989b8-5185-4ba6-b73f-c126e3a06ba7",
            value="No",
        )

        answers = AnswerStore()
        answers.add(answer_1)
        answers.add(answer_2)

        path_finder = PathFinder(survey, answer_store=answers)

        self.assertEqual(path_finder.get_previous_location(current_location=current_location), expected_previous_location)

    def test_next_location_goto_summary(self):
        survey = load_schema_file("0_star_wars.json")

        expected_path = [
            Location("14ba4707-321d-441d-8d21-b8367366e766", 0, 'introduction'),
            Location("14ba4707-321d-441d-8d21-b8367366e766", 0, 'choose-your-side-block'),
            Location("14ba4707-321d-441d-8d21-b8367366e766", 0, 'summary'),
        ]

        answer = Answer(
            group_id="14ba4707-321d-441d-8d21-b8367366e766",
            group_instance=0,
            block_id="choose-your-side-block",
            answer_id="ca3ce3a3-ae44-4e30-8f85-5b6a7a2fb23c",
            value="I prefer Star Trek",
        )
        answers = AnswerStore()
        answers.add(answer)
        path_finder = PathFinder(survey, answer_store=answers)

        current_location = expected_path[1]
        expected_next_location = expected_path[2]

        next_location = path_finder.get_next_location(current_location=current_location)

        self.assertEqual(next_location, expected_next_location)

    def test_next_location_empty_routing_rules(self):
        survey = load_schema_file("test_checkbox.json")

        expected_path = [
            Location("14ba4707-321d-441d-8d21-b8367366e761", 0, 'introduction'),
            Location("14ba4707-321d-441d-8d21-b8367366e761", 0, 'block-1'),
            Location("14ba4707-321d-441d-8d21-b8367366e761", 0, 'f22b1ba4-d15f-48b8-a1f3-db62b6f34cc1'),
            Location("14ba4707-321d-441d-8d21-b8367366e761", 0, 'summary')
        ]

        answer_1 = Answer(
            group_id="14ba4707-321d-441d-8d21-b8367366e761",
            block_id="block-1",
            answer_id="ca3ce3a3-ae44-4e30-8f85-5b6a7a2fb23c",
            value="Cheese",
        )
        answer_2 = Answer(
            group_id="14ba4707-321d-441d-8d21-b8367366e761",
            block_id="f22b1ba4-d15f-48b8-a1f3-db62b6f34cc1",
            answer_id="ca3ce3a3-ae44-4e30-8f85-5b6a7a2fb23",
            value="deep pan",
        )

        answers = AnswerStore()
        answers.add(answer_1)
        answers.add(answer_2)

        path_finder = PathFinder(survey, answer_store=answers)

        current_location = expected_path[1]
        expected_next_location = expected_path[2]

        next_location = path_finder.get_next_location(current_location=current_location)

        self.assertEqual(next_location, expected_next_location)

    def test_interstitial_post_blocks(self):
        survey = load_schema_file("0_star_wars.json")

        answer = Answer(
            group_id="14ba4707-321d-441d-8d21-b8367366e766",
            block_id="choose-your-side-block",
            answer_id="ca3ce3a3-ae44-4e30-8f85-5b6a7a2fb23c",
            value="Light Side"
        )

        answers = AnswerStore()
        answers.add(answer)

        path_finder = PathFinder(survey, answer_store=answers)

        self.assertFalse(Location("14ba4707-321d-441d-8d21-b8367366e766", 0, 'summary') in path_finder.get_location_path())

    def test_repeating_groups(self):
        survey = load_schema_file("test_repeating_household.json")

        # Default is to count answers, so switch to using value
        survey['groups'][-1]['routing_rules'][0]['repeat']['type'] = 'answer_value'

        expected_path = [
            Location("multiple-questions-group", 0, "household-composition"),
            Location("repeating-group", 0, "repeating-block-1"),
            Location("repeating-group", 0, "repeating-block-2"),
            Location("repeating-group", 1, "repeating-block-1"),
            Location("repeating-group", 1, "repeating-block-2"),
        ]

        answer = Answer(
            group_id="multiple-questions-group",
            group_instance=0,
            answer_id="first-name",
            block_id="household-composition",
            value="2"
        )
        answers = AnswerStore()
        answers.add(answer)

        path_finder = PathFinder(survey, answer_store=answers)

        self.assertEqual(expected_path, path_finder.get_routing_path())

    def test_should_not_show_block_for_zero_repeats(self):
        survey = load_schema_file("test_repeating_household.json")

        # Default is to count answers, so switch to using value
        survey['groups'][-1]['routing_rules'][0]['repeat']['type'] = 'answer_value'

        expected_path = [
            Location("multiple-questions-group", 0, "household-composition")
        ]

        answer = Answer(
            group_id="multiple-questions-group",
            group_instance=0,
            answer_id="first-name",
            block_id="household-composition",
            value="0"
        )
        answers = AnswerStore()
        answers.add(answer)

        path_finder = PathFinder(survey, answer_store=answers)

        self.assertEqual(expected_path, path_finder.get_routing_path())

    def test_repeating_groups_no_of_answers(self):
        survey = load_schema_file("test_repeating_household.json")

        expected_path = [
            Location("multiple-questions-group", 0, "household-composition"),
            Location("repeating-group", 0, "repeating-block-1"),
            Location("repeating-group", 0, "repeating-block-2"),
            Location("repeating-group", 1, "repeating-block-1"),
            Location("repeating-group", 1, "repeating-block-2"),
            Location("repeating-group", 2, "repeating-block-1"),
            Location("repeating-group", 2, "repeating-block-2"),
        ]

        answer = Answer(
            group_id="multiple-questions-group",
            group_instance=0,
            answer_instance=0,
            answer_id="first-name",
            block_id="household-composition",
            value="Joe Bloggs"
        )

        answer_2 = Answer(
            group_id="multiple-questions-group",
            group_instance=0,
            answer_instance=1,
            answer_id="first-name",
            block_id="household-composition",
            value="Sophie Bloggs"
        )

        answer_3 = Answer(
            group_id="multiple-questions-group",
            group_instance=0,
            answer_instance=2,
            answer_id="first-name",
            block_id="household-composition",
            value="Gregg Bloggs"
        )

        answers = AnswerStore()

        answers.add(answer)
        answers.add(answer_2)
        answers.add(answer_3)

        path_finder = PathFinder(survey, answer_store=answers)

        self.assertEqual(expected_path, path_finder.get_routing_path())

    def test_repeating_groups_no_of_answers_minus_one(self):
        survey = load_schema_file("test_repeating_household.json")

        # Default is to count answers, so switch to using value
        survey['groups'][-1]['routing_rules'][0]['repeat']['type'] = 'answer_count_minus_one'

        expected_path = [
            Location("multiple-questions-group", 0, "household-composition"),
            Location("repeating-group", 0, "repeating-block-1"),
            Location("repeating-group", 0, "repeating-block-2"),
        ]

        answer = Answer(
            group_id="multiple-questions-group",
            group_instance=0,
            answer_instance=0,
            answer_id="first-name",
            block_id="household-composition",
            value="Joe Bloggs"
        )

        answer_2 = Answer(
            group_id="multiple-questions-group",
            group_instance=0,
            answer_instance=1,
            answer_id="first-name",
            block_id="household-composition",
            value="Sophie Bloggs"
        )

        answers = AnswerStore()

        answers.add(answer)
        answers.add(answer_2)

        path_finder = PathFinder(survey, answer_store=answers)

        self.assertEqual(expected_path, path_finder.get_routing_path())

    def test_repeating_groups_previous_location_introduction(self):
        survey = load_schema_file("test_repeating_household.json")

        expected_path = [
            Location('multiple-questions-group', 0, 'introduction'),
            Location('multiple-questions-group', 0, 'household-composition'),
        ]

        path_finder = PathFinder(survey)

        self.assertEqual(path_finder.get_previous_location(current_location=expected_path[1]), expected_path[0])

    def test_repeating_groups_previous_location(self):
        survey = load_schema_file("test_repeating_household.json")

        expected_path = [
            Location("multiple-questions-group", 0, "household-composition"),
            Location("repeating-group", 0, "repeating-block-1"),
            Location("repeating-group", 0, "repeating-block-2"),
            Location("repeating-group", 1, "repeating-block-1"),
            Location("repeating-group", 1, "repeating-block-2"),
        ]

        answer = Answer(
            group_id="multiple-questions-group",
            answer_instance=0,
            answer_id="first-name",
            block_id="household-composition",
            value="Joe Bloggs"
        )

        answer_2 = Answer(
            group_id="multiple-questions-group",
            answer_instance=1,
            answer_id="first-name",
            block_id="household-composition",
            value="Sophie Bloggs"
        )

        current_location = expected_path[4]

        expected_previous_location = expected_path[3]

        answers = AnswerStore()

        answers.add(answer)
        answers.add(answer_2)

        path_finder = PathFinder(survey, answer_store=answers)

        self.assertEqual(expected_previous_location, path_finder.get_previous_location(current_location=current_location))

    def test_repeating_groups_next_location(self):
        survey = load_schema_file("test_repeating_household.json")

        expected_path = [
            Location("multiple-questions-group", 0, "household-composition"),
            Location("repeating-group", 0, "repeating-block-1"),
            Location("repeating-group", 0, "repeating-block-2"),
            Location("repeating-group", 1, "repeating-block-1"),
            Location("repeating-group", 1, "repeating-block-2"),
        ]

        answer = Answer(
            group_id="multiple-questions-group",
            answer_instance=0,
            answer_id="first-name",
            block_id="household-composition",
            value="Joe Bloggs"
        )

        answer_2 = Answer(
            group_id="multiple-questions-group",
            answer_instance=1,
            answer_id="first-name",
            block_id="household-composition",
            value="Sophie Bloggs"
        )

        current_location = expected_path[-1]

        answers = AnswerStore()
        answers.add(answer)
        answers.add(answer_2)

        path_finder = PathFinder(survey, answer_store=answers)

        summary_location = Location("repeating-group", 0, 'summary')

        self.assertEqual(summary_location, path_finder.get_next_location(current_location=current_location))

    def test_repeating_groups_conditional_location_path(self):
        survey = load_schema_file("test_repeating_and_conditional_routing.json")

        expected_path = [
            Location("repeat-value-group", 0, "introduction"),
            Location("repeat-value-group", 0, "no-of-repeats"),
            Location("repeated-group", 0, "repeated-block"),
            Location("repeated-group", 0, "age-block"),
            Location("repeated-group", 0, "shoe-size-block"),
            Location("repeated-group", 1, "repeated-block"),
            Location("repeated-group", 1, "shoe-size-block"),
            Location("repeated-group", 0, "summary"),
            Location("repeated-group", 0, "thank-you"),
        ]

        answer_1 = Answer(
            group_id="repeat-value-group",
            block_id="no-of-repeats",
            answer_id="no-of-repeats-answer",
            value="2"
        )

        answer_2 = Answer(
            group_id="repeated-group",
            group_instance=0,
            block_id="repeated-block",
            answer_id="conditional-answer",
            value="Age and Shoe Size"
        )

        answer_3 = Answer(
            group_id="repeated-group",
            group_instance=1,
            block_id="repeated-block",
            answer_id="conditional-answer",
            value="Shoe Size Only"
        )

        answers = AnswerStore()
        answers.add(answer_1)
        answers.add(answer_2)
        answers.add(answer_3)

        path_finder = PathFinder(survey, answer_store=answers)

        self.assertEqual(expected_path, path_finder.get_location_path())

    def test_next_with_conditional_path_based_on_metadata(self):
        survey = load_schema_file("test_metadata_routing.json")

        expected_path = [
            Location("group1", 0, "block1"),
            Location("group1", 0, "block3"),
        ]

        current_location = expected_path[0]

        expected_next_location = expected_path[1]

        metadata = {
            "variant_flags": {
                "flag_1": True
            }
        }

        path_finder = PathFinder(survey, metadata=metadata)

        self.assertEqual(expected_next_location, path_finder.get_next_location(current_location=current_location))

    def test_next_with_conditional_path_when_value_not_in_metadata(self):
        survey = load_schema_file("test_metadata_routing.json")

        expected_path = [
            Location("group1", 0, "block1"),
            Location("group1", 0, "block2"),
        ]

        current_location = expected_path[0]

        expected_next_location = expected_path[1]

        metadata = {
            "variant_flags": {
            }
        }

        path_finder = PathFinder(survey, metadata=metadata)

        self.assertEqual(expected_next_location, path_finder.get_next_location(current_location=current_location))

    def test_routing_backwards_loops_to_previous_block(self):
        survey = load_schema_file("test_household_question.json")

        expected_path = [
            Location('multiple-questions-group', 0, 'introduction'),
            Location('multiple-questions-group', 0, 'household-composition'),
            Location('multiple-questions-group', 0, 'household-summary'),
            Location('multiple-questions-group', 0, 'household-composition'),
        ]

        current_location = expected_path[2]

        expected_next_location = expected_path[3]

        answers = AnswerStore()

        answer_1 = Answer(
            group_id="multiple-questions-group",
            group_instance=0,
            block_id="household-composition",
            answer_id="household-full-name",
            answer_instance=0,
            value="Joe Bloggs"
        )

        answer_2 = Answer(
            group_id="multiple-questions-group",
            group_instance=0,
            block_id="household-composition",
            answer_id="household-full-name",
            answer_instance=1,
            value="Sophie Bloggs"
        )

        answer_3 = Answer(
            group_id="multiple-questions-group",
            group_instance=0,
            block_id="household-summary",
            answer_id="household-composition-add-another",
            answer_instance=0,
            value="No"
        )

        answers.add(answer_1)
        answers.add(answer_2)
        answers.add(answer_3)

        path_finder = PathFinder(survey, answer_store=answers)

        self.assertEqual(expected_next_location, path_finder.get_next_location(current_location=current_location))

    def test_routing_backwards_continues_to_summary_when_complete(self):
        survey = load_schema_file("test_household_question.json")

        expected_path = [
            Location('multiple-questions-group', 0, 'introduction'),
            Location('multiple-questions-group', 0, 'household-composition'),
            Location('multiple-questions-group', 0, 'household-summary'),
            Location('multiple-questions-group', 0, 'summary'),
        ]

        current_location = expected_path[2]

        expected_next_location = expected_path[3]

        answers = AnswerStore()

        answer_1 = Answer(
            group_id="multiple-questions-group",
            group_instance=0,
            block_id="household-composition",
            answer_id="household-full-name",
            answer_instance=0,
            value="Joe Bloggs"
        )

        answer_2 = Answer(
            group_id="multiple-questions-group",
            group_instance=0,
            block_id="household-composition",
            answer_id="household-full-name",
            answer_instance=1,
            value="Sophie Bloggs"
        )

        answer_3 = Answer(
            group_id="multiple-questions-group",
            group_instance=0,
            block_id="household-summary",
            answer_id="household-composition-add-another",
            answer_instance=0,
            value="Yes"
        )

        answers.add(answer_1)
        answers.add(answer_2)
        answers.add(answer_3)

        path_finder = PathFinder(survey, answer_store=answers)

        self.assertEqual(expected_next_location, path_finder.get_next_location(current_location=current_location))

    def test_get_next_location_should_skip_group(self):
        # Given
        survey = load_schema_file('test_skip_condition_group.json')
        current_location = Location('do-you-want-to-skip-group', 0, 'do-you-want-to-skip')
        answer_store = AnswerStore()
        answer_store.add(Answer(group_id='do-you-want-to-skip-group', block_id='do-you-want-to-skip',
                                answer_id='do-you-want-to-skip-answer', value='Yes'))

        # When
        path_finder = PathFinder(survey, answer_store=answer_store)

        # Then
        expected_next_location = Location('last-group', 0, 'last-group-block')

        self.assertEqual(path_finder.get_next_location(current_location=current_location), expected_next_location)

    def test_get_next_location_should_not_skip_group(self):
        # Given
        survey = load_schema_file('test_skip_condition_group.json')
        current_location = Location('do-you-want-to-skip-group', 0, 'do-you-want-to-skip')
        answer_store = AnswerStore()
        answer_store.add(Answer(group_id='do-you-want-to-skip-group', block_id='do-you-want-to-skip',
                                answer_id='do-you-want-to-skip-answer', value='No'))

        # When
        path_finder = PathFinder(survey, answer_store=answer_store)

        # Then
        expected_location = Location('should-skip-group', 0, 'should-skip')

        self.assertEqual(path_finder.get_next_location(current_location=current_location), expected_location)

    def test_get_next_location_should_not_skip_when_no_answers(self):
        # Given
        survey = load_schema_file('test_skip_condition_group.json')
        current_location = Location('do-you-want-to-skip-group', 0, 'do-you-want-to-skip')
        answer_store = AnswerStore()

        # When
        path_finder = PathFinder(survey, answer_store=answer_store)

        # Then
        expected_location = Location('should-skip-group', 0, 'should-skip')

        self.assertEqual(path_finder.get_next_location(current_location=current_location), expected_location)

    @pytest.mark.xfail(reason="Known bug when skipping last group due to summary bundled into it", strict=True, raises=StopIteration)
    def test_get_routing_path_when_first_block_in_group_skipped(self):
        # Given
        survey = load_schema_file('test_skip_condition_group.json')
        answer_store = AnswerStore()
        answer_store.add(Answer(group_id='do-you-want-to-skip-group', block_id='do-you-want-to-skip',
                                answer_id='do-you-want-to-skip-answer', value='Yes'))

        # When
        path_finder = PathFinder(survey, answer_store=answer_store)

        # Then
        expected_route = [
            {
                'block_id': 'do-you-want-to-skip-block',
                'group_id': 'do-you-want-to-skip-group',
                'group_instance': 0
            },
            {
                'block_id': 'summary',
                'group_id': 'should-skip-group',
                'group_instance': 0
            }
        ]
        self.assertEqual(path_finder.get_routing_path('should-skip-group'), expected_route)

    def test_build_path_with_invalid_location(self):
        path_finder = PathFinder(survey_json={})

        blocks = [
            {
                "group_id": 'first-valid-group-id',
                "group_instance": 0,
                "block": {"id": 'first-valid-block-id'}
            }, {
                "group_id": 'second-valid-group-id',
                "group_instance": 0,
                "block": {"id": 'second-valid-block-id'}
            }
        ]

        invalid_group_location = Location(
            group_instance=0,
            group_id='this-group-id-doesnt-exist-in-the-list-of-blocks',
            block_id='first-valid-block-id'
        )

        with self.assertRaises(StopIteration):
            path_finder.build_path(blocks, invalid_group_location)

        invalid_block_location = Location(
            group_instance=0,
            group_id='second-valid-group-id',
            block_id='this-block-id-doesnt-exist-in-the-list-of-blocks'
        )

        with self.assertRaises(StopIteration):
            path_finder.build_path(blocks, invalid_block_location)
