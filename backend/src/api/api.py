from flask import jsonify,request
from . import api_bp
from .gapi_calendar import *

g_calendar=google_calendar(get_secret_path())


@api_bp.route("/calendar", methods=['GET', 'POST'])
def calendar():
    return jsonify({1:2})
    #return jsonify(g_calendar.calendar_list()) 

@api_bp.route("/calendar/list", methods=['GET'])
def calendar_list():
    list_type = request.args.get('type', default = 'settings', type = str)
    if list_type!='settings':
        res=g_calendar.calendar_list()
    else:
        res=get_calendar_list()
    return jsonify(res)
    #return jsonify(g_calendar.calendar_list()) 

