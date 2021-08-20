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

    token = event["headers"]["Authorization"]
    print(token)
    jwt_secret = "2oSaOLx6Uii6sn5DfqlcaPWPYCJS"
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
                "body":  json.dumps(prepare_for_dumps({"cliente": cliente,
                          "token_payload": payload}))
                }

    print(response)
    return response


def prepare_for_dumps(d):
    for key in d:
        if type(d[key]) == dict or type(d[key]) == list:
            prepare_for_dumps(d)
        elif is_jsonable(d[key]):
            pass
        else:
            d[key] = str(d[key])
    return d


def is_jsonable(x):
    try:
        json.dumps(x)
        return True
    except (TypeError, OverflowError):
        return False