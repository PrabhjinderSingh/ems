from fastapi import APIRouter 
from models.project import ProjectModel , UpdateProjectModel
from config.config import projects_collection
from serializers.project import DecodeProjects, DecodeProject, DecodeProjectDashboard, DecodeProjectsDashboard
import datetime
from bson import ObjectId

project_root = APIRouter()

# post request 
@project_root.post("/project")
def NewProject(doc:ProjectModel):
    doc = dict(doc)
    # current_date = datetime.date.today()
    # doc["date"] = str(current_date )
    
    res = projects_collection.insert_one(doc)

    doc_id = str(res.inserted_id )

    return {
        "status" : "ok" ,
        "message" : "Project posted successfully" , 
        "_id" : doc_id
    }
    

# getting projects 
@project_root.get("/projects")
def AllProjects():
    res =  projects_collection.find() 
    decoded_data = DecodeProjects(res)

    return {
        "status": "ok" , 
        "data" : decoded_data
    }


@project_root.get("/project/{_id}") 
def GetProject(_id:str) :
    res = projects_collection.find_one({"_id" : ObjectId(_id) }) 
    decoded_project = DecodeProject(res)
    return {
        "status" : "ok" ,
        "data" : decoded_project
    }


# update project 
@project_root.patch("/project/{_id}")
def UpdateProject(_id: str , doc:UpdateProjectModel):
    req = dict(doc.model_dump(exclude_unset=True)) 
    projects_collection.find_one_and_update(
       {"_id" : ObjectId(_id) } ,
       {"$set" : req}
    )

    return {
        "status" : "ok" ,
        "message" : "project updated successfully"
    }


# delete project 
@project_root.delete("/project/{_id}")
def  DeleteProject(_id : str):
    projects_collection.find_one_and_delete(
        {"_id" : ObjectId(_id)}
    )

    return {
        "status" : "ok" ,
        "message" : "Project deleted succesfully"
    }

@project_root.get("/project/dashboard/{_id}")
def GetDashboardData(_id:int):
    
    res = projects_collection.aggregate([
    {
        '$lookup': {
            'from': 'panels', 
            'localField': 'project_id', 
            'foreignField': 'project_id', 
            'as': 'panel_details'
        }
    }, {
        '$lookup': {
            'from': 'meters', 
            'localField': 'panel_details.panel_id', 
            'foreignField': 'panel_id', 
            'as': 'meter_details'
        }
    }, {
        '$lookup': {
            'from': 'telemetries', 
            'localField': 'meter_details.meter_name', 
            'foreignField': 'device_id', 
            'pipeline': [
                {
                    '$match': {
                        '$expr': {
                            '$and': [
                                {
                                    '$gte': [
                                        '$time', '2020-01-08T00:00:00.000Z'
                                    ]
                                }, {
                                    '$lte': [
                                        '$time', '2025-09-08T23:59:59.000Z'
                                    ]
                                }
                            ]
                        }
                    }
                }
            ], 
            'as': 'telemetry_details'
        }
    }, {
        '$addFields': {
            'total_w_r': {
                '$sum': '$telemetry_details.data.W_R'
            }, 
            'total_w_t': {
                '$sum': '$telemetry_details.data.W_T'
            }, 
            'total_w_t123': {
                '$sum': '$telemetry_details.data.W_T123'
            }, 
            'meters_running': {
                '$cond': {
                    'if': {
                        '$gt': [
                            {
                                '$sum': '$telemetry_details.data.HZ'
                            }, 0
                        ]
                    }, 
                    'then': True, 
                    'else': False
                }
            }, 
            'all_meters_not_running': {
                '$in': [
                    0, '$telemetry_details.data.HZ'
                ]
            }, 
            'total_energy': {
                '$sum': '$telemetry_details.data.WH_EB_REC'
            }, 
            'max_demand': {
                '$max': '$telemetry_details.data.W_T'
            }, 
            'cost': 99999, 
            'last_run_date': {
                '$max': '$telemetry_details.time'
            }
        }
    }, {
        '$project': {
            'project_short_name': 1, 
            'project_long_name': 1, 
            'location': 1, 
            'total_energy': 1, 
            'project_status': {
                '$cond': {
                    'if': {
                        '$and': [
                            {
                                '$eq': [
                                    '$meters_running', True
                                ]
                            }, {
                                '$eq': [
                                    '$all_meters_not_running', False
                                ]
                            }
                        ]
                    }, 
                    'then': 'Running', 
                    'else': {
                        '$cond': {
                            'if': {
                                '$and': [
                                    {
                                        '$eq': [
                                            '$meters_running', True
                                        ]
                                    }, {
                                        '$eq': [
                                            '$all_meters_not_running', True
                                        ]
                                    }
                                ]
                            }, 
                            'then': 'Partial Failure', 
                            'else': 'Full Failure'
                        }
                    }
                }
            }, 
            'max_demand': 1, 
            'cost': 1, 
            'last_run_date': 1, 
            'meters_running': 1, 
            'all_meters_not_running': 1
        }
    }
]) 
    decoded_project_dashboard = DecodeProjectsDashboard(res)
    
    return {
        "status" : "ok" ,
        "data" : decoded_project_dashboard
    }