from flask import Blueprint, jsonify
import time
import jwt

api_bp = Blueprint('login', __name__)


@api_bp.route('/v1/login', methods=['POST'])
def login():
    token = jwt.encode(
        {
            "test": "value",
            "iat": time.time(),
            "exp": time.time() + 10000,
        },
        "key",
    )
    return jsonify({"payload": {"accessToken": token}}), 200
