from flask import jsonify,request,Response
from os import getenv
from . import api_bp
from .gapi_calendar import google_calendar

g_calendar=google_calendar(getenv('gapi_secret_path'))

@api_bp.route("/calendar", methods=['GET', 'POST'])
def calendar():
    return jsonify(g_calendar.calendar_list()) 

