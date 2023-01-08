from __future__ import annotations

from functools import wraps
from typing import TYPE_CHECKING

from flask import Blueprint

from Man10InstanceManager.methods.instance.sub_methods.Create import InstanceCreateMethod
from Man10InstanceManager.methods.instance.sub_methods.List import InstanceListMethod
from Man10InstanceManager.methods.instance.sub_methods.Stop import InstanceStopMethod

if TYPE_CHECKING:
    from Man10InstanceManager import Man10InstanceManager


class InstanceMethod:

    def __init__(self, main: Man10InstanceManager):
        self.main = main
        self.blueprint = Blueprint('instance', __name__, url_prefix="/")
        InstanceCreateMethod(self)
        InstanceStopMethod(self)
        InstanceListMethod(self)

        self.main.flask.register_blueprint(self.blueprint)
