from flask import Blueprint, jsonify
from datetime import datetime, timedelta

week_blueprint = Blueprint('week_blueprint', __name__)

@week_blueprint.route('/get_this_week')
def get_this_week():
    today = datetime.today()
    monday = today - timedelta(days=today.weekday())
    sunday = monday + timedelta(days=6)
    return  jsonify({"monday": monday.strftime("%Y-%m-%d"), "sunday": sunday.strftime("%Y-%m-%d")}), 201

@week_blueprint.route('/get_next_week')
def get_next_week():
    today = datetime.today()
    monday = today - timedelta(days=today.weekday()) + timedelta(days=7)
    sunday = monday + timedelta(days=6)
    return  jsonify({"monday": monday.strftime("%Y-%m-%d"), "sunday": sunday.strftime("%Y-%m-%d")}), 201