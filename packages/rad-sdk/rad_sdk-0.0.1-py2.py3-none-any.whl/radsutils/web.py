import json
import traceback

from fastapi.responses import Response
from mongoengine import Document
from pydantic import BaseModel

from radsutils.logger import logger


def mongo_to_dict(content) -> dict:
    """
    The mongo_to_dict function takes a MongoDB object and returns a dictionary.
    It also removes the _id field from the returned dictionary, as it is not serializable.

    :param content: Determine the type of object to be transformed
    :return: The dictionary representation of the content
    :doc-author: Trelent
    """
    if content is None:
        return {}
    if issubclass(type(content), Document):
        response_object = json.loads(content.to_json())
        response_object["id"] = str(content.id)
        response_object.pop("_id")
    elif issubclass(type(content), BaseModel):
        response_object = content.dict()
    else:
        logger.debug(f"format type {type(content)}")
        response_object = content

    return response_object


def json_response(content=None, dict_content: dict = None, http_status=200, pop_fields=None):
    """
    The json_response function is a helper function that takes in an object and returns a Response
    object with the appropriate content-type header.  It also populates the response body with json encoded
    data, which can be either a list or dictionary.  The function will also accept QuerySets as input, but it will
    convert them to lists before encoding.

    :param content:
    :param dict_content:dict=None: Pass in a dictionary that will be encoded into json
    :return: A json encoded response
    :doc-author: Trelent
    """
    if pop_fields is None:
        pop_fields = {}
    try:
        response = doc_cleanup(content if content is not None else dict_content, pop_fields)
        response = json.dumps(response)
        return Response(content=response, status_code=http_status, media_type="application/json")
    except Exception as e:
        exception_log(e)


def deprecated(args):
    """

    :param args:
    """
    print("this function is deprecated, use the sensitive attribute")


def doc_cleanup(doc, pop_fields):
    """

    :param doc:
    :param pop_fields:
    :return:
    """
    response = mongo_to_dict(doc)
    for field in pop_fields:
        try:
            response.pop(field)
        except Exception as e:
            logger.error(f"field {field} not in dictionary")
    return response

def exception_log(e):
    logger.error(e)
    traceback_log = traceback.format_exception(type(e), e, e.__traceback__)
    logger.error(traceback_log)