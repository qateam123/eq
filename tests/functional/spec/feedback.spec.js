import chai from 'chai'
import {startQuestionnaire} from '../helpers'

import SummaryPage from '../pages/summary.page'

const expect = chai.expect

describe('Feedback', function() {

  it('Given a feedback button, a user should be able to click the feedback button to redirect them', function() {
    startQuestionnaire('test_textarea.json')
    browser.click('.qa-btn-submit')
    SummaryPage.submit()

    if(browser.isExisting('#feedbackButton'))
    {
      browser.click('.qa-btn-get-started')
      expect(browser.isExisting('#feedback')).to.be.true
    }
  })

  it('Given user has submitted the survey without selecting satisfacion, a user should get a error', function() {
    browser.click('.qa-btn-submit-answers')
    expect(browser.isExisting('.panel--error')).to.be.true
  })

  it('Given user has selected satisfacion, a user should be able to submit the survey successfully', function() {
    browser.element('#satisfied').click()
    browser.click('.qa-btn-submit-answers')
    expect(browser.isExisting('#successful')).to.be.true
  })


})

//error shows up if radios picked
//feedback is successfully submitted
//browser.element('#satisfied').click()
