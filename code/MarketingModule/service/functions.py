import jwt


def get_campaign_clients(**kargs):
    pass


def decode_token(token):
    return jwt.decode(token[1], 'secrets', algorithms=['HS256'])

