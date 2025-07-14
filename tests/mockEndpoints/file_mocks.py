from flask import Blueprint, jsonify
from ..utils.success_wrapper import wrap
from ..utils import constants

api_bp = Blueprint('files', __name__)


@api_bp.route('/v1/uploaded-files/partial', methods=['POST'])
def start_partial():
    return jsonify(wrap({"id": constants.uuid})), 200


@api_bp.route('/v1/uploaded-files/partial/<id>', methods=['PUT'])
def append_partial(id):
    return jsonify(wrap({"id": constants.uuid})), 200


@api_bp.route('/v1/uploaded-files/partial/<id>', methods=['POST'])
def complete_partial(id):
    return jsonify(wrap({"id": constants.uuid})), 200


@api_bp.route('/v1/uploaded-files/<id>/digest', methods=['GET'])
def digest(id):
    return jsonify(wrap({"digest": constants.uploadTestFileSHA1})), 200
