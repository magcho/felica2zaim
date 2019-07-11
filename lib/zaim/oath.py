from rauth import OAuth1Service, OAuth1Session
from authInfo import consumerKey, consumerSecret ,accessToken, accessTokenSecret

def oath():
    zaimService = OAuth1Service(
        consumer_key=consumerKey,
        consumer_secret=consumerSecret,
        request_token_url='https://api.zaim.net/v2/auth/request',
        access_token_url='https://api.zaim.net/v2/auth/access',
        authorize_url='https://auth.zaim.net/users/auth',
        base_url='https://api.zaim.net/v2/home/'
    )

    zaimSession = OAuth1Session(
        consumer_key=consumerKey,
        consumer_secret=consumerSecret,
        access_token=accessToken,
        access_token_secret=accessTokenSecret,
        service=zaimService
    )

    return zaimSession
