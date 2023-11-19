from fastapi import HTTPException


def validate(obj, statuscode, errormsg):
    if obj is None:
        raise HTTPException(status_code=statuscode, detail=errormsg)

