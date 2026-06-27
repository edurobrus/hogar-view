from flask import request, jsonify


def is_fetch() -> bool:
    return request.headers.get('X-Requested-With') == 'fetch'


def json_ok(redirect_url=None):
    return jsonify({'ok': True, 'redirect': redirect_url})
