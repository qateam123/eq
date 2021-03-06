import chai from 'chai'
import {startCensusQuestionnaire} from '../../../helpers'
import {completeHouseholdAndAccommodation, completeVisitorSection} from '../complete-section'

import PermanentOrFamilyHome from '../../../pages/surveys/census/household/permanent-or-family-home.page.js'
import ElsePermanentOrFamilyHome from '../../../pages/surveys/census/household/else-permanent-or-family-home.page.js'
import HouseholdComposition from '../../../pages/surveys/census/household/household-composition.page.js'
import EveryoneAtAddressConfirmation from '../../../pages/surveys/census/household/everyone-at-address-confirmation.page.js'
import OvernightVisitors from '../../../pages/surveys/census/household/overnight-visitors.page.js'
import HouseholdRelationships from '../../../pages/surveys/census/household/household-relationships.page.js'
import WhoLivesHereCompleted from '../../../pages/surveys/census/household/who-lives-here-completed.page.js'
import TypeOfAccommodation from '../../../pages/surveys/census/household/type-of-accommodation.page.js'
import TypeOfHouse from '../../../pages/surveys/census/household/type-of-house.page.js'
import TypeOfFlat from '../../../pages/surveys/census/household/type-of-flat.page.js'
import SelfContainedAccommodation from '../../../pages/surveys/census/household/self-contained-accommodation.page.js'
import NumberOfBedrooms from '../../../pages/surveys/census/household/number-of-bedrooms.page.js'
import CentralHeating from '../../../pages/surveys/census/household/central-heating.page.js'
import OwnOrRent from '../../../pages/surveys/census/household/own-or-rent.page.js'
import Landlord from '../../../pages/surveys/census/household/landlord.page.js'
import NumberOfVehicles from '../../../pages/surveys/census/household/number-of-vehicles.page.js'
import HouseholdAndAccommodationCompleted from '../../../pages/surveys/census/household/household-and-accommodation-completed.page.js'
import HouseholdMemberBegin from '../../../pages/surveys/census/household/household-member-begin.page.js'
import DetailsCorrect from '../../../pages/surveys/census/household/details-correct.page.js'
import CorrectName from '../../../pages/surveys/census/household/correct-name.page.js'
import Over16 from '../../../pages/surveys/census/household/over-16.page.js'
import PrivateResponse from '../../../pages/surveys/census/household/private-response.page.js'
import RequestPrivateResponse from '../../../pages/surveys/census/household/request-private-response.page.js'
import Sex from '../../../pages/surveys/census/household/sex.page.js'
import DateOfBirth from '../../../pages/surveys/census/household/date-of-birth.page.js'
import MaritalStatus from '../../../pages/surveys/census/household/marital-status.page.js'
import AnotherAddress from '../../../pages/surveys/census/household/another-address.page.js'
import OtherAddress from '../../../pages/surveys/census/household/other-address.page.js'
import AddressType from '../../../pages/surveys/census/household/address-type.page.js'
import InEducation from '../../../pages/surveys/census/household/in-education.page.js'
import TermTimeLocation from '../../../pages/surveys/census/household/term-time-location.page.js'
import CountryOfBirth from '../../../pages/surveys/census/household/country-of-birth.page.js'
import ArriveInUk from '../../../pages/surveys/census/household/arrive-in-uk.page.js'
import LengthOfStay from '../../../pages/surveys/census/household/length-of-stay.page.js'
import Carer from '../../../pages/surveys/census/household/carer.page.js'
import NationalIdentity from '../../../pages/surveys/census/household/national-identity.page.js'
import EthnicGroup from '../../../pages/surveys/census/household/ethnic-group.page.js'
import WhiteEthnicGroup from '../../../pages/surveys/census/household/white-ethnic-group.page.js'
import MixedEthnicGroup from '../../../pages/surveys/census/household/mixed-ethnic-group.page.js'
import AsianEthnicGroup from '../../../pages/surveys/census/household/asian-ethnic-group.page.js'
import BlackEthnicGroup from '../../../pages/surveys/census/household/black-ethnic-group.page.js'
import OtherEthnicGroup from '../../../pages/surveys/census/household/other-ethnic-group.page.js'
import SexualIdentity from '../../../pages/surveys/census/household/sexual-identity.page.js'
import UnderstandWelsh from '../../../pages/surveys/census/household/understand-welsh.page.js'
import Language from '../../../pages/surveys/census/household/language.page.js'
import English from '../../../pages/surveys/census/household/english.page.js'
import Religion from '../../../pages/surveys/census/household/religion.page.js'
import PastUsualAddress from '../../../pages/surveys/census/household/past-usual-address.page.js'
import LastYearAddress from '../../../pages/surveys/census/household/last-year-address.page.js'
import Passports from '../../../pages/surveys/census/household/passports.page.js'
import OtherPassports from '../../../pages/surveys/census/household/other-passports.page.js'
import Disability from '../../../pages/surveys/census/household/disability.page.js'
import Qualifications from '../../../pages/surveys/census/household/qualifications.page.js'
import Volunteering from '../../../pages/surveys/census/household/volunteering.page.js'
import EmploymentType from '../../../pages/surveys/census/household/employment-type.page.js'
import Jobseeker from '../../../pages/surveys/census/household/jobseeker.page.js'
import JobAvailability from '../../../pages/surveys/census/household/job-availability.page.js'
import JobPending from '../../../pages/surveys/census/household/job-pending.page.js'
import Occupation from '../../../pages/surveys/census/household/occupation.page.js'
import EverWorked from '../../../pages/surveys/census/household/ever-worked.page.js'
import MainJob from '../../../pages/surveys/census/household/main-job.page.js'
import JobTitle from '../../../pages/surveys/census/household/job-title.page.js'
import JobDescription from '../../../pages/surveys/census/household/job-description.page.js'
import EmployersBusiness from '../../../pages/surveys/census/household/employers-business.page.js'
import MainJobType from '../../../pages/surveys/census/household/main-job-type.page.js'
import BusinessName from '../../../pages/surveys/census/household/business-name.page.js'
import HouseholdMemberCompleted from '../../../pages/surveys/census/household/household-member-completed.page.js'
import VisitorBegin from '../../../pages/surveys/census/household/visitor-begin.page.js'
import VisitorName from '../../../pages/surveys/census/household/visitor-name.page.js'
import VisitorSex from '../../../pages/surveys/census/household/visitor-sex.page.js'
import VisitorDateOfBirth from '../../../pages/surveys/census/household/visitor-date-of-birth.page.js'
import VisitorUkResident from '../../../pages/surveys/census/household/visitor-uk-resident.page.js'
import VisitorAddress from '../../../pages/surveys/census/household/visitor-address.page.js'
import VisitorCompleted from '../../../pages/surveys/census/household/visitor-completed.page.js'
import VisitorsCompleted from '../../../pages/surveys/census/household/visitors-completed.page.js'
import Confirmation from '../../../pages/confirmation.page.js'
import ThankYou from '../../../pages/thank-you.page'

