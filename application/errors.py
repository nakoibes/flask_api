from flask import jsonify


def not_found(e):
    return jsonify({"error": str(e)}), 404


def bad_data(e):
    return jsonify({"error": str(e)}), 400


def server_failure(e):
    return jsonify({"error": str(e)}), 500
