from api_controller import utils
import json


def get_similar_videos(videoId):
    """
    Return a list of similar videos, of available.
    :param videoId: Integer
    :return: Similar Video JSON Objects
    """
    if utils.validate_video_id(videoId):
        return json.dumps({'data': utils.get_similar_videos(videoId)}), 200, {'message': 'video not found'}
    return 'Not Found', 404, {'x-error': 'video not found'}
