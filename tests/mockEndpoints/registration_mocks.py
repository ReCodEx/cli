from flask import Blueprint, jsonify
from ..utils.success_wrapper import wrap

api_bp = Blueprint('registration', __name__)


@api_bp.route('/v1/users/invite', methods=['POST'])
def invite():
    return jsonify(wrap(True)), 200
