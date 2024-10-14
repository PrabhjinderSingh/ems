# one doc 
def DecodeProject(doc) -> dict:
    return {
        # "_id" : str(doc["_id"]) ,
        # "time" : doc["time"] ,
        # "device_id" : doc["device_id"] ,
        # "data" : doc["data"]

        "project_id" : str(doc["project_id"]),
        "project_short_name" : str(doc["project_short_name"]),
        "project_long_name" : str(doc["project_long_name"]),
        "location": str(doc["location"]),
        "project_protocol_type": str(doc["project_protocol_type"]),
        "capacity":int(doc["capacity"]),
        # mobile:str
        # account:str
        "account_id":int(doc["account_id"]),
        "status": str(doc["status"]),
        "active":str(doc["active"])


    }

# all projects 
def DecodeProjects(docs) -> list:
    return [DecodeProject(doc) for doc in docs]


def DecodeProjectDashboard(doc) -> dict:
    return {
        # "_id" : str(doc["_id"]) ,
        # "time" : doc["time"] ,
        # "device_id" : doc["device_id"] ,
        # "data" : doc["data"]

        # "project_id" : str(doc["project_id"]),
        "project_short_name" : str(doc["project_short_name"]),
        "project_long_name" : str(doc["project_long_name"]),
        "location": str(doc["location"]),
        "total_energy" : float(doc["total_energy"]),
        "project_status" : str(doc["project_status"]),
        "max_demand":  float(doc["max_demand"]),
        "cost": float(doc["cost"]),
        "last_run_date" : str(doc["last_run_date"]),
        "meters_running" : bool(doc["meters_running"]), 
        "all_meters_not_running" : bool(doc["all_meters_not_running"]),
        # "project_protocol_type": str(doc["project_protocol_type"]),
        # "capacity":int(doc["capacity"]),
        # mobile:str
        # account:str
        # "account_id":int(doc["account_id"]),
        # "status": str(doc["status"]),
        # "active":str(doc["active"])
    }

# all projects' on dashboard
def DecodeProjectsDashboard(docs) -> list:
    return [DecodeProjectDashboard(doc) for doc in docs]
