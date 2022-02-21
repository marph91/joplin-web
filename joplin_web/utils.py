# coding: utf-8
"""
   joplin-web
"""
from django.conf import settings
from django.urls import reverse
from joppy.api import Api
import logging
from rich import console
console = console.Console()

logger = logging.getLogger("joplin_web.app")

joplin = Api(token=settings.JOPLIN_WEBCLIPPER_TOKEN)


def tags_to_string(my_tags):
    """
    tags list to string with all tags
    :param my_tags: list
    :return string
    """
    tags = ''
    for tag in my_tags:
        tags += tag
        if len(my_tags) > 1:
            tags += ','
    return tags


def tag_for_notes(data):
    """
    alter the original data to add the tag related to the note
    :param data: data list
    :return: json
    """
    payload = []
    for note in data:
        tag = joplin.get_all_tags(note_id=note['id'])
        new_note = note
        new_note['tag'] = tag if tag else ''
        payload.append(new_note)
    logger.debug(payload)
    return payload


def nb_notes_by_tag(tags):
    """
    get the number of notes in each tag
    :param tags: tags list
    :return:
    """
    data = []
    # get the number of notes of each tag, if any
    for tag in tags:
        nb_notes = 0
        res_tags_notes = joplin.get_all_notes(tag_id=tag['id'])
        if len(res_tags_notes):
            nb_notes = len(res_tags_notes)
        item = dict()
        item['nb_notes'] = nb_notes
        item['text'] = f"{tag['title']} ({nb_notes})"
        item['href'] = reverse('notes_tag', args=[tag['id']])
        data.append(item)
    logger.debug(data)
    return data


def nb_notes_by_folder(folders):
    """
    get the number of notes in each folder
    :param folders: folders list
    :return: json
    """
    data = []
    # get the number of notes of each folder, if any
    for folder in folders:
        nb_notes = 0
        res_folders_notes = joplin.get_all_notes(notebook_id=folder['id'])
        if len(res_folders_notes):
            nb_notes = len(res_folders_notes)
        # item = folder
        item = dict()
        item['nb_notes'] = nb_notes
        item['text'] = f"{folder['title']} ({nb_notes})"
        item['href'] = reverse('notes_folder', args=[folder['id']])
        if 'children' in folder:
            # due to bstreeview, need to adapt data
            # children = nodes
            # title = text
            children = nb_notes_by_folder(folder['children'])
            item['nodes'] = children
        data.append(item)
    logger.debug(data)
    return data

