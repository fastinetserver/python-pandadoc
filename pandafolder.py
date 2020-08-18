from typing import List, Dict
from abc import ABC, abstractmethod

from .panda_exceptions import ApiError


class FolderUuidRequired(Exception):
    pass


class PandaFolder(ABC):
    _pandadoc = None

    def __init__(self, uuid: str = None, name: str = None, date_created: str = None):
        """
        :type pandadoc: pandadoc
        """
        if uuid is None:
            raise FolderUuidRequired()
        self.__uuid = uuid
        self.__name = name
        self.__date_created = date_created

    @classmethod
    @abstractmethod
    def get_folder_type(cls):
        pass

    @property
    def uuid(self):
        return self.__uuid

    @property
    def name(self):
        return self.__name

    @property
    def date_created(self):
        return self.__date_created

    @classmethod
    def list(
            cls,
            parent_uuid: str = None,
            count: int = None,
            page: int = None,
    ) -> List[Dict]:
        """
            :param parent_uuid: str: The UUID of the folder containing folders. To list the folders located in the root folder, please remove this param in the request.
            :param count: int: Optionally specify how many folders to return. Default is 50 folders, maximum is 100 folders.
            :param page: int: Optionally specify which page of the dataset to return.
            :return List[Dict]: List of folders
        """

        data = {}
        if parent_uuid:
            data['parent_uuid'] = parent_uuid
        if count:
            data['count'] = count
        if page:
            data['page'] = page

        response = cls._pandadoc.get('{folder_type}/folders'.format(
            folder_type=cls.get_folder_type(),
        ), data=data)
        if response.status_code != 200:
            raise ApiError(response.text)
        results = response.json().get('results')
        return results

    @classmethod
    def create(
            cls,
            parent_uuid: str = None,
            name: str = 'Sample Template',
    ):
        """
        :param pandadoc:
        :param parent_uuid: ID of the parent folder
        :param name: Name for the new folder
        :param template_uuid: e.g.: "Cu7KZisX2Hrnug6FgrYX4d"
        :return:
        """
        data = {
            'name': name,
        }
        if parent_uuid:
            data['parent_uuid'] = parent_uuid

        response = cls._pandadoc.post('{folder_type}/folders'.format(folder_type=cls.get_folder_type()), data=data)
        response_json = response.json()
        folder_uuid = response_json.get('uuid', None)
        print("folder_uuid:", folder_uuid)
        panda_folder = cls(
            uuid=response_json.get('uuid', None),
            name=response_json.get('name', None),
            date_created=response_json.get('date_created', None),
        )
        return panda_folder

    def rename(self, new_name: str = 'New folder name') -> int:
        data = {
            'name': new_name,
        }
        response = self.__class__._pandadoc.put('{folder_type}/folders/{folder_uuid}'.format(
            folder_type=self.__class__.get_folder_type(),
            folder_uuid=self.uuid,
        ), data=data)
        return response.status_code

    # def delete(self) -> int:
    #     response = self.__class__._pandadoc.delete('{folder_type}/folders/{folder_uuid}'.format(
    #         folder_type=self.__class__.get_folder_type(),
    #         folder_uuid=self.uuid,
    #     ))
    #     return response.status_code
