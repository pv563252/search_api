import pandas as pd
import re
import os
import json


def validate_video_id(video_id):
    """
    Validate if the Video ID is available in the data
    :param video_id: Integer Video ID
    :return: True if present, False otherwise
    """
    videos = pd.read_csv(os.getcwd().split('/api_controller')[0] + '/data/similar-clips.csv')
    if video_id in list(videos['clip_id']):
        return True
    return False


def get_similar_videos(video_id):
    """
    Get Similar Videos for the Video ID
    :param video_id: Integer Video ID
    :return: List of json objects.
    """
    videos = pd.read_csv(os.getcwd().split('/api_controller')[0] + '/data/similar-clips.csv')
    similar_videos = list(videos[videos['clip_id'] == video_id]['similar_clips'])[0]
    return build_schema(extract_similar_videos(similar_videos))


def extract_similar_videos(similar_videos):
    """
    Extract Similar Videos from the string cosine similarity
    :param similar_videos: Integer List of similar Videos
    :return: Integer List of similar Videos
    """
    similar_videos = re.findall(r'\d+', similar_videos)
    similar_videos = [int(x) for x in similar_videos]
    similar_videos.reverse()
    return similar_videos


def build_schema(similar_videos):
    """
    Extract the list of similar videos
    :param similarity: Pandas DataFrame Object
    :return: JSON Objects for Similar Videos
    """
    clips = pd.read_csv(os.getcwd().split('/api_controller')[0] + '/data/similar-staff-picks-challenge-clips_cleaned.csv')
    clip_data = clips[clips['index_id'].isin(similar_videos)].fillna('NA')
    return json_builder(clip_data)


def json_builder(clip_data):
    """
    Build JSON Object
    :param clip_data: Pandas DataFrame Object
    :return: JSON object
    """
    clip_data = clip_data[["id", "title", "caption", "thumbnail", "category_names"]]
    return json_processing(clip_data.to_dict(orient='rows'))


def json_processing(clip_data):
    """
    Clean JSON Object
    :param clip_data: List of JSON records
    :return: json object
    """
    results = []
    for each in clip_data:
        try:
            each['categories'] = each['category_names'].split(',')
        except:
            each['categories'] = []
        each['image'] = each['thumbnail']
        del each['category_names']
        del each['thumbnail']
        results.append(each)
    return results


def write_locally(result):
    """
    Write Json result locally
    :param result: Response Json Object
    :return: True if executes correctly, False otherwise
    """
    try:
        path = os.getcwd().split('/utils')[0] + '/results/' + str(result['videoId']) + '.json'
        with open(path, 'w') as file:
            json.dump(result, file)
        return True
    except Exception as e:
        print(e)
        return False
