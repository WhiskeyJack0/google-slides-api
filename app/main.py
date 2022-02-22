
from fastapi import FastAPI
from pydantic import BaseModel
import app.gslides as SlidesAPI

app = FastAPI()

class Presentation(BaseModel):
    presentationID: str


@app.get("/")
def read_root():
    return {"Usage": "/slides"}

@app.post("/slides")
def get_slides(presentation: Presentation):
    print(presentation.presentationID)
    slides = SlidesAPI.get_slideid_dict(presentation.presentationID)
    return(slides)

# Unused Drive API calls for getting list of files.

# class File(BaseModel):
#     fileID: str

# @app.get("/files")
# def get_files():
#     files = SlidesAPI.get_drive_info()
#     return(files)

# @app.post("/files")
# def get_slides(file: File):
#     files = SlidesAPI.get_file_info(file.fileID)
#     return(files)