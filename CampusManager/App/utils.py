from itsdangerous import URLSafeTimedSerializer


def create_serializer(secret_key):
    return URLSafeTimedSerializer(secret_key)
