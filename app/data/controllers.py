import os
import json
import random

from datetime import datetime
from app.util import allowed_file
from app.auth_utilities import permission_required
from app.models import RoleAccountPasswordReset, NamedAccountPasswordReset
from flask import render_template, request, flash, redirect, current_app, url_for
from flask_login import login_required
from azure.storage.blob import ContentSettings
from app import azs, celery, csrf

from . import data


@data.route('/resets/update/named', methods=['POST', 'GET'])
@login_required
@permission_required('pwr_upload')
@csrf.exempt
def update_named():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part', 'error')
            return redirect(url_for('data.update_named'))
        file = request.files['file']
        if file.filename == '':
            flash('No selected file', 'error')
            return redirect(request.url)
        if file:
            if allowed_file(file.filename, current_app.config['ALLOWED_EXTENSIONS']):
                fn = upload_csv_file(file, 'named', 'named-csv')
                process_named.delay(fn)
                flash('File Uploaded Successfully', 'success')
            else:
                flash('Invalid File Type', 'error')
    return render_template('data/update_named.html', title='Home')


@data.route('/resets/update/role', methods=['POST', 'GET'])
@login_required
@permission_required('pwr_upload')
@csrf.exempt
def update_role():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part', 'error')
            return redirect(url_for('data.update_role'))
        file = request.files['file']
        if file.filename == '':
            flash('No selected file', 'error')
            return redirect(request.url)
        if file:
            if allowed_file(file.filename, current_app.config['ALLOWED_EXTENSIONS']):
                fn = upload_csv_file(file, 'role', 'role-csv')
                process_role.delay(fn)
                flash('File Uploaded Successfully', 'success')
            else:
                flash('Invalid File Type', 'error')
    return render_template('data/update_role.html', title='Home')


def upload_csv_file(file, file_prefix, container):
    now = str(datetime.utcnow().isoformat())
    filename = '{}_{}.csv'.format(file_prefix, now)
    file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)
    azs.block_blob_service.create_blob_from_path(container_name=container,
                                                 blob_name=filename, file_path=file_path,
                                                 content_settings=ContentSettings(content_type='text/csv'))
    if os.path.isfile(file_path):
        os.remove(file_path)

    return filename


@celery.task
def process_role(file_name):
    local_path = os.path.join(current_app.config['UPLOAD_FOLDER'], file_name)
    azs.block_blob_service.get_blob_to_path(
        'role-csv',
        file_name,
        local_path
    )
    if os.path.isfile(local_path):
        update_csv_queue('role_account_password_resets', 'role-csv', file_name, 'roleImport', 'Role Import Start')
        try:
            RoleAccountPasswordReset.insert_resets(local_path)
            RoleAccountPasswordReset.clean_duplicates()
            os.remove(local_path)
        except Exception as err:
            err_msg = 'Exception: {0} \n Args: {1}'.format(str(type(err)), str(err))
            update_csv_queue('role_account_password_resets', 'role-csv', file_name, 'roleImportError', err_msg)
        update_csv_queue('role_account_password_resets', 'role-csv', file_name, 'roleImport', 'Role Import Completed')


@celery.task
def process_named(file_name):
    local_path = os.path.join(current_app.config['UPLOAD_FOLDER'], file_name)
    azs.block_blob_service.get_blob_to_path(
        'named-csv',
        file_name,
        local_path
    )
    if os.path.isfile(local_path):
        update_csv_queue('named_account_password_resets', 'named-csv', file_name, 'namedImport', 'Named Import Start')
        try:
            NamedAccountPasswordReset.insert_resets(local_path)
            NamedAccountPasswordReset.clean_duplicates()
            os.remove(local_path)
        except Exception as err:
            err_msg = 'Exception: {0} \n Args: {1}'.format(str(type(err)), str(err))
            update_csv_queue('named_account_password_resets', 'named-csv', file_name, 'namedImportError', err_msg)
        update_csv_queue('named_account_password_resets', 'named-csv', file_name,
                         'namedImport', 'Named Import Completed')


# Unused code for now.
@celery.task
def test_async():
    file_name = 'File_{}.txt'.format(random.randint(1, 101))
    file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], file_name)
    with open(file_path, "w") as text_file:
        text_file.write('Test of Celery.')

    azs.block_blob_service.create_blob_from_path(container_name='test-files',
                                                 blob_name=file_name, file_path=file_path,
                                                 content_settings=ContentSettings(content_type='text/plain'))


def update_csv_queue(database_table, blob_name, file_name, action, message):
    msg = {
        'database_table': database_table,
        'blob_name': blob_name,
        'file_name': file_name,
        'action': action,
        'message': message
    }
    msg = json.dumps(msg)
    azs.queue_service.put_message('csv-queue', msg)
