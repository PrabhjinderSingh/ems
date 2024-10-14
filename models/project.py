from pydantic import BaseModel 

class ProjectModel(BaseModel):
    project_id : int 
    project_short_name : str 
    project_long_name : str 
    location: str
    project_protocol_type: str
    capacity:int
    # mobile:str
    # account:str
    account_id:int
    status: str
    active:str
    

class UpdateProjectModel(BaseModel):
    # project_id : int 
    project_short_name : str = None
    project_long_name : str  = None
    location: str = None
    project_protocol_type: str = None
    capacity:int = None
    # mobile:str = None
    # account:str = None
    account_id:int = None
    status: str = None
    active:str = None

