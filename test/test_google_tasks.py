#!/usr/bin/env python3

import pytest
from src.google_tasks import GoogleTasks


def test_tasklist():
    google_tasks = GoogleTasks()
    google_tasks.get_task_list()
    task_list = [x['title'] for x in google_tasks.tasks_list]
    assert 'Task Testing' in task_list

def test_tasks():
    google_tasks = GoogleTasks()
    google_tasks.get_tasks(task_item='Task Testing')
    assert 'Task test' in google_tasks.tasks