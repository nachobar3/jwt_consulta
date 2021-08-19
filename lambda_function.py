import jwt
import pymongo
import json
from jwt import InvalidSignatureError

TEST = False


def lambda_handler(event, context):
    try:
        if TEST:
            client = pymongo.MongoClient("mongodb+srv://ibarbero:muvinai@cluster0.sf15y.mongodb.net/checkout")
            database = client.checkout
        else:
            client = pymongo.MongoClient("mongodb+srv://ibarbero:muvinai@cluster0.sf15y.mongodb.net/sportclub_prod")
            database = client.sportclub_prod

        print("Conexión establecida a Mongo DB.")
    except:
        print("No fue posible conectarse a MongoDB.")
        return {'statusCode': 500,
                'body': json.dumps('No fue posible conectar a MongoDB.')}

    print(event)
    print(event.headers)
    print(event["headers"]["Authorization"])
    body = json.loads(event['body'])
    token = body["token"]
    print(token)
    jwt_secret = "2oSaOLx6Uii6sn5DfqlcaPWPYCJS"

    try:
        payload = jwt.decode(token, jwt_secret, algorithms=["HS256"])
    except InvalidSignatureError:
        return {"status": 401,
                "message": "Invalid signature."}

    print(payload)
    cliente = database.clientes.find_one({"token_authorized": token})
    del cliente["token_authorized"]
    del cliente["token_unauthorized"]

    response = {"statusCode": 200,
                "body":  json.dumps({"cliente": cliente,
                          "token_payload": payload}, indent=4, sort_keys=True, default=str)
                }

    print(response)
    return response
