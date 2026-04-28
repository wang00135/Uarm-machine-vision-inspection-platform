# -*- encoding: utf-8 -*-
from flask import Blueprint
from flask_api import status
from tools.config import config
import json

posen_status_bp = Blueprint('posen_start', __name__)

_posen_start: dict
def setStatus(posen_start):
    global _posen_start
    _posen_start = posen_start

@posen_status_bp.route("/pluginStatus", methods=['GET', 'POST'])
def getCarPluginStatus():
    return_msg = {
        "temp_value": _posen_start[config.TEMP_VALUE],
        "face_mask_start": _posen_start[config.FACE_MASK_START]
    }
    print("full_dict[config.POSEN_STATIC]:", return_msg)
    return json.dumps(return_msg), status.HTTP_200_OK
