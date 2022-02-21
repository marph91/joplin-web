# coding: utf-8
"""
   joplin-web
"""
from django.conf import settings
from django.http.response import JsonResponse
from django.urls import reverse
from joppy.api import Api
from joplin_web.utils import nb_notes_by_tag, nb_notes_by_folder
import logging
from rich import console
console = console.Console()

logger = logging.getLogger("joplin_web.app")

joplin = Api(token=settings.JOPLIN_WEBCLIPPER_TOKEN)


def get_folders(request):
    """
    all the folders
    :param request
    :return: json
    """
    json_data = sorted(joplin.get_all_notebooks(), key=lambda k: k['title'])
    data = nb_notes_by_folder(json_data)
    logger.debug(data)
    return JsonResponse(data, safe=False)


def get_tags(request):
    json_data = sorted(joplin.get_all_tags(), key=lambda k: k['title'])
    data = nb_notes_by_tag(json_data)
    return JsonResponse(data, safe=False)
