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

@api_bp.route("/calendar/events", methods=['GET'])
def calendar_events():
    start_date = request.args.get('start', None)
    end_date = request.args.get('end', None)
    # You'd normally use the variables above to limit the data returned
    # you don't want to return ALL events like in this code
    # but since no db or any real storage is implemented I'm just
    # returning data from a text file that contains json elements

    _worker=lambda item:[format_event(_event,item['color']) for _event 
                         in g_calendar.events(item['id'],start_date,end_date)['events']
                         ]
   
    calendar_list=[{'id':"ru.russian#holiday@group.v.calendar.google.com",'color':'blue'},
                  { 'id':"62bb6be75cd5ea029a193e5ba62a5bd3e1c8224ed938d9516863296289a937f2@group.calendar.google.com",'color':'purple'}
                  ]

    formatted_events=list(map(_worker,calendar_list))
    return jsonify(sum(formatted_events,[]))

