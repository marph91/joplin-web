"""joplin_web URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, re_path
from joplin_web.views import home, notes_folder, notes_tag, edit_note_and_tags, delete_note, create_folder, create_tag
from joplin_web.api import get_folders, get_tags

urlpatterns = [
    path('', home, name='home'),
    path('create/note/', home, name='create_note'),
    path('create/tag/', create_tag, name='create_tag'),
    path('create/folder/', create_folder, name='create_folder'),
    re_path('^notes/folder/(?P<folder_id>[0-9a-z]{32})', notes_folder, name='notes_folder'),
    re_path('^notes/tag/(?P<tag_id>[0-9a-z]{32})', notes_tag, name='notes_tag'),
    re_path('^notes/(?P<note_id>[0-9a-z]{32})', edit_note_and_tags, name='edit_note_and_tags'),
    re_path('^notes/delete/(?P<note_id>[0-9a-z]{32})', delete_note, name='delete_note'),
    path('folders', get_folders),
    path('tags', get_tags),
]


