from androguard.core.bytecodes import apk
from androguard.core.bytecodes import dvm
import os
import copy

data_dictionary = {
        "apk_name" : None,
        "num_activities" : None,
        "permissions" : [],
        "libraries" : []}

def get_data(path):
    """Analyze and return data regarding the apk specified in the parameter path.
        the output record is a data_dictionary"""
    a = apk.APK(path)
    d = dvm.DalvikVMFormat(a.get_dex())
    out_record = copy.deepcopy(data_dictionary)
    out_record["apk_name"] = os.path.basename(path)
    out_record["num_activities"] = len(a.get_activities())
    out_record["permissions"] = list(set(a.get_permissions()))
    out_record["libraries"] = list(set(a.get_libraries()))
    return out_record
