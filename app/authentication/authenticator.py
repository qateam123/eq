import logging

from flask import session
from flask_login import LoginManager

from app.authentication.invalid_token_exception import InvalidTokenException
from app.authentication.jwt_decoder import JWTDecryptor
from app.authentication.no_token_exception import NoTokenException
from app.authentication.session_storage import session_storage
from app.authentication.user import User
from app.authentication.user_id_generator import UserIDGenerator
from app.globals import get_questionnaire_store
from app.parser.metadata_parser import is_valid_metadata, parse_metadata

logger = logging.getLogger(__name__)


login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id):
    logger.debug("Loading user %s", user_id)
    authenticator = Authenticator()
    return authenticator.check_session()


@login_manager.request_loader
def request_load_user(request):
    logger.debug("Load user %s", request)
    authenticator = Authenticator()
    return authenticator.check_session()


class Authenticator(object):

    @staticmethod
    def check_session():
        """
        Checks for the present of the JWT in the users sessions
        :return: A user object if a JWT token is available in the session
        """
        logger.debug("Checking for session")
        if session_storage.has_user_id():
            user = User(session_storage.get_user_id(), session_storage.get_user_ik())
            questionnaire_store = get_questionnaire_store(user.user_id, user.user_ik)
            metadata = questionnaire_store.metadata

            logger.debug("Session token exists for tx_id=%s", metadata["tx_id"])

            return user
        else:
            logging.info("Session does not have an authenticated token")
            return None

    def jwt_login(self, request):
        """
        Login using a JWT token, this must be an encrypted JWT.
        :param request: The flask request
        """
        # clear the session entry in the database
        session_storage.clear()
        # also clear the secure cookie data
        session.clear()

        if request.args.get('token') is None:
            raise NoTokenException("Please provide a token")
        token = self._jwt_decrypt(request)

        # once we've decrypted the token correct
        # check we have the required user data
        self._check_user_data(token)

        # get the hashed user id for eq
        user_id = UserIDGenerator.generate_id(token)
        user_ik = UserIDGenerator.generate_ik(token)

        # store the user id in the session
        session_storage.store_user_id(user_id)
        # store the user ik in the cookie
        session_storage.store_user_ik(user_ik)

        # store the meta data
        metadata = parse_metadata(token)

        questionnaire_store = get_questionnaire_store(user_id, user_ik)
        questionnaire_store.metadata = metadata
        questionnaire_store.add_or_update()

        logger.info("User authenticated with tx_id=%s", metadata["tx_id"])

    @staticmethod
    def _jwt_decrypt(request):
        encrypted_token = request.args.get('token')
        decoder = JWTDecryptor()
        token = decoder.decrypt_jwt_token(encrypted_token)
        return token

    @staticmethod
    def _check_user_data(token):
        valid, field = is_valid_metadata(token)
        if not valid:
            raise InvalidTokenException("Missing value {}".format(field))
