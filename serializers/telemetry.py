# one doc 
def DecodeTelemetry(doc) -> dict:
    return {
        "_id" : str(doc["_id"]) ,
        "time" : doc["time"] ,
        "device_id" : doc["device_id"] ,
        "data" : doc["data"]
    }

# all telemetries 
def DecodeTelemetries(docs) -> list:
    return [DecodeTelemetry(doc) for doc in docs]
