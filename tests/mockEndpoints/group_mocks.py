from flask import Blueprint, jsonify
from ..utils.success_wrapper import wrap
from ..utils import constants

api_bp = Blueprint('groups', __name__)


@api_bp.route('/v1/groups', methods=['GET'])
def get_group():
    return jsonify(wrap([
        {
            "id": constants.uuid,
        }
    ])), 200
