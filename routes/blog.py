from fastapi import APIRouter 
from models.blog import BlogModel , UpdateBlogModel
from config.config import blogs_collection
from serializers.blog import DecodeBlogs, DecodeBlog
import datetime
from bson import ObjectId

blog_root = APIRouter()

# post request 
@blog_root.post("/new/blog")
def NewBlog(doc:BlogModel):
    doc = dict(doc)
    current_date = datetime.date.today()
    doc["date"] = str(current_date )
    
    res = blogs_collection.insert_one(doc)

    doc_id = str(res.inserted_id )

    return {
        "status" : "ok" ,
        "message" : "Blog posted successfully" , 
        "_id" : doc_id
    }
    

# getting blogs 
@blog_root.get("/all/blogs")
def AllBlogs():
    res =  blogs_collection.find() 
    decoded_data = DecodeBlogs(res)

    return {
        "status": "ok" , 
        "data" : decoded_data
    }


@blog_root.get("/blog/{_id}") 
def Getblog(_id:str) :
    res = blogs_collection.find_one({"_id" : ObjectId(_id) }) 
    decoded_blog = DecodeBlog(res)
    return {
        "status" : "ok" ,
        "data" : decoded_blog
    }


# update blog 
@blog_root.patch("/update/{_id}")
def UpdateBlog(_id: str , doc:UpdateBlogModel):
    req = dict(doc.model_dump(exclude_unset=True)) 
    blogs_collection.find_one_and_update(
       {"_id" : ObjectId(_id) } ,
       {"$set" : req}
    )

    return {
        "status" : "ok" ,
        "message" : "blog updated successfully"
    }


# delete blog 
@blog_root.delete("/delete/{_id}")
def  DeleteBlog(_id : str):
    blogs_collection.find_one_and_delete(
        {"_id" : ObjectId(_id)}
    )

    return {
        "status" : "ok" ,
        "message" : "Blog deleted succesfully"
    }