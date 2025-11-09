import os
import json

from flask import Blueprint, render_template, request, current_app, redirect, url_for
from access import group_required
from database.sql_provider import SQLProvider
from model import model_route


bp_report = Blueprint('bp_report', __name__, template_folder='templates', url_prefix='/report')

report_provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@bp_report.route('/', methods=['GET'])
@group_required
def report_menu():
    return render_template('report_menu.html')


@bp_report.route('/handle/<report_type>', methods=['GET', 'POST'])
# @group_required
def handle_report(report_type):
    reports_cfg = current_app.config.get('db_reports', {})

    if not report_type in reports_cfg:
        return render_template('error.html', msg='Неизвестный тип отчета')

    if request.method == 'GET':
        return render_template(
            'report_form.html',
            report_type=report_type,
            report_name=reports_cfg.get(report_type).get('name', 'Отчет'),
            description=reports_cfg.get(report_type).get('description')
        )

    month = request.values.get('month')
    year = request.values.get('year')
    action = request.values.get('action')

    if not month or not year:
        return render_template('error.html', msg='Укажите месяц и год')

    if not action in ('Создать', 'Посмотреть',):
        return render_template('error.html', msg='Неизвестное действие')

    if action == 'Создать':
        result = model_route(
            report_provider,
            reports_cfg.get(report_type, {}).get('sql_create', ''),
            {'month': month, 'year': year}
        )

        if not result.status:
            return render_template('error.html', msg=f'Ошибка создания отчета: {result.err_message}')

    result = model_route(
        report_provider,
        reports_cfg.get(report_type, {}).get('sql_read', ''),
        {'month': month, 'year': year}
    )

    if not result.status:
        return render_template('error.html', msg=result.err_message)

    return render_template(
        'report_result.html',
        report_type=report_type,
        report_name=reports_cfg.get(report_type, {}).get('name', 'Отчет'),
        fields=reports_cfg.get(report_type, {}).get('fields', []),
        items=result.result,
        message=request.args.get('message'),
    )


@bp_report.route('/create/<report_type>', methods=['POST'])
# @group_required
def create_report(report_type):
    reports_cfg = current_app.config.get('db_reports', {})

    if not report_type in reports_cfg:
        return render_template('error.html', msg='Неизвестный тип отчета')

    month = request.values.get('month')
    year = request.values.get('year')
    if not month or not year:
        return redirect('/report/handle/revenue')



    return redirect(url_for('bp_report.read_report', report_type=report_type, month=month, year=year, message=result.result[0][0]))


@bp_report.route('/read/<report_type>', methods=['GET'])
# @group_required
def read_report(report_type):
    reports_cfg = current_app.config.get('db_reports', {})

    if not report_type in reports_cfg:
        return render_template('error.html', msg='Неизвестный тип отчета')

    month = request.args.get('month')
    year = request.args.get('year')

    if not month or not year:
        return redirect('/report/handle/revenue')
