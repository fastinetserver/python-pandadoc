from abc import ABC
from enum import Enum
from typing import List, Dict

from .panda_exceptions import ApiException
from .pandarecipient import Pandarecipient


class DocumentIdRequiredException(Exception):
    pass


class PandaDocumentDoesNotExist(Exception):
    pass


class PandaDocumentAbstract(ABC):
    _pandaworkspace = None

    def __init__(self, id_: str = None):
        """
        :str id: - Id provided by Panda
        """
        if id_ is None:
            raise DocumentIdRequiredException()
        self.__id = id_

    @property
    def id(self):
        return self.__id

    class Document(str, Enum):
        draft = 0
        sent = 1
        completed = 2
        viewed = 5
        waiting_approval = 6
        approved = 7
        rejected = 8
        waiting_pay = 9
        paid = 10
        voided = 11
        declined = 12

    @classmethod
    def list(
            cls,
            q: str = None,
            tag: str = None,
            status_: Document = None,
            count: int = None,
            page: int = None,
            metadata: str = None,
            deleted: bool = None,
            id_: str = None,
            template_id: str = None,
            folder_uuid: str = None,
    ) -> List[Dict]:
        """
            :param q: str: Optional search query. Filter by document reference number (this token is stored on template level) or name.
            :param tag: str: Optional search tag. Filter by document tag.
            :param status_: PandaDocumentStatus: Optionally specify the status of documents to return.
            :param count: int: Optionally specify how many document results to return. Default is 50 documents, maximum is 100 documents.
            :param page: int: Optionally specify which page of the dataset to return.
            :param metadata: str: Optionally specify metadata to filter by in the format of metadata_{metadata-key}={metadata-value} such as metadata_opportunity_id=2181432. The metadata_ prefix is always required.
            :param deleted: bool: Optionally returns only deleted documents
            :param id_: str: Optionally specify document's ID
            :param template_id: str: Optionally specify template used for documents creation.
            :param folder_uuid: str: The UUID of the folder where the documents are stored.
            :return List[Dict]: List of documents
        """

        data = {}
        if q:
            data['q'] = q
        if tag:
            data['tag'] = tag
        if status_:
            data['status'] = status_
        if count:
            data['count'] = count
        if page:
            data['page'] = page
        if metadata:
            data['metadata'] = metadata
        if deleted is not None:
            data['deleted'] = deleted
        if id_:
            data['id'] = id_
        if template_id:
            data['template_id'] = template_id
        if folder_uuid:
            data['folder_uuid'] = folder_uuid

        response = cls._pandaworkspace.get('documents', data=data)
        if response.status_code != 200:
            raise ApiException(response.text)
        results = response.json().get('results')
        return results

    @classmethod
    def create(
            cls,
            template_uuid: str,
            recipients: List[Pandarecipient],
            name: str = 'Sample Template',
            folder_uuid: str = '',
            tokens: List[Dict] = None
    ):
        """
        :param folder_uuid:
        :param recipients:
        :param name:
        :param template_uuid: e.g.: "Cu7KZisX2Hrnug6FgrYX4d"
        :param tokens:
        :return:
        """
        data = {
            "name": name,
            "template_uuid": template_uuid,
            "recipients": [recipient.as_dict for recipient in recipients],
        }
        if folder_uuid:
            data['folder_uuid'] = folder_uuid
        if tokens:
            data['tokens'] = tokens

        response = cls._pandaworkspace.post('documents', data=data)
        response_json = response.json()
        document_id = response_json.get('id', None)
        print("document_id:", document_id)
        return cls(document_id)

    def send(
            self,
            message: str = 'Hello! This document was sent from the PandaDoc API.',
            subject: str = 'Please check this test API document from PandaDoc',
            silent: bool = False,
    ) -> Dict:
        """
        :param message:
        :param subject:
        :param silent:
        :return:
        """
        if self.id is None:
            raise PandaDocumentDoesNotExist()

        data = {
            "message": message,
            "subject": subject,
            "silent": silent,
        }
        response = self.__class__._pandaworkspace.post(
            'documents/{document_id}/send'.format(document_id=self.id),
            data=data,
        )
        return response.json()

    def status(self) -> Dict:
        response = self.__class__._pandaworkspace.get('documents/{document_id}'.format(document_id=self.id))
        return response.json()

    def details(self) -> Dict:
        response = self.__class__._pandaworkspace.get('documents/{document_id}/details'.format(document_id=self.id))
        return response.json()

    def delete(self) -> int:
        response = self.__class__._pandaworkspace.delete('documents/{document_id}'.format(document_id=self.id))
        return response.status_code

    def share(self, recipient: Pandarecipient, lifetime: int = 3600):
        """
        :type recipient: Pandarecipient
        :type lifetime: int - Provide the number of seconds for which a document link should be valid for.
         Default is 3600 seconds.
        """
        data = {
            "recipient": recipient.email,
            "lifetime": lifetime,
        }
        response = self.__class__._pandaworkspace.post(
            'documents/{document_id}/session'.format(document_id=self.id),
            data=data,
        )
        link_id = response.json().get('id', None)
        if link_id:
            return self.__class__._pandaworkspace.get_app_url(uri='s/{link_id}'.format(link_id=link_id))
        else:
            raise ApiException(response)

    def download(self, filename=None, download_folder=None) -> str:
        return self.__class__._pandaworkspace.download(
            'documents/{document_id}/download'.format(document_id=self.id),
            filename,
            download_folder,
        )

    def download_protected(self, filename=None, download_folder=None) -> str:
        return self.__class__._pandaworkspace.download(
            'documents/{document_id}/download-protected'.format(document_id=self.id),
            filename,
            download_folder,
        )

    def download_large(self, filename=None, download_folder=None) -> str:
        return self.__class__._pandaworkspace.download_large(
            'documents/{document_id}/download'.format(document_id=self.id),
            filename,
            download_folder
        )
