import unittest

from app import create_app
from app.data_model.answer_store import AnswerStore, Answer
from app.questionnaire.location import Location
from app.questionnaire.navigation import Navigation
from app.schema_loader.schema_loader import load_schema_file


class TestNavigation(unittest.TestCase):

    @staticmethod
    def setUp():
        app = create_app()
        app.config['SERVER_NAME'] = "test"
        app_context = app.app_context()
        app_context.push()

    def test_navigation_no_blocks_completed(self):
        survey = load_schema_file("test_navigation.json")
        metadata = {
            "eq_id": '1',
            "collection_exercise_sid": '999',
            "form_type": "some_form"
        }

        navigation = Navigation(survey, AnswerStore(), metadata)

        user_navigation = [
            {
                'link_name': 'Property Details',
                'highlight': True,
                'repeating': False,
                'completed': False,
                'link_url': Location('property-details', 0, 'insurance-type').url(metadata)
            },
            {
                'link_name': 'Household Details',
                'highlight': False,
                'repeating': False,
                'completed': False,
                'link_url': Location('multiple-questions-group', 0, 'household-composition').url(metadata)
            },
            {
                'link_name': 'Extra Cover',
                'highlight': False,
                'repeating': False,
                'completed': False,
                'link_url': Location('extra-cover', 0, 'extra-cover-block').url(metadata)
            },
            {
                'link_name': 'Payment Details',
                'highlight': False,
                'repeating': False,
                'completed': False,
                'link_url': Location('payment-details', 0, 'credit-card').url(metadata)
            }
        ]

        self.assertEqual(navigation.build_navigation('property-details', 0), user_navigation)

    def test_non_repeating_block_completed(self):
        survey = load_schema_file("test_navigation.json")
        metadata = {
            "eq_id": '1',
            "collection_exercise_sid": '999',
            "form_type": "some_form"
        }
        completed_blocks = [
            Location('property-details', 0, 'introduction'),
            Location('property-details', 0, 'insurance-type'),
            Location('property-details', 0, 'insurance-address'),
            Location('property-details', 0, 'property-interstitial')
        ]

        navigation = Navigation(survey, AnswerStore(), metadata, completed_blocks=completed_blocks)

        user_navigation = [
            {
                'completed': True,
                'link_name': 'Property Details',
                'highlight': True,
                'repeating': False,
                'link_url': Location('property-details', 0, 'insurance-type').url(metadata),
            },
            {
                'completed': False,
                'link_name': 'Household Details',
                'highlight': False,
                'repeating': False,
                'link_url': Location('multiple-questions-group', 0, 'household-composition').url(metadata),
            },
            {
                'completed': False,
                'link_name': 'Extra Cover',
                'highlight': False,
                'repeating': False,
                'link_url': Location('extra-cover', 0, 'extra-cover-block').url(metadata)
            },
            {
                'completed': False,
                'link_name': 'Payment Details',
                'highlight': False,
                'repeating': False,
                'link_url': Location('payment-details', 0, 'credit-card').url(metadata)
            }
        ]
        self.assertEqual(navigation.build_navigation('property-details', 0), user_navigation)

    def test_navigation_repeating_household_and_hidden_household_groups_completed(self):

        survey = load_schema_file("test_navigation.json")
        metadata = {
            "eq_id": '1',
            "collection_exercise_sid": '999',
            "form_type": "some_form"
        }

        completed_blocks = [
            Location('property-details', 0, 'introduction'),
            Location('multiple-questions-group', 0, 'household-composition'),
            Location('repeating-group', 0, 'repeating-block-1'),
            Location('repeating-group', 0, 'repeating-block-2'),
            Location('repeating-group', 1, 'repeating-block-1'),
            Location('repeating-group', 1, 'repeating-block-2')
        ]

        navigation = Navigation(survey, AnswerStore(), metadata, completed_blocks=completed_blocks)

        navigation.answer_store.answers = [
            {
                'group_instance': 0,
                'answer_instance': 0,
                'answer_id': 'household-full-name',
                'value': 'Jim',
                'group_id': 'multiple-questions-group',
                'block_id': 'household-composition'
            },
            {
                'group_instance': 0,
                'answer_instance': 1,
                'answer_id': 'household-full-name',
                'value': 'Ben',
                'group_id': 'multiple-questions-group',
                'block_id': 'household-composition'
            },
            {
                'group_instance': 0,
                'answer_instance': 0,
                'answer_id': 'what-is-your-age',
                'value': None,
                'group_id': 'repeating-group',
                'block_id': 'repeating-block-1'
            },
            {
                'group_instance': 0,
                'answer_instance': 0,
                'answer_id': 'what-is-your-shoe-size',
                'value': None,
                'group_id': 'repeating-group',
                'block_id': 'repeating-block-2'
            },
            {
                'group_instance': 1,
                'answer_instance': 0,
                'answer_id': 'what-is-your-age',
                'value': None,
                'group_id': 'repeating-group',
                'block_id': 'repeating-block-1'
            },
            {
                'group_instance': 1,
                'answer_instance': 0,
                'answer_id': 'what-is-your-shoe-size',
                'value': None,
                'group_id': 'repeating-group',
                'block_id': 'repeating-block-2'
            }
        ]

        user_navigation = [
            {
                'link_name': 'Property Details',
                'repeating': False,
                'completed': False,
                'highlight': True,
                'link_url': Location('property-details', 0, 'insurance-type').url(metadata)
            },
            {
                'link_name': 'Household Details',
                'repeating': False,
                'completed': True,
                'highlight': False,
                'link_url': Location('multiple-questions-group', 0, 'household-composition').url(metadata)
            },
            {
                'link_name': 'Jim',
                'repeating': True,
                'completed': True,
                'highlight': False,
                'link_url': Location('repeating-group', 0, 'repeating-block-1').url(metadata)
            },
            {
                'link_name': 'Ben',
                'repeating': True,
                'completed': True,
                'highlight': False,
                'link_url': Location('repeating-group', 1, 'repeating-block-1').url(metadata)
            },
            {
                'link_name': 'Extra Cover',
                'repeating': False,
                'completed': False,
                'highlight': False,
                'link_url': Location('extra-cover', 0, 'extra-cover-block').url(metadata)
            },
            {
                'link_name': 'Payment Details',
                'repeating': False,
                'completed': False,
                'highlight': False,
                'link_url': Location('payment-details', 0, 'credit-card').url(metadata)
            }
        ]

        self.assertEqual(navigation.build_navigation('property-details', 0), user_navigation)

    def test_navigation_repeating_group_extra_answered_not_completed(self):
        survey = load_schema_file("test_navigation.json")
        metadata = {
            "eq_id": '1',
            "collection_exercise_sid": '999',
            "form_type": "some_form"
        }

        completed_blocks = [
            Location('property-details', 0, 'introduction'),
            Location('property-details', 0, 'insurance-type'),
            Location('property-details', 0, 'cd6a5727-8cab-4737-aa4e-d666d98b3f92'),
            Location('property-details', 0, 'personal-interstitial'),
            Location('extra-cover', 0, 'extra-cover-block'),
            Location('extra-cover', 0, 'ea651fa7-6b9d-4b6f-ba72-79133f312039'),
        ]

        answer_store = AnswerStore()

        answer_1 = Answer(
            answer_instance=0,
            group_id='multiple-questions-group',
            answer_id='household-full-name',
            block_id='household-composition',
            group_instance=0,
            value='Person1'
        )
        answer_2 = Answer(
            answer_instance=1,
            group_id='multiple-questions-group',
            answer_id='household-full-name',
            block_id='household-composition',
            group_instance=0,
            value='Person2'
        )
        answer_3 = Answer(
            answer_instance=1,
            group_id='extra-cover',
            answer_id='extra-cover-answer',
            block_id='extra-cover-block',
            group_instance=0,
            value=2
        )

        answer_store.add(answer_1)
        answer_store.add(answer_2)
        answer_store.add(answer_3)

        navigation = Navigation(survey, answer_store, metadata, completed_blocks)

        user_navigation = [
            {
                'completed': False,
                'highlight': True,
                'repeating': False,
                'link_name': 'Property Details',
                'link_url': Location('property-details', 0, 'insurance-type').url(metadata)
            },
            {
                'completed': False,
                'highlight': False,
                'repeating': False,
                'link_name': 'Household Details',
                'link_url': Location('multiple-questions-group', 0, 'household-composition').url(metadata),
            },
            {
                'completed': False,
                'highlight': False,
                'repeating': True,
                'link_name': 'Person1',
                'link_url': Location('repeating-group', 0, 'repeating-block-1').url(metadata),
            },
            {
                'completed': False,
                'highlight': False,
                'repeating': True,
                'link_name': 'Person2',
                'link_url': Location('repeating-group', 1, 'repeating-block-1').url(metadata),
            },
            {
                'completed': False,
                'highlight': False,
                'repeating': False,
                'link_name': 'Extra Cover',
                'link_url': Location('extra-cover', 0, 'extra-cover-block').url(metadata),
            },
            {
                'completed': False,
                'highlight': False,
                'repeating': False,
                'link_name': 'Payment Details',
                'link_url': Location('payment-details', 0, 'credit-card').url(metadata),
            },
            {
                'completed': False,
                'highlight': False,
                'repeating': False,
                'link_name': 'Extra Cover Items',
                'link_url': Location('extra-cover-items-group', 0, 'extra-cover-items').url(metadata)
            }
        ]

        self.assertEqual(navigation.build_navigation('property-details', 0), user_navigation)

    def test_navigation_repeating_group_extra_answered_completed(self):
        survey = load_schema_file("test_navigation.json")
        metadata = {
            "eq_id": '1',
            "collection_exercise_sid": '999',
            "form_type": "some_form"
        }

        completed_blocks = [
            Location('property-details', 0, 'introduction'),
            Location('extra-cover', 0, 'extra-cover-block'),
            Location('extra-cover', 0, 'extra-cover-interstitial'),
            Location('extra-cover-items-group', 0, 'extra-cover-items'),
            Location('extra-cover-items-group', 1, 'extra-cover-items'),
        ]

        answer_store = AnswerStore()

        answer_1 = Answer(
            value=2,
            group_instance=0,
            block_id='extra-cover-block',
            group_id='extra-cover',
            answer_instance=0,
            answer_id='extra-cover-answer'
        )
        answer_2 = Answer(
            value='2',
            group_instance=0,
            block_id='extra-cover-items',
            group_id='extra-cover-items-group',
            answer_instance=0,
            answer_id='extra-cover-items-answer'
        )
        answer_3 = Answer(
            value='2',
            group_instance=1,
            block_id='extra-cover-items',
            group_id='extra-cover-items-group',
            answer_id='extra-cover-items-answer',
            answer_instance=0
        )

        answer_store.add(answer_1)
        answer_store.add(answer_2)
        answer_store.add(answer_3)

        navigation = Navigation(survey, answer_store, metadata, completed_blocks=completed_blocks)

        user_navigation = [
            {
                'repeating': False,
                'highlight': True,
                'completed': False,
                'link_name': 'Property Details',
                'link_url': Location('property-details', 0, 'insurance-type').url(metadata)
            },
            {
                'repeating': False,
                'highlight': False,
                'completed': False,
                'link_name': 'Household Details',
                'link_url': Location('multiple-questions-group', 0, 'household-composition').url(metadata)
            },
            {
                'repeating': False,
                'highlight': False,
                'completed': True,
                'link_name': 'Extra Cover',
                'link_url': Location('extra-cover', 0, 'extra-cover-block').url(metadata)
            },
            {
                'repeating': False,
                'highlight': False,
                'completed': False,
                'link_name': 'Payment Details',
                'link_url': Location('payment-details', 0, 'credit-card').url(metadata)
            },
            {
                'repeating': False,
                'highlight': False,
                'completed': True,
                'link_name': 'Extra Cover Items',
                'link_url': Location('extra-cover-items-group', 0, 'extra-cover-items').url(metadata)
            }
        ]
        self.assertEqual(navigation.build_navigation('property-details', 0), user_navigation)

    def test_navigation_repeating_group_link_name_format(self):
        survey = load_schema_file("test_repeating_household.json")
        metadata = {
            "eq_id": '1',
            "collection_exercise_sid": '999',
            "form_type": "some_form"
        }

        completed_blocks = [
            Location('multiple-questions-group', 0, 'introduction'),
            Location('multiple-questions-group', 0, 'household-composition'),
        ]

        answer_store = AnswerStore()

        answer_1 = Answer(
            block_id='household-composition',
            answer_instance=0,
            answer_id='first-name',
            group_id='multiple-questions-group',
            group_instance=0,
            value='Joe'
        )
        answer_2 = Answer(
            block_id='household-composition',
            answer_instance=0,
            answer_id='middle-names',
            group_id='multiple-questions-group',
            group_instance=0,
            value=None
        )
        answer_3 = Answer(
            block_id='household-composition',
            answer_instance=0,
            answer_id='last-name',
            group_id='multiple-questions-group',
            group_instance=0,
            value='Bloggs'
        )
        answer_4 = Answer(
            block_id='household-composition',
            answer_instance=1,
            answer_id='first-name',
            group_id='multiple-questions-group',
            group_instance=0,
            value='Jim'
        )
        answer_5 = Answer(
            block_id='household-composition',
            answer_instance=1,
            answer_id='last-name',
            group_id='multiple-questions-group',
            group_instance=0,
            value=None
        )
        answer_6 = Answer(
            block_id='household-composition',
            answer_instance=1,
            answer_id='middle-names',
            group_id='multiple-questions-group',
            group_instance=0,
            value=None
        )

        answer_store.add(answer_1)
        answer_store.add(answer_2)
        answer_store.add(answer_3)
        answer_store.add(answer_4)
        answer_store.add(answer_5)
        answer_store.add(answer_6)

        navigation = Navigation(survey, answer_store, metadata, completed_blocks=completed_blocks)

        user_navigation = [
            {
                'repeating': False,
                'completed': True,
                'highlight': False,
                'link_name': '',
                'link_url': Location('multiple-questions-group', 0, 'household-composition').url(metadata)
            },
            {
                'repeating': True,
                'link_name': 'Joe Bloggs',
                'completed': False,
                'highlight': False,
                'link_url': Location('repeating-group', 0, 'repeating-block-1').url(metadata)
            },
            {
                'repeating': True,
                'link_name': 'Jim',
                'completed': False,
                'highlight': False,
                'link_url': Location('repeating-group', 1, 'repeating-block-1').url(metadata)
            }
        ]

        self.assertEqual(navigation.build_navigation('property-details', 0), user_navigation)

    def test_navigation_skip_condition_hide_group(self):
        survey = load_schema_file("test_navigation.json")

        metadata = {
            "eq_id": '1',
            "collection_exercise_sid": '999',
            "form_type": "some_form"
        }

        completed_blocks = []

        answer_store = AnswerStore()

        answer_1 = Answer(
            value="Contents",
            group_instance=0,
            block_id='insurance-type',
            group_id='property-details',
            answer_instance=0,
            answer_id='insurance-type-answer'
        )

        answer_store.add(answer_1)

        navigation = Navigation(survey, answer_store, metadata, completed_blocks=completed_blocks)
        user_navigation = navigation.build_navigation('property-details', 0)
        link_names = [d['link_name'] for d in user_navigation]
        self.assertNotIn('House Details', link_names)

    def test_navigation_skip_condition_show_group(self):
        survey = load_schema_file("test_navigation.json")

        metadata = {
            "eq_id": '1',
            "collection_exercise_sid": '999',
            "form_type": "some_form"
        }

        completed_blocks = []

        answer_store = AnswerStore()

        answer_1 = Answer(
            value="Buildings",
            group_instance=0,
            block_id='insurance-type',
            group_id='property-details',
            answer_instance=0,
            answer_id='insurance-type-answer'
        )

        answer_store.add(answer_1)

        navigation = Navigation(survey, answer_store, metadata, completed_blocks=completed_blocks)

        user_navigation = navigation.build_navigation('property-details', 0)
        link_names = [d['link_name'] for d in user_navigation]
        self.assertIn('House Details', link_names)

    def test_navigation_skip_condition_change_answer(self):
        survey = load_schema_file("test_navigation.json")

        metadata = {
            "eq_id": '1',
            "collection_exercise_sid": '999',
            "form_type": "some_form"
        }

        completed_blocks = []

        answer_store = AnswerStore()

        answer_1 = Answer(
            value="Buildings",
            group_instance=0,
            block_id='insurance-type',
            group_id='property-details',
            answer_instance=0,
            answer_id='insurance-type-answer'
        )

        answer_store.add(answer_1)
        navigation = Navigation(survey, answer_store, metadata, completed_blocks=completed_blocks)

        user_navigation = navigation.build_navigation('property-details', 0)
        link_names = [d['link_name'] for d in user_navigation]
        self.assertIn('House Details', link_names)

        change_answer = Answer(
            value="Contents",
            group_instance=0,
            block_id='insurance-type',
            group_id='property-details',
            answer_instance=0,
            answer_id='insurance-type-answer'
        )

        answer_store.update(change_answer)

        user_navigation = navigation.build_navigation('property-details', 0)
        link_names = [d['link_name'] for d in user_navigation]
        self.assertNotIn('House Details', link_names)
