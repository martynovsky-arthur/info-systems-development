import os
import json

from flask import Blueprint, render_template, request, current_app, redirect, url_for
from access import group_required, login_required
from database.sql_provider import SQLProvider
from model import model_route


bp_report = Blueprint('bp_report', __name__, template_folder='templates', url_prefix='/report')

report_provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@bp_report.route('/', methods=['GET'])
@login_required
def report_menu():
    return render_template('report_menu.html')


@bp_report.route('/<report_type>', methods=['GET'])
@group_required
def handle_report(report_type):
    reports_cfg = current_app.config.get('db_reports', {})

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
    reports_cfg = current_app.config.get('db_reports', {})

    if not report_type in reports_cfg:
        return render_template('error.html', msg='Неизвестный тип отчета')

    month = request.values.get('month')
    year = request.values.get('year')

    if not month or not year:
        return redirect(url_for('bp_report.handle_report', report_type=report_type))

    result_create = model_route(
        report_provider,
        reports_cfg.get(report_type, {}).get('sql_create', ''),
        {'month': month, 'year': year}
    )

    if not result_create.status:
        return render_template('error.html', msg=f'Ошибка создания отчета: {result_create.err_message}')

    return render_template('report_create.html', report_type=report_type, message=result_create.result[0][0])


@bp_report.route('/<report_type>/read', methods=['POST'])
@group_required
def read_report(report_type):
    reports_cfg = current_app.config.get('db_reports', {})

    if not report_type in reports_cfg:
        return render_template('error.html', msg='Неизвестный тип отчета')

    month = request.values.get('month')
    year = request.values.get('year')

    if not month or not year:
        return redirect(url_for('bp_report.handle_report', report_type=report_type))

    result_read = model_route(
        report_provider,
        reports_cfg.get(report_type, {}).get('sql_read', ''),
        {'month': month, 'year': year}
    )

    if not result_read.status:
        return render_template('error.html', msg=result_read.err_message)

    return render_template(
        'report_read.html',
        report_type=report_type,
        report_name=reports_cfg.get(report_type, {}).get('name', 'Отчет'),
        fields=reports_cfg.get(report_type, {}).get('fields', []),
        items=result_read.result,
    )
