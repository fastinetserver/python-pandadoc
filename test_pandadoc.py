"""pandarecipient.py implements tests for API Wrapper https://developers.pandadoc.com/reference#about"""

__author__ = "Kostyantyn Ovechko"
__copyright__ = "Copyright 2020, Zxscript"
__license__ = "MIT"
__version__ = "0.0.1"
__email__ = "kos@zxscript.com"
__status__ = "Production"


import os
import re

import pytest

from .sleep_request_limit_manager import SleepRequestLimitManager
from .pandaworkspace import PandaWorkspace
from .pandarecipient import Pandarecipient


TEST_TEMPLATE_UUID = os.environ.get('TEST_TEMPLATE_UUID', 'ZXYzyxsX2Hrnug6FgrYX4d')
TEST_FOLDER_UUID = os.environ.get('TEST_FOLDER_UUID', 'ABCzyxsX2Hrnug6FgrYX4d')

TEST_TEMPLATE_DELETE_UUID = os.environ.get('TEST_TEMPLATE_DELETE_UUID', 'ZYxyzeyXdTHHxCV5K5PoQH')
# TEST_FOLDER_DELETE_UUID = os.environ.get('TEST_TEMPLATE_DELETE_UUID', 'a7y3zgpmk3cfmMryEJxaRM')

@pytest.fixture
def pandadoc():
    return PandaWorkspace(request_limit_manager=SleepRequestLimitManager)


@pytest.fixture
def recipients():
    employee = Pandarecipient(
        email='employee@example.com',
        first_name='Kos',
        last_name='Smarty',
        role='Employee',
    )
    employer = Pandarecipient(
        email='employer@example.com',
        first_name='Kos',
        last_name='Ovechko',
        role='Employer',
    )
    return [employee, employer]


@pytest.fixture
def a_pandadocument(pandadoc, recipients):
    tokens = [
        {
            'name': 'Favorite.Pet',
            'value': 'Panda',
        },
        {
            'name': 'Best.Friend',
            'value': 'David Schwimmer',
        },
    ]
    return pandadoc.documents.create(
        template_uuid=TEST_TEMPLATE_UUID,
        recipients=recipients,
        name="Test Document",
        tokens=tokens
    )


def test_document_create(a_pandadocument):
    assert type(a_pandadocument.id) == str
    assert len(a_pandadocument.id) > 10
    assert a_pandadocument.delete() == 204


def test_document_create_in_folder(pandadoc, recipients):
    document = pandadoc.documents.create(
        template_uuid=TEST_TEMPLATE_UUID,
        folder_uuid=TEST_FOLDER_UUID,
        recipients=recipients,
        name="Test Document in Folder",
    )
    assert type(document.id) == str
    assert len(document.id) > 10
    assert document.delete() == 204


def test_document_send(a_pandadocument):
    result = a_pandadocument.send(
        message='TEST: Sending through PandaDoc API. If you see it then the test works.',
        subject='TEST: Sending through PandaDoc API.',
        silent=False,
    )
    assert result.get('status', None) == 'document.sent'
    assert result.get('id', None) == a_pandadocument.id
    assert a_pandadocument.delete() == 204


def test_document_status(a_pandadocument):
    assert a_pandadocument.status().get('status', None) == 'document.draft'
    assert a_pandadocument.delete() == 204


def test_document_details(a_pandadocument):
    assert a_pandadocument.details().get('status', None) == 'document.draft'
    assert a_pandadocument.delete() == 204


def test_document_share(a_pandadocument, recipients):
    a_pandadocument.send(
        message='TEST: Sending through PandaDoc API. If you see it then the test works.',
        subject='TEST: Sending through PandaDoc API.',
        silent=False,
    )
    share_url = a_pandadocument.share(recipient=recipients[0], lifetime=72000)
    print("Share Url:", share_url)
    assert re.match('https://app.pandadoc.com/s/[\d\w]+', share_url)
    assert a_pandadocument.delete() == 204


