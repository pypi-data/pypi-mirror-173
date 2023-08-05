import datetime
import json

import boto3
import jwt

from radsdata.user import MongoUser
from radsreq.jwtbearer import JWT_SECRET, JWT_ALGORITHM
from radsreq.jwtbearer import encode_jwt
from radsutils.logger import logger


def email_token(receiver):
    """
    The email_token function takes a receiver email address as an argument and returns a token.
    The token is created by encoding the receiver email address in a JWT payload, which expires after 48 hours.

    :param receiver: Send the email to the user
    :return: A token that is a jwt
    :doc-author: Trelent
    """
    logger.info("email token called with %s" % (receiver,))
    payload = {
        "email": receiver,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=2)
    }
    logger.info("token creation %s" % (payload,))
    token = encode_jwt(payload)
    logger.info("token created %s" % (token,))
    return token


def send_registration_confirmation(user, **kwargs):
    hostname = kwargs.get("origin", "http://localhost:3000")
    token = email_token(user.email)
    template_data = json.dumps({"first_name": user.first_name, "last_name": user.last_name, "hostname": hostname, "token": token})

    ses = boto3.client("ses", region_name="ap-southeast-1", aws_access_key_id="AKIA5CLBR5JUXW7XTYXC",
                       aws_secret_access_key="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")
    ses.send_templated_email(
        Source="HiAcuity Support <support@reverseads.io>",
        Template="Registration",
        ConfigurationSetName="reverseads",
        Destination={"ToAddresses": [user.email]},
        SourceArn='arn:aws:ses:ap-southeast-1:898389633641:identity/reverseads.io',
        TemplateData=template_data
    )


async def verify_token(token: str):
    """
    The verify_token function takes a token as an argument and returns the user object associated with that token.
    The function uses the jwt library to decode the token, then loads it into a json object. The json object is then
    used to query MongoDB for the user's document, which is returned.

    :param token:str: Pass the token that is being verified
    :return: A dictionary of the user's information
    :doc-author: Trelent
    """
    payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    user = json.loads(MongoUser.objects(email=payload.get("email")).to_json())
    selected_user = user[0]
    return selected_user
