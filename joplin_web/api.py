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
    json_data = sorted(res.json(), key=lambda k: k['title'])
    data = nb_notes_by_folder(json_data)
    logger.debug(data)
    return JsonResponse(data, safe=False)


def get_tags(request):
    res = joplin.get_tags()
    json_data = sorted(res.json(), key=lambda k: k['title'])
    data = nb_notes_by_tag(json_data)
    return JsonResponse(data, safe=False)