def test_document_download(a_pandadocument):
    result = a_pandadocument.send(
        message='TEST: Sending through PandaDoc API. If you see it then the test works.',
        subject='TEST: Sending through PandaDoc API.',
        silent=False,
    )
    assert result.get('status', None) == 'document.sent'
    assert result.get('id', None) == a_pandadocument.id
    filepath = a_pandadocument.download()
    print("Downloaded file:", filepath)
    assert a_pandadocument.delete() == 204


def test_document_download_large(a_pandadocument):
    result = a_pandadocument.send(
        message='TEST: Sending through PandaDoc API. If you see it then the test works.',
        subject='TEST: Sending through PandaDoc API.',
        silent=False,
    )
    assert result.get('status', None) == 'document.sent'
    assert result.get('id', None) == a_pandadocument.id
    filepath = a_pandadocument.download_large()
    print("Downloaded file:", filepath)
    assert a_pandadocument.delete() == 204


def test_document_download_protected(a_pandadocument):
    result = a_pandadocument.send(
        message='TEST: Sending through PandaDoc API. If you see it then the test works.',
        subject='TEST: Sending through PandaDoc API.',
        silent=False,
    )
    assert result.get('status', None) == 'document.sent'
    assert result.get('id', None) == a_pandadocument.id
    filepath = a_pandadocument.download_protected()
    print("Downloaded file:", filepath)
    assert a_pandadocument.delete() == 204


def test_document_list(pandadoc):
    results = pandadoc.documents.list(status_=pandadoc.documents.Document.sent)
    for result in results:
        print(result.get('id', None), "   >   ", result.get('status', None))
        assert type(result.get('id', None)) == str
        assert len(result.get('id', '')) > 5


def test_template_list(pandadoc):
    results = pandadoc.templates.list()
    for result in results:
        print(result.get('id', None), "   >   ", result.get('name', None))
        assert type(result.get('id', None)) == str
        assert len(result.get('id', '')) > 5


def test_template_details(pandadoc):
    a_pandatemplate = pandadoc.templates(template_id=TEST_TEMPLATE_UUID)
    result = a_pandatemplate.details()
    assert type(result.get('created_by', None)) == dict


# def test_template_delete(pandadoc):
#     """Api to delete templates not Implemented by PandaDoc at the moment when this code was written"""
#     a_pandatemplate = pandadoc.templates(template_id=TEST_TEMPLATE_DELETE_UUID)
#     assert a_pandatemplate.delete() == 204


def test_documents_folder_list(pandadoc):
    results = pandadoc.document_folders.list(count=2, page=0)
    for result in results:
        print(result.get('uuid', None), "   >   ", result.get('name', None))
        assert type(result.get('uuid', None)) == str
        assert len(result.get('uuid', '')) > 5


def test_documents_folder_create_and_rename(pandadoc):
    folder_name = 'Api created Folder'
    a_folder = pandadoc.document_folders.create(name=folder_name)
    print(a_folder.uuid, "   >   ", a_folder.name)
    assert len(a_folder.uuid) > 5
    assert a_folder.name == folder_name
    assert a_folder.rename('Api Renamed Folder') == 201


# def test_documents_folder_delete(pandadoc):
#     a_folder = PandaDocumentsFolder(pandadoc, uuid=TEST_FOLDER_DELETE_UUID)
#     assert a_folder.delete() == 405


def test_templates_folder_list(pandadoc):
    results = pandadoc.tempate_folders.list(count=2, page=0)
    for result in results:
        print(result.get('uuid', None), "   >   ", result.get('name', None))
        assert type(result.get('uuid', None)) == str
        assert len(result.get('uuid', '')) > 5


def test_templates_folder_create_and_rename(pandadoc):
    folder_name = 'Api created Folder'
    a_folder = pandadoc.tempate_folders.create(name=folder_name)
    print(a_folder.uuid, "   >   ", a_folder.name)
    assert len(a_folder.uuid) > 5
    assert a_folder.name == folder_name
    assert a_folder.rename('Api Renamed Folder') == 201
