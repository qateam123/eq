import chai from 'chai'
import {startCensusQuestionnaire} from '../../../helpers'

import PermanentOrFamilyHome from '../../../pages/surveys/census/household/permanent-or-family-home.page.js'
import HouseholdComposition from '../../../pages/surveys/census/household/household-composition.page.js'
import EveryoneAtAddressConfirmation from '../../../pages/surveys/census/household/everyone-at-address-confirmation.page.js'
import OvernightVisitors from '../../../pages/surveys/census/household/overnight-visitors.page.js'
import HouseholdRelationships from '../../../pages/surveys/census/household/household-relationships.page.js'
import WhoLivesHereCompleted from '../../../pages/surveys/census/household/who-lives-here-completed.page.js'
import TypeOfAccommodation from '../../../pages/surveys/census/household/type-of-accommodation.page.js'
import TypeOfHouse from '../../../pages/surveys/census/household/type-of-house.page.js'
import SelfContainedAccommodation from '../../../pages/surveys/census/household/self-contained-accommodation.page.js'
import NumberOfBedrooms from '../../../pages/surveys/census/household/number-of-bedrooms.page.js'
import CentralHeating from '../../../pages/surveys/census/household/central-heating.page.js'
import OwnOrRent from '../../../pages/surveys/census/household/own-or-rent.page.js'
import NumberOfVehicles from '../../../pages/surveys/census/household/number-of-vehicles.page.js'
import HouseholdAndAccommodationCompleted from '../../../pages/surveys/census/household/household-and-accommodation-completed.page.js'
import HouseholdMemberBegin from '../../../pages/surveys/census/household/household-member-begin.page.js'
import DetailsCorrect from '../../../pages/surveys/census/household/details-correct.page.js'
import Sex from '../../../pages/surveys/census/household/sex.page.js'
import DateOfBirth from '../../../pages/surveys/census/household/date-of-birth.page.js'
import Over16 from '../../../pages/surveys/census/household/over-16.page.js'
import PrivateResponse from '../../../pages/surveys/census/household/private-response.page.js'
import MaritalStatus from '../../../pages/surveys/census/household/marital-status.page.js'
import AnotherAddress from '../../../pages/surveys/census/household/another-address.page.js'
import InEducation from '../../../pages/surveys/census/household/in-education.page.js'
import CountryOfBirth from '../../../pages/surveys/census/household/country-of-birth.page.js'
import Carer from '../../../pages/surveys/census/household/carer.page.js'
import NationalIdentity from '../../../pages/surveys/census/household/national-identity.page.js'
import EthnicGroup from '../../../pages/surveys/census/household/ethnic-group.page.js'
import WhiteEthnicGroup from '../../../pages/surveys/census/household/white-ethnic-group.page.js'
import Language from '../../../pages/surveys/census/household/language.page.js'
import Religion from '../../../pages/surveys/census/household/religion.page.js'
import PastUsualAddress from '../../../pages/surveys/census/household/past-usual-address.page.js'
import Passports from '../../../pages/surveys/census/household/passports.page.js'
import Disability from '../../../pages/surveys/census/household/disability.page.js'
import Qualifications from '../../../pages/surveys/census/household/qualifications.page.js'
import Volunteering from '../../../pages/surveys/census/household/volunteering.page.js'
import EmploymentType from '../../../pages/surveys/census/household/employment-type.page.js'
import Jobseeker from '../../../pages/surveys/census/household/jobseeker.page.js'
import MainJob from '../../../pages/surveys/census/household/main-job.page'

const expect = chai.expect

