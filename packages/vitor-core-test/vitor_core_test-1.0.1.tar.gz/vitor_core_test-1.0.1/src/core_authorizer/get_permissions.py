import json
import jwt
"""Get Permission from JWT"""


def decode_token(event):
    """"Decode the token"""
    if 'headers' in event and 'authorization' in event['headers']:
        token = event['headers']['authorization']
        token1 = token.split(' ')[1]
        tok_dec = jwt.decode(token1, options={"verify_signature": False})
        return tok_dec
    else:
        return None


def get_permissions(event):
    """return the permissions"""
    token_decoded = decode_token(event)
    username = token_decoded['username']
    permissions = {username: {}}
    permissions[username]['/policy'] = ["GET", "PUT"]
    permissions[username]['/admin'] = ["GET"]
    return permissions
