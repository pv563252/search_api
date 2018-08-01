from api_controller import utils
import flask
import json


def get_similar_videos(videoId):
    """
    Return a list of similar videos, of available.
    :param videoId: Integer
    :return: Similar Video JSON Objects
    """
    if utils.validate_video_id(videoId):
        data = utils.get_similar_videos(videoId)
        response = {'data': data, 'videoId': videoId, 'count': len(data)}
        utils.write_locally(response)
        return flask.jsonify(response), 200, {'message': 'Similar Videos found'}
    return flask.jsonify('Not Found'), 404, {'x-error': 'video not found'}
