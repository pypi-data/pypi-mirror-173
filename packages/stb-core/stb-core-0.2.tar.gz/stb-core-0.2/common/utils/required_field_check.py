
def required_field_check(data,fieldname_list):
    error = []
    for field_name in fieldname_list:
        if not data.get(f'{field_name}'):
            error.append(f'{field_name} is required')
    if error:
        return_dict = {"status":False,"error":error}
        return return_dict
    else:
        return_dict = {"status":True,"error":error}
        return return_dict
