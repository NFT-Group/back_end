import pickle
import firebase_admin
from firebase_admin import credentials, firestore, db
from pandas import DataFrame
from sklearn.ensemble import RandomForestRegressor

cred_push_key = {
  "type": "service_account",
  "project_id": "ml-prepped-database",
  "private_key_id": "b94db5e77d786b2608f10636b3baf757070974d6",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDDtf8ceauQXcM9\nvOFP4mUUbuOTYk5twoU/LhdbeE8Gs6F+SrB+YA7WmurJTp/GwQdY7ThV7YKYtkSx\nsaFmYDjUHeJGgnq4QJyvSyWVf9kW8ZSMhWmt0kOcgeSLAKbqI6UOyIUsN/5rSe5K\ngxVeDKQCLW7IIzVZEDI+xkVeAYmiXuHsx+qqQ2lO0ki5bGtxyAvnJQ6dBS7hhYWf\nx9jzOPYB1YBV6wi55uhjOaj7Z+WcVz2ME2ybjvmMwX2oE0FyRE7H+s1RvzAltYQN\nCS95aX4YxWr1Fe/bMmzAlKkT9T+ccDu57Ix1dUl41Am1uoa1DjhAUls6UFqC3iX2\npPaRnWcvAgMBAAECggEAFG77kEMJzRxlBpyiX59RE2WSgDBa5O3S0KpkyOmSQq5d\nlZyBuegYlIJ/Mf5yAyPjOv8lix8tq/kXyf+0TMaOGGN4XQlBe9xPH6Q2a9n51gHq\nExPY2UujQIN1U6gBRV/sW1NHSDseZqBE72WpRPUH6KxKrT2z07UzsccstehuMNQN\nZ2aAR+rp9JcmGfUbHQ08usQF8lyRuhAkhomHY9OR5k0GWLzBrxqJHqHA/+E4EDH4\nLwFdL8zOtZmATbZHXqX55Uj8zGLws+2I/ksG3l8yZHeuitniqvpmKvhYc2ER2KLx\nAZ8ejevcWTMRVGHkX9XUxVG8NUWTH09vJ6W3jbgabQKBgQDuq0CSCA31aEbSXguf\nFJL63oyqRX5FGIz1wbzWyAOUndhpc1TupOQxnt1RQwLqwqb4Oy0C19rhSSF6h4BI\nHpNrnX6z65rhFGp0APHdt7kGZ4NApx7iiNkM/SGSCGPdaxYylZ3Rb1hE3Omit6VU\nEbm3NkoZVhjjsGWtKtaaSWugzQKBgQDR7CyJnE8V5lD/OrCd5BZqIhBxbBD299+R\nDs8hnrktw+Gtvn9WwLql0AUIstSV7m7W7eJYvD1h3AUbO2o/H7+bmneIHARt8DrP\nQQLnholcX+aPAEKuokesEpjEoleqTI8epu5dwE2uuYgF7P7QqbhWWFaBkYqjQTFj\nVio9Zlf36wKBgAvok5I1wKyMBWydsKrBVgwaap5cVU6RSQdCIW/+Dt+teIzaalR1\n+cTYDmbtlwmrqLUeDsLjjlJLWdZJSIdQrz5hX18O1G2CnUUofuj3L843//6L2Cip\nd1sEjlZBAOqdW0Au4u7+RUM6WpX538/wCnovxUa6WweRV6FqT8bm/u3JAoGAFA4B\nD0B8mbYAJPIBb4Qb1BXfBkbxs/ZoSF5m0WptfH7LL6MUXUBaVH70DCmxf4Vg122w\ngxOwtYmkfz6E3vT0hDQUmU876RjbNXObiGzk8ItE5oJ63F4qhLjeGWL9Bwr7XU1L\nVm+JvFiDMzW5/ktIjg8wbH5wBTq0Mi5IKMd/PfMCgYEAqq6OAWU2CcNu2MJdPaON\nEraEdyO8UmTeRNcAsI/DVfJkOgDWs/mON33Cmtnmc4HHSf6YsjHBy+g8XCkWBPdb\n4RqguTSBbMdbpSjinnkocJF5UcMMjKWUfOBdymWMrQao14tAxtuSvqtSY1fvUCB+\n1Ohu36IjTNi8LW1kGi//zII=\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-u7cos@ml-prepped-database.iam.gserviceaccount.com",
  "client_id": "110669828910428993200",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-u7cos%40ml-prepped-database.iam.gserviceaccount.com"
}

transactions_app = None
ml_app = None

def find_price_predictor_from_tokenid():
    cred_push = firebase_admin.credentials.Certificate(cred_push_key)
    try:
        firebase_admin.delete_app(transactions_app)
    except:
        a = cred_push # dummy operation
    try:
        ml_app = firebase_admin.initialize_app(cred_push, { 'databaseURL':'https://ml-prepped-database-default-rtdb.europe-west1.firebasedatabase.app/' } )
    except:
        a = cred_push # dummy operation
    
    # process request
    collection_name = "boredape"
    tokenID = "3749"

    # find model
    filename = collection_name + "_model.pkl"
    print(filename)
    loaded_model = pickle.load(open(filename, 'rb'))

    # find input
    nft_string = collection_name+tokenID
    ref = db.reference(nft_string)
    data_for_input = ref.get()

    # format input 
    data_for_input_json = DataFrame([data_for_input])
    print(data_for_input_json)
    data_for_input_json = data_for_input_json.drop(['NameOfCollection', 'ethprice'], axis=1)
    data_for_input_json['timestamp'] = 0

    predicted_price = loaded_model.predict(data_for_input_json)

    firebase_admin.delete_app(ml_app) # there will DEFINITELY be a better way of doing this!!


    return predicted_price

print(find_price_predictor_from_tokenid())