from fastapi import APIRouter 
from models.telemetry import TelemetryModel , UpdateTelemetryModel
from config.config import telemetries_collection
from serializers.telemetry import DecodeTelemetries, DecodeTelemetry
import datetime
from bson import ObjectId

telemetry_root = APIRouter()

# post request 
@telemetry_root.post("/telemetry")
def NewTelemetry(doc:TelemetryModel):
    doc = dict(doc)
    # current_date = datetime.date.today()
    # doc["date"] = str(current_date )
    
    res = telemetries_collection.insert_one(doc)

    doc_id = str(res.inserted_id )

    return {
        "status" : "ok" ,
        "message" : "Telemetry posted successfully" , 
        "_id" : doc_id
    }
    

# getting telemetries 
@telemetry_root.get("/telemetries")
def AllTelemetries():
    res =  telemetries_collection.find() 
    decoded_data = DecodeTelemetries(res)

    return {
        "status": "ok" , 
        "data" : decoded_data
    }


@telemetry_root.get("/telemetry/{_id}") 
def GetTelemetry(_id:str) :
    res = telemetries_collection.find_one({"_id" : ObjectId(_id) }) 
    decoded_telemetry = DecodeTelemetry(res)
    return {
        "status" : "ok" ,
        "data" : decoded_telemetry
    }


# update telemetry 
@telemetry_root.patch("/telemetry/{_id}")
def UpdateTelemetry(_id: str , doc:UpdateTelemetryModel):
    req = dict(doc.model_dump(exclude_unset=True)) 
    telemetries_collection.find_one_and_update(
       {"_id" : ObjectId(_id) } ,
       {"$set" : req}
    )

    return {
        "status" : "ok" ,
        "message" : "telemetry updated successfully"
    }


# delete telemetry 
@telemetry_root.delete("/telemetry/{_id}")
def  DeleteTelemetry(_id : str):
    telemetries_collection.find_one_and_delete(
        {"_id" : ObjectId(_id)}
    )

    return {
        "status" : "ok" ,
        "message" : "Telemetry deleted succesfully"
    }