const expect = chai.expect

describe('Private response routing', function () {

    it('Given I have added a householder, When I request a private response for that person, Then I don\'t have to complete any more questions for them', function () {
        startCensusQuestionnaire('census_household.json', true)

        // who-lives-here
        PermanentOrFamilyHome.clickPermanentOrFamilyHomeAnswerYes().submit()

        // Given I have added a householder
        HouseholdComposition.setFirstName('Pete', 0).submit()
        EveryoneAtAddressConfirmation.clickEveryoneAtAddressConfirmationAnswerYes().submit()
        OvernightVisitors.setOvernightVisitorsAnswer(1).submit()
        WhoLivesHereCompleted.submit()

        // household-and-accommodation
        completeHouseholdAndAccommodation()

        // household-member
        HouseholdMemberBegin.submit()
        DetailsCorrect.clickDetailsCorrectAnswerYesThisIsMyFullName().submit()
        Over16.clickOver16AnswerYes().submit()

        // When I request a private response for that person
        PrivateResponse.clickPrivateResponseAnswerYesIWantToRequestAPersonalForm().submit()
        RequestPrivateResponse.submit()

        // Then I don\'t have to complete any more questions for them
        HouseholdMemberCompleted.submit()

        // visitors
        completeVisitorSection()
        VisitorsCompleted.submit()

        Confirmation.submit()

        // Thank You
        expect(ThankYou.isOpen()).to.be.true
    })

})
