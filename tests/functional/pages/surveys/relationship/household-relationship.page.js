import QuestionPage from '../question.page'

class HouseholdRelationshipPage extends QuestionPage {

  getRelationshipLabelAt(index) {
    var elementId = browser.elements('[data-qa="relationship-title"]').value[index]
    return browser.elementIdText(elementId.ELEMENT).value
  }

  setHusbandOrWifeRelationship(index, relationshipIndex) {
    var id = this.buildRelationshipAnswerId(index, 1)
    browser.waitForExist(id)
    browser.element(id).click().pause(300)
    return this
  }

  setSonOrDaughterRelationship(index, relationshipIndex) {
    var id = this.buildRelationshipAnswerId(index, 4)
    browser.waitForExist(id)
    browser.element(id).click().pause(300)
    return this
  }

  buildRelationshipAnswerId(index, relationshipId) {
    var id = '#who-is-related'
    if (index > 0) {
      id += '_' + index
    }
    id += '-' + relationshipId
    return id
  }

  toggleEditCloseButton(index) {
    let btnId = browser.elements('[data-qa="relationship-close-btn"]').value[index]
    browser.elementIdClick(btnId.ELEMENT)
    return this
  }

  submit() {
    browser.submitForm('.qa-questionnaire-form')
    return this
  }

}

export default new HouseholdRelationshipPage()
