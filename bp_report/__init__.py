# Реализация сценария "работа с отчетами"

import os
import json

from access import login_required, group_required
from database.sql_provider import SQLProvider
from flask import Blueprint, render_template, request, current_app
from model import model_route


bp_report = Blueprint('bp_report', __name__, template_folder='templates', url_prefix='/report')

report_provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


with open('data/db_reports.json') as f:
    current_app.config['db_reports'] = json.load(f)


@bp_report.route(rule='/', methods=['GET'])
def report_menu():
    return render_template(
        template_name_or_list='report_menu.html',
    )
