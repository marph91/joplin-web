# coding: utf-8
"""
   joplin-web
"""
from django.conf import settings
from django.http.response import JsonResponse
from django.urls import reverse
from joplin_api import JoplinApiSync
from joplin_web.utils import nb_notes_by_tag, nb_notes_by_folder
import logging
from rich import console
console = console.Console()

logger = logging.getLogger("joplin_web.app")

joplin = JoplinApiSync(token=settings.JOPLIN_WEBCLIPPER_TOKEN)


def get_folders(request):
    """
    all the folders
    :param request
    :return: json
    """
    res = joplin.get_folders()
    data = nb_notes_by_folder(res.json())
    logger.debug(data)
    return JsonResponse(data, safe=False)


def get_tags(request):
    res = joplin.get_tags()
    data = nb_notes_by_tag(res.json())
    data_tree = []
    for line in data:
        my_data = {'text': line['title'],
                   'href': reverse('notes_tag', args=[line['id']])}
        if 'children' in line:
            # due to bstreeview, need to adapt data
            # children = nodes
            # title = text
            my_data['nodes'] = line['children']
        data_tree.append(my_data)
    logger.debug(data_tree)
    return JsonResponse(data_tree, safe=False)
