from tests.integration.create_token import create_token
from tests.integration.integration_test_case import IntegrationTestCase
from tests.integration.mci import mci_test_urls


class TestNonMandatoryErrorToEmptyValue(IntegrationTestCase):

    def test_non_mandatory_error_to_empty_value(self):
        # Get a token
        token = create_token('0203', '1')
        resp = self.client.get('/session?token=' + token.decode(), follow_redirects=True)
        self.assertEqual(resp.status_code, 200)

        # We proceed to the questionnaire
        post_data = {
            'action[start_questionnaire]': 'Start Questionnaire'
        }
        resp = self.client.post(mci_test_urls.MCI_0203_INTRODUCTION, data=post_data, follow_redirects=False)
        self.assertEqual(resp.status_code, 302)

        block_one_url = resp.location

        resp = self.client.get(block_one_url, follow_redirects=False)
        self.assertEqual(resp.status_code, 200)

        # We fill in our answers, generating a error in a non-mandatory field
        form_data = {
            # Start Date
            "total-sales-food": "01",
            "period-from-month": "04",
            "period-from-year": "2016",
            # End Date
            "period-to-day": "01",
            "period-to-month": "04",
            "period-to-year": "2017",
            # Non Mandatory field but fails validation as should be Integer
            "total-retail-turnover": "failing test",
            # User Action
            "action[save_continue]": "Save &amp; Continue"
        }

        # We submit the form
        resp = self.client.post(block_one_url, data=form_data, follow_redirects=False)
        self.assertEqual(resp.status_code, 200)

        # Get the page content
        content = resp.get_data(True)
        self.assertRegex(content, "Please only enter whole numbers into the field")

        # We remove the non-mandatory field value
        form_data = {
            # Start Date
            "period-from-day": "01",
            "period-from-month": "4",
            "period-from-year": "2016",
            # End Date
            "period-to-day": "30",
            "period-to-month": "04",
            "period-to-year": "2016",
            # Total Turnover
            "total-retail-turnover": "100000",
            # User Action
            "action[save_continue]": "Save &amp; Continue"
        }

        # We submit the form

        resp = self.client.post(block_one_url, data=form_data, follow_redirects=False)
        self.assertEqual(resp.status_code, 302)

        # There are no validation errors
        self.assertRegex(resp.location, mci_test_urls.MCI_0203_SUMMARY_REGEX)
