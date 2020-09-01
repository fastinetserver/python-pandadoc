"""pandatemplate.py implements API Wrapper for Templates https://developers.pandadoc.com/reference#list-templates"""

__author__ = "Kostyantyn Ovechko"
__copyright__ = "Copyright 2020, Zxscript"
__license__ = "MIT"
__version__ = "0.0.1"
__email__ = "kos@zxscript.com"
__status__ = "Production"


from abc import ABC
from typing import List, Dict

from .panda_exceptions import ApiException


class TemplateIdRequiredException(Exception):
    pass


class PandaTemplateAbstract(ABC):
    def __init__(self, template_id: str = None):
        """
        :str template_id
        """
        if template_id is None:
            raise TemplateIdRequiredException()
        self.__id = template_id

    @property
    def id(self):
        return self.__id

    @classmethod
    def list(
            cls,
            q: str = None,
            tag: str = None,
            count: int = None,
            page: int = None,
            deleted: bool = None,
            id_: str = None,
            folder_uuid: str = None,
    ) -> List[Dict]:
        """
            :param q: str: Optional search query. Filter by template name.
            :param tag: str: Optional search tag. Filter by template tag.
            :param count: int: Optionally specify how many templates to return. Default is 50 templates, maximum is 100 templates.
            :param page: int: Optionally specify which page of the dataset to return.
            :param deleted: bool: Optionally returns only deleted templates
            :param id_: str: Optionally specify template ID
            :param folder_uuid: str: The UUID of the folder where the templates are stored.
            :return List[Dict]: List of templates
        """

        data = {}
        if q:
            data['q'] = q
        if tag:
            data['tag'] = tag
        if count:
            data['count'] = count
        if page:
            data['page'] = page
        if deleted is not None:
            data['deleted'] = deleted
        if id_:
            data['id'] = id_
        if folder_uuid:
            data['folder_uuid'] = folder_uuid

        response = cls._pandaworkspace.get('templates', data=data)
        if response.status_code != 200:
            raise ApiException(response.text)
        results = response.json().get('results')
        return results

    def details(self) -> Dict:
        response = self.__class__._pandaworkspace.get('templates/{template_id}/details'.format(template_id=self.id))
        return response.json()

    def delete(self) -> int:
        response = self.__class__._pandaworkspace.delete('templates/{template_id}'.format(template_id=self.id))
        return response.status_code
