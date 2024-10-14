from pydantic import BaseModel 

class TelemetryModel(BaseModel):
    time : str 
    device_id : str 
    data : dict 

class UpdateTelemetryModel(BaseModel):
    time : str = None
    device_id : str = None
    data : dict = None