describe('Routing on Multiple Checkbox', function () {

  it('Given I am answering question 28. Last week were you.., When I dont select any response, Then I am routed to 29. Were you actively looking for...?', function () {
    startCensusQuestionnaire('census_household.json')

    // who-lives-here
    PermanentOrFamilyHome.clickPermanentOrFamilyHomeAnswerYes().submit()
    HouseholdComposition.setFirstName('John').addPerson().setFirstName('Jane', 1).submit()
    EveryoneAtAddressConfirmation.clickEveryoneAtAddressConfirmationAnswerYes().submit()
    OvernightVisitors.setOvernightVisitorsAnswer(0).submit()
    HouseholdRelationships.clickHouseholdRelationshipsAnswerHusbandOrWife().submit()
    WhoLivesHereCompleted.submit()

    // household-and-accommodation
    TypeOfAccommodation.clickTypeOfAccommodationAnswerWholeHouseOrBungalow().submit()
    TypeOfHouse.clickTypeOfHouseAnswerSemiDetached().submit()
    SelfContainedAccommodation.clickSelfContainedAccommodationAnswerYesAllTheRoomsAreBehindADoorThatOnlyThisHouseholdCanUse().submit()
    NumberOfBedrooms.setNumberOfBedroomsAnswer(3).submit()
    CentralHeating.clickCentralHeatingAnswerGas().submit()
    OwnOrRent.clickOwnOrRentAnswerOwnsOutright().submit()
    NumberOfVehicles.setNumberOfVehiclesAnswer(2).submit()
    HouseholdAndAccommodationCompleted.submit()

    // household-member
    HouseholdMemberBegin.submit()
    DetailsCorrect.clickDetailsCorrectAnswerYesThisIsMyFullName().submit()
    Over16.clickOver16AnswerYes().submit()
    PrivateResponse.clickPrivateResponseAnswerNoIDoNotWantToRequestAPersonalForm().submit()
    Sex.clickSexAnswerMale().submit()
    DateOfBirth.setDateOfBirthAnswerDay(2).setDateOfBirthAnswerMonth(3).setDateOfBirthAnswerYear(1980).submit()
    MaritalStatus.clickMaritalStatusAnswerMarried().submit()
    AnotherAddress.clickAnotherAddressAnswerNo().submit()
    InEducation.clickInEducationAnswerNo().submit()
    CountryOfBirth.clickCountryOfBirthEnglandAnswerEngland().submit()
    Carer.clickCarerAnswerNo().submit()
    NationalIdentity.clickNationalIdentityEnglandAnswerEnglish().submit()
    EthnicGroup.clickEthnicGroupEnglandAnswerWhite().submit()
    WhiteEthnicGroup.clickWhiteEthnicGroupEnglandAnswerEnglishWelshScottishNorthernIrishBritish().submit()
    Language.clickLanguageEnglandAnswerEnglish().submit()
    Religion.clickReligionAnswerNoReligion().submit()
    PastUsualAddress.clickPastUsualAddressAnswerThisAddress().submit()
    Passports.clickPassportsAnswerUnitedKingdom().submit()
    Disability.clickDisabilityAnswerNo().submit()
    Qualifications.clickQualificationsEnglandAnswerUndergraduateDegree().submit()
    Volunteering.clickVolunteeringAnswerNo().submit()
    EmploymentType.submit()
    expect(Jobseeker.isOpen()).to.be.true
  })

  it('Given I am answering question 28. Last week were you.., When I select none of the above, Then I am routed to 29. Were you actively looking for...?', function () {
    startCensusQuestionnaire('census_household.json')

    // who-lives-here
    PermanentOrFamilyHome.clickPermanentOrFamilyHomeAnswerYes().submit()
    HouseholdComposition.setFirstName('John').addPerson().setFirstName('Jane', 1).submit()
    EveryoneAtAddressConfirmation.clickEveryoneAtAddressConfirmationAnswerYes().submit()
    OvernightVisitors.setOvernightVisitorsAnswer(0).submit()
    HouseholdRelationships.clickHouseholdRelationshipsAnswerHusbandOrWife().submit()
    WhoLivesHereCompleted.submit()

    // household-and-accommodation
    TypeOfAccommodation.clickTypeOfAccommodationAnswerWholeHouseOrBungalow().submit()
    TypeOfHouse.clickTypeOfHouseAnswerSemiDetached().submit()
    SelfContainedAccommodation.clickSelfContainedAccommodationAnswerYesAllTheRoomsAreBehindADoorThatOnlyThisHouseholdCanUse().submit()
    NumberOfBedrooms.setNumberOfBedroomsAnswer(3).submit()
    CentralHeating.clickCentralHeatingAnswerGas().submit()
    OwnOrRent.clickOwnOrRentAnswerOwnsOutright().submit()
    NumberOfVehicles.setNumberOfVehiclesAnswer(2).submit()
    HouseholdAndAccommodationCompleted.submit()

    // household-member
    HouseholdMemberBegin.submit()
    DetailsCorrect.clickDetailsCorrectAnswerYesThisIsMyFullName().submit()
    Over16.clickOver16AnswerYes().submit()
    PrivateResponse.clickPrivateResponseAnswerNoIDoNotWantToRequestAPersonalForm().submit()
    Sex.clickSexAnswerMale().submit()
    DateOfBirth.setDateOfBirthAnswerDay(2).setDateOfBirthAnswerMonth(3).setDateOfBirthAnswerYear(1980).submit()
    MaritalStatus.clickMaritalStatusAnswerMarried().submit()
    AnotherAddress.clickAnotherAddressAnswerNo().submit()
    InEducation.clickInEducationAnswerNo().submit()
    CountryOfBirth.clickCountryOfBirthEnglandAnswerEngland().submit()
    Carer.clickCarerAnswerNo().submit()
    NationalIdentity.clickNationalIdentityEnglandAnswerEnglish().submit()
    EthnicGroup.clickEthnicGroupEnglandAnswerWhite().submit()
    WhiteEthnicGroup.clickWhiteEthnicGroupEnglandAnswerEnglishWelshScottishNorthernIrishBritish().submit()
    Language.clickLanguageEnglandAnswerEnglish().submit()
    Religion.clickReligionAnswerNoReligion().submit()
    PastUsualAddress.clickPastUsualAddressAnswerThisAddress().submit()
    Passports.clickPassportsAnswerUnitedKingdom().submit()
    Disability.clickDisabilityAnswerNo().submit()
    Qualifications.clickQualificationsEnglandAnswerUndergraduateDegree().submit()
    Volunteering.clickVolunteeringAnswerNo().submit()
    EmploymentType.clickEmploymentTypeAnswerNoneOfTheAbove().submit()
    expect(Jobseeker.isOpen()).to.be.true
  })

  it('Given I am answering question 28. Last week were you.., When I select multiple answers including none of the above, Then I am routed to 35. In your main job, are (were) you?', function () {
    startCensusQuestionnaire('census_household.json')

    // who-lives-here
    PermanentOrFamilyHome.clickPermanentOrFamilyHomeAnswerYes().submit()
    HouseholdComposition.setFirstName('John').addPerson().setFirstName('Jane', 1).submit()
    EveryoneAtAddressConfirmation.clickEveryoneAtAddressConfirmationAnswerYes().submit()
    OvernightVisitors.setOvernightVisitorsAnswer(0).submit()
    HouseholdRelationships.clickHouseholdRelationshipsAnswerHusbandOrWife().submit()
    WhoLivesHereCompleted.submit()

    // household-and-accommodation
    TypeOfAccommodation.clickTypeOfAccommodationAnswerWholeHouseOrBungalow().submit()
    TypeOfHouse.clickTypeOfHouseAnswerSemiDetached().submit()
    SelfContainedAccommodation.clickSelfContainedAccommodationAnswerYesAllTheRoomsAreBehindADoorThatOnlyThisHouseholdCanUse().submit()
    NumberOfBedrooms.setNumberOfBedroomsAnswer(3).submit()
    CentralHeating.clickCentralHeatingAnswerGas().submit()
    OwnOrRent.clickOwnOrRentAnswerOwnsOutright().submit()
    NumberOfVehicles.setNumberOfVehiclesAnswer(2).submit()
    HouseholdAndAccommodationCompleted.submit()

    // household-member
    HouseholdMemberBegin.submit()
    DetailsCorrect.clickDetailsCorrectAnswerYesThisIsMyFullName().submit()
    Over16.clickOver16AnswerYes().submit()
    PrivateResponse.clickPrivateResponseAnswerNoIDoNotWantToRequestAPersonalForm().submit()
    Sex.clickSexAnswerMale().submit()
    DateOfBirth.setDateOfBirthAnswerDay(2).setDateOfBirthAnswerMonth(3).setDateOfBirthAnswerYear(1980).submit()
    MaritalStatus.clickMaritalStatusAnswerMarried().submit()
    AnotherAddress.clickAnotherAddressAnswerNo().submit()
    InEducation.clickInEducationAnswerNo().submit()
    CountryOfBirth.clickCountryOfBirthEnglandAnswerEngland().submit()
    Carer.clickCarerAnswerNo().submit()
    NationalIdentity.clickNationalIdentityEnglandAnswerEnglish().submit()
    EthnicGroup.clickEthnicGroupEnglandAnswerWhite().submit()
    WhiteEthnicGroup.clickWhiteEthnicGroupEnglandAnswerEnglishWelshScottishNorthernIrishBritish().submit()
    Language.clickLanguageEnglandAnswerEnglish().submit()
    Religion.clickReligionAnswerNoReligion().submit()
    PastUsualAddress.clickPastUsualAddressAnswerThisAddress().submit()
    Passports.clickPassportsAnswerUnitedKingdom().submit()
    Disability.clickDisabilityAnswerNo().submit()
    Qualifications.clickQualificationsEnglandAnswerUndergraduateDegree().submit()
    Volunteering.clickVolunteeringAnswerNo().submit()
    EmploymentType.clickEmploymentTypeAnswerWorkingAsAnEmployee().clickEmploymentTypeAnswerOnAGovernmentSponsoredTrainingScheme().clickEmploymentTypeAnswerNoneOfTheAbove().submit()
    expect(MainJob.isOpen()).to.be.true
  })

  it('Given I am answering question 28. Last week were you.., When I select multiple answers excluding none of the above, Then I am routed to 35. In your main job, are (were) you?', function () {
    startCensusQuestionnaire('census_household.json')

    // who-lives-here
    PermanentOrFamilyHome.clickPermanentOrFamilyHomeAnswerYes().submit()
    HouseholdComposition.setFirstName('John').addPerson().setFirstName('Jane', 1).submit()
    EveryoneAtAddressConfirmation.clickEveryoneAtAddressConfirmationAnswerYes().submit()
    OvernightVisitors.setOvernightVisitorsAnswer(0).submit()
    HouseholdRelationships.clickHouseholdRelationshipsAnswerHusbandOrWife().submit()
    WhoLivesHereCompleted.submit()

    // household-and-accommodation
    TypeOfAccommodation.clickTypeOfAccommodationAnswerWholeHouseOrBungalow().submit()
    TypeOfHouse.clickTypeOfHouseAnswerSemiDetached().submit()
    SelfContainedAccommodation.clickSelfContainedAccommodationAnswerYesAllTheRoomsAreBehindADoorThatOnlyThisHouseholdCanUse().submit()
    NumberOfBedrooms.setNumberOfBedroomsAnswer(3).submit()
    CentralHeating.clickCentralHeatingAnswerGas().submit()
    OwnOrRent.clickOwnOrRentAnswerOwnsOutright().submit()
    NumberOfVehicles.setNumberOfVehiclesAnswer(2).submit()
    HouseholdAndAccommodationCompleted.submit()

    // household-member
    HouseholdMemberBegin.submit()
    DetailsCorrect.clickDetailsCorrectAnswerYesThisIsMyFullName().submit()
    Over16.clickOver16AnswerYes().submit()
    PrivateResponse.clickPrivateResponseAnswerNoIDoNotWantToRequestAPersonalForm().submit()
    Sex.clickSexAnswerMale().submit()
    DateOfBirth.setDateOfBirthAnswerDay(2).setDateOfBirthAnswerMonth(3).setDateOfBirthAnswerYear(1980).submit()
    MaritalStatus.clickMaritalStatusAnswerMarried().submit()
    AnotherAddress.clickAnotherAddressAnswerNo().submit()
    InEducation.clickInEducationAnswerNo().submit()
    CountryOfBirth.clickCountryOfBirthEnglandAnswerEngland().submit()
    Carer.clickCarerAnswerNo().submit()
    NationalIdentity.clickNationalIdentityEnglandAnswerEnglish().submit()
    EthnicGroup.clickEthnicGroupEnglandAnswerWhite().submit()
    WhiteEthnicGroup.clickWhiteEthnicGroupEnglandAnswerEnglishWelshScottishNorthernIrishBritish().submit()
    Language.clickLanguageEnglandAnswerEnglish().submit()
    Religion.clickReligionAnswerNoReligion().submit()
    PastUsualAddress.clickPastUsualAddressAnswerThisAddress().submit()
    Passports.clickPassportsAnswerUnitedKingdom().submit()
    Disability.clickDisabilityAnswerNo().submit()
    Qualifications.clickQualificationsEnglandAnswerUndergraduateDegree().submit()
    Volunteering.clickVolunteeringAnswerNo().submit()
    EmploymentType.clickEmploymentTypeAnswerWorkingAsAnEmployee().clickEmploymentTypeAnswerOnAGovernmentSponsoredTrainingScheme().submit()
    expect(MainJob.isOpen()).to.be.true
  })
})
