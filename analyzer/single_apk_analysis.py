"""Bho"""
from androguard.core.bytecodes import apk
import os
PATH = "/home/luca/dev/AdwareSamples/adware/com.AlolasJJ.jzcompass-5.1.4-154a86b1e4b5ece4be5bfa6ef4ed3047.apk"

def get_data(path):
    """Analyze and return data regarding the apk specified in the parameter path
        the output record is a list of tuples
        [(name,value), (name2,value2)...] """
    a = apk.APK(path)
    out_record = [("apk_name", os.path.basename(path))]
    out_record.append(("num_activities", len(a.get_activities())))
    out_record.append(("permissions", a.get_permissions()))

    return out_record

print get_data(PATH)
