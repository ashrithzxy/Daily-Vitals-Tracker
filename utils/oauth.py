import os, time, httpx
import jwt

class Oauth:
    def __init__(self):
        self.secretKey = os.environ.get("service_account_private_key")
        self.serviceAccountEmail = os.environ.get("service_account_email")
    
    async def setAccessToken(self):
        jwt_header = {"alg": "RS256", "typ": "JWT"}

        iat = time.time()
        exp = iat + 3600

        payload = {
        "iss": self.serviceAccountEmail,
        "scope": "https://www.googleapis.com/auth/spreadsheets \
                    https://www.googleapis.com/auth/spreadsheets.readonly \
                    https://www.googleapis.com/auth/spreadsheets \
                    https://www.googleapis.com/auth/drive.readonly \
                    https://www.googleapis.com/auth/drive.file \
                    https://www.googleapis.com/auth/drive",
        "aud": "https://oauth2.googleapis.com/token",
        "exp": exp,
        "iat": iat
        }

        signed_jwt = jwt.encode(payload, self.secretKey, headers=jwt_header, algorithm='RS256')

        params = {
                    "grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
                    "assertion": signed_jwt
                }
        
        async with httpx.AsyncClient() as client:
            responseOauth = await client.post("https://www.googleapis.com/oauth2/v4/token", data=params)

        # print(f'ACCESS TOKEN IS: {responseOauth.content}')

        keyDict = responseOauth.json()
        oauth_token = keyDict.get("access_token")
        os.environ['service_account_oauth_token'] = oauth_token
        print(f"Access token set successfully")