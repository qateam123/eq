import logging
import os
import time

from flask import Blueprint
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import g
from werkzeug.exceptions import NotFound
from flask_themes2 import render_theme_template
from werkzeug.exceptions import NotFound

from app.submitter.submitter import SubmitterFactory

from app.cryptography.jwt_encoder import Encoder
from app.schema_loader.schema_loader import available_schemas

from datetime import datetime, timezone

# pylint: disable=too-many-locals
logger = logging.getLogger(__name__)
feedback_blueprint = Blueprint('feedback', __name__, template_folder='templates')

@feedback_blueprint.before_request
def check_feedback_state():
    if session.get('feedback') == True:
        g.referrer = request.referrer
    else:
        raise NotFound



@feedback_blueprint.route('/feedback', methods=['GET', 'POST'])
def get_feedback():
    if request.method == "POST":
        form = request.form
        satisfaction = request.form['satisfaction']
        survey_type = request.form['surveyType']
        comment = request.form['comment']
        submitted_at = datetime.now(timezone.utc)

        message = {
            'submitted_at': submitted_at.isoformat(),
            'survey_type': survey_type,
            'satisfaction': satisfaction,
            'comment': comment
        }

        submitter = SubmitterFactory.get_submitter()
        submitter.send_answers(message, eqSurvey = False)

        session.clear()
        return render_template("thank-you-feedback.html")

    if g.referrer is not None:
        values = g.referrer[7:].split("/")
        return render_template("feedback.html", form_type = values[3])
    else:
        raise NotFound
