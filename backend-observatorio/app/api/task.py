from . import api
from flask import jsonify, url_for
from flask import current_app as app
from threading import Thread
from .errors import not_found
from ..decorators import background_tasks


@api.route('/status/<id>', methods=['GET'])
def get_task_status(id):
    """Query the status of an asynchronous task."""
    # obtain the task and validate it
    global background_tasks
    rv = background_tasks.get(id)
    if rv is None:
        return not_found(None)

    # if the task object is a Thread object that means that the task is still
    # running. In this case return the 202 status message again.
    if isinstance(rv, Thread):
        return jsonify({'Location': url_for('api.get_task_status', id=id)}), 202, {'Location': url_for('api.get_task_status', id=id)}

    # If the task object is not a Thread then it is assumed to be the response
    # of the finished task, so that is the response that is returned.
    # If the application is configured to auto-delete task status resources once
    # the task is done then the deletion happens now, if not the client is
    # expected to send a delete request.
    if app.config['AUTO_DELETE_BG_TASKS']:
        del background_tasks[id]
    return rv
