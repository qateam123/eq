// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../../multiple-choice.page'

class WhyPaperEstablishmentPage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('why-paper-establishment')
  }

  clickWhyPaperEstablishmentAnswerMoreConvenient() {
    browser.element('[id="why-paper-establishment-answer-1"]').click()
    return this
  }

  clickWhyPaperEstablishmentAnswerDonTTrustInternetOrSecurityConcerns() {
    browser.element('[id="why-paper-establishment-answer-2"]').click()
    return this
  }

  clickWhyPaperEstablishmentAnswerOther() {
    browser.element('[id="why-paper-establishment-answer-3"]').click()
    return this
  }

  setWhyPaperEstablishmentAnswerOtherText(value) {
    browser.setValue('[id="why-paper-establishment-answer-3-other"]', value)
    return this
  }

}

export default new WhyPaperEstablishmentPage()
