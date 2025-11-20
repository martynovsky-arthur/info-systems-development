import os

from access import group_required, login_required
from database.sql_provider import SQLProvider
from flask import Blueprint, redirect, render_template, request, url_for
from model import Model


bp_report = Blueprint('bp_report', __name__, template_folder='templates', url_prefix='/report')

report_model: Model
reports_cfg: dict

@bp_report.record
def on_register(setup_state):
    global report_model, reports_cfg
    app = setup_state.app
    report_provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))
    report_model = Model(app.config['db_config'], report_provider)
    reports_cfg = app.config.get('reports', {})


@bp_report.route('/', methods=['GET'])
@login_required
def report_menu():
    return render_template('report_menu.html')


@bp_report.route('/<report_type>', methods=['GET'])
@group_required
def handle_report(report_type):
    if not report_type in reports_cfg:
        return render_template('error.html', msg='Неизвестный тип отчета')

    return render_template(
        'report_form.html',
        report_type=report_type,
        report_name=reports_cfg.get(report_type).get('name', 'Отчет'),
        description=reports_cfg.get(report_type).get('description')
    )


@bp_report.route('/<report_type>/create', methods=['POST'])
@group_required
def create_report(report_type):
    if not report_type in reports_cfg:
        return render_template('error.html', msg='Неизвестный тип отчета')

    month = request.values.get('month')
    year = request.values.get('year')

    if not month or not year:
        return redirect(url_for('bp_report.handle_report', report_type=report_type))

    result_create = report_model.select(
        reports_cfg.get(report_type, {}).get('sql_create', ''),
        {'month': month, 'year': year}
    )

    return render_template(
        'report_create.html',
        report_type=report_type,
        report_name=reports_cfg.get(report_type, {}).get('name', 'Отчет'),
        message=result_create[0]['message'],
    )


@bp_report.route('/<report_type>/read', methods=['POST'])
@group_required
def read_report(report_type):
    if not report_type in reports_cfg:
        return render_template('error.html', msg='Неизвестный тип отчета')

    month = request.values.get('month')
    year = request.values.get('year')

    if not month or not year:
        return redirect(url_for('bp_report.handle_report', report_type=report_type))

    result_read = report_model.select(
        reports_cfg.get(report_type, {}).get('sql_read', ''),
        {'month': month, 'year': year}
    )

    return render_template(
        'report_read.html',
        report_type=report_type,
        report_name=reports_cfg.get(report_type, {}).get('name', 'Отчет'),
        fields=reports_cfg.get(report_type, {}).get('fields', []),
        items=result_read,
    )
