def _(dataBaseModelObject: object,name: str,value: any)->None:
    if(value is None):
        return
    if(value.strip() == ""):
       return setattr(dataBaseModelObject,name,None)
    return setattr(dataBaseModelObject, name, value)
    