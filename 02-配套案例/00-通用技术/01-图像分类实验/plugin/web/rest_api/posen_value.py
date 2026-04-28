# -*- encoding: utf-8 -*-
from flask import Blueprint
from flask_api import status
from tools.config import config as cfg
import json

fruits_status_bp = Blueprint('fruits_start', __name__)

_fruits_start: dict
def setStatus(fruits_start):
    global _fruits_start
    _fruits_start = fruits_start

@fruits_status_bp.route("/pluginStatus", methods=['GET', 'POST'])
def getCarPluginStatus():
    print("__fruits_start:", _fruits_start)
    return_msg = {
        "fruit_class": _fruits_start[cfg.FRUIT_LIAB][0],
        "fruit_m": _fruits_start[cfg.FRUIT_LIAB][1],
        "fruit_g": _fruits_start[cfg.PRESSURE_SENSOR_DATA]
    }
    print("return_msg:", return_msg)
    return json.dumps(return_msg), status.HTTP_200_OK
