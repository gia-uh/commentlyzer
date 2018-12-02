import functools
from flask import copy_current_request_context, make_response, jsonify
from flask import url_for, request
from threading import Thread
from .api.errors import internal_server_error, bad_gateway_error
import uuid
import logging
from .model import Manager
from Crawler import UnreachebleURL, ProxyConfigError

logger = logging.getLogger('backgroundlogger')


background_tasks = {}

def background(f):
    """Decorator that runs the wrapped function as a background task. It is
    assumed that this function creates a new resource, and takes a long time
    to do so. The response has status code 202 Accepted and includes a Location
    header with the URL of a task resource. Sending a GET request to the task
    will continue to return 202 for as long as the task is running. When the task
    has finished, a status code 303 See Other will be returned, along with a
    Location header that points to the newly created resource. The client then
    needs to send a DELETE request to the task resource to remove it from the
    system."""
    @functools.wraps(f)
    def wrapped(*args, **kwargs):
        # The background task needs to be decorated with Flask's
        # copy_current_request_context to have access to context globals.
        @copy_current_request_context
        def task():
            global background_tasks
            try:
                # invoke the wrapped function and record the returned
                # response in the background_tasks dictionary
                background_tasks[id] = make_response(f(*args, **kwargs))
            except ProxyConfigError as e:
                logger.error(str(e))
                background_tasks[id] = make_response(
                    bad_gateway_error("Server Proxy error."))
            except UnreachebleURL as e:
                logger.error(str(e))
                background_tasks[id] = make_response(
                    bad_gateway_error("URL unreacheble."))
            except Exception as e:
                # the wrapped function raised an exception, return a 500
                # response
                logger.error(str(e))
                background_tasks[id] = make_response(internal_server_error(e.args[0]))

        # store the background task under a randomly generated identifier
        # and start it
        global background_tasks
        id = uuid.uuid4().hex
        background_tasks[id] = Thread(target=task)
        background_tasks[id].start()

        # return a 202 Accepted response with the location of the task status
        # resource
        logger.debug(str({'Location': url_for('api.get_task_status', id=id)}))
        return jsonify({'Location': url_for('api.get_task_status', id=id), 'id': id }), 202, {'Location': url_for('api.get_task_status', id=id)}
    return wrapped


def background_optional(f):
    """Decorator that runs the wrapped function as a background task. It is
    assumed that this function creates a new resource, and takes a long time
    to do so. The response has status code 202 Accepted and includes a Location
    header with the URL of a task resource. Sending a GET request to the task
    will continue to return 202 for as long as the task is running. When the task
    has finished, a status code 303 See Other will be returned, along with a
    Location header that points to the newly created resource. The client then
    needs to send a DELETE request to the task resource to remove it from the
    system."""
    @functools.wraps(f)
    def wrapped(*args, **kwargs):
        # The background task needs to be decorated with Flask's
        # copy_current_request_context to have access to context globals.
        @copy_current_request_context
        def task():
            global background_tasks
            try:
                # invoke the wrapped function and record the returned
                # response in the background_tasks dictionary
                background_tasks[id] = make_response(f(*args, **kwargs))
            except ProxyConfigError as e:
                logger.error(str(e))
                background_tasks[id] = make_response(
                    bad_gateway_error("Server Proxy error."))
            except UnreachebleURL as e:
                logger.error(str(e))
                background_tasks[id] = make_response(
                    bad_gateway_error("URL unreacheble."))
            except Exception as e:
                # the wrapped function raised an exception, return a 500
                # response
                logger.error(str(e))
                background_tasks[id] = make_response(internal_server_error(e.args[0]))

        data = request.json
        print(data)
        url = data['url']

        id = Manager.search_url(url)

        if id is not None:
            # return jsonify({'id': str(id)})
            return f(*args, **kwargs)
        # store the background task under a randomly generated identifier
        # and start it
        global background_tasks
        id = uuid.uuid4().hex
        background_tasks[id] = Thread(target=task)
        background_tasks[id].start()

        # return a 202 Accepted response with the location of the task status
        # resource
        logger.debug(str({'Location': url_for('api.get_task_status', id=id)}))
        return jsonify({'Location': url_for('api.get_task_status', id=id), 'id': id}), 202, {'Location': url_for('api.get_task_status', id=id)}
    return wrapped
