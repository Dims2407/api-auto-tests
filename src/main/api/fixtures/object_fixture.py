import logging
from typing import List, Any

import pytest

from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.create_user_response import CreateUserResponse


@pytest.fixture
def create_obj():
    objects: List[Any] = []
    yield objects
    clean_user(objects)


def clean_user(objects: List[Any]):
    api_manager = ApiManager(objects)
    for el in objects:
        if isinstance(el, CreateUserResponse):
            api_manager.admin_steps.delete_user(el.id)
        else:
            logging.warning(f"Error in delete user_id: {el.id}")

