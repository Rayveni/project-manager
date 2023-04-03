from flask import jsonify,request,Response

from . import api_bp


@api_bp.route("/uploads_info", methods=['GET', 'POST'])
def uploads_info():

    return jsonify({'ff':123}) 

