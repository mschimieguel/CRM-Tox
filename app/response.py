from flask import  jsonify


def success(data:dict = None):
    response = {
        'success': True,
        'message': 'Operation successful',
        'data': data
     }
    return jsonify(response), 200


def bad_request(mensagem: str):
    response = {
        'success': False,
        'message': "Bad request: " + mensagem
    }
    return 400,response


def unauthorized(mensagem : str):
    response = {
        'success': False,
        'message': "Unauthorized: " +  mensagem
    }
    return jsonify(response), 401

def not_found(mensagem : str):
    response = {
        'success': False,
        'message': 'Resource not found: ' + mensagem
    }
    return jsonify(response), 404


def internal_server_error(mensagem: str):
    response = {
        'success': False,
        'message': 'Internal server error: '+ mensagem
    }
    return jsonify(response), 500