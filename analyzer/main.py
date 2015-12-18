from pymongo import MongoClient
from single_apk_analysis import get_data
from single_apk_analysis import data_dictionary
import glob
import time
import sys
import os

TEST_ADWARE = "cn.hosy.simkawang-1.2.1-6b2d0948a462431d93a2035a82af6cb5.apk"
PATH_ADWARE = "/home/luca/dev/AdwareSamples/adware"
PATH_BENIGN = "/home/luca/dev/AdwareSamples/benign0"

client = MongoClient()
db = client.analysis_database
adware_db = db.adware_database
benign_db = db.benign_database
results_db = db.results_database

def analyze_samples(path, mongo_db_collection):
    listfile = glob.glob(path + "/*.apk")
    num_files = len(listfile)
    start_time = time.time()
    added = 0;
    found = 0;
    for i in range (0, num_files):
        """Check presence"""
        check_flag = mongo_db_collection.find_one({"apk_name" : os.path.basename(listfile[i])})
        if check_flag is None:
            """Start Analysis"""
            tmp_record = get_data(listfile[i])
            mongo_db_collection.insert_one(tmp_record)
            added += 1
        else:
            found += 1 
        """output console and execution time"""
        curr_time = time.time()
        exec_time_string = str(int((curr_time - start_time) /60)) + " min " + str(int(((curr_time - start_time)))%60) + " sec"
        sys.stdout.write("\rAnalized " + str(i+1) + "/" + str(num_files) + " exec time " + exec_time_string)
        sys.stdout.flush()
    """Output end execution"""
    print ""
    print "Added " + str(added) + " records to the db: " + mongo_db_collection.name + ". " + str(found) + " were already in the db" 
    return

def clear_db(coll):
    print "Deleted " + str(coll.delete_many({}).deleted_count) + " records"
    return

def status_db():
    print adware_db.name + ": " + str(adware_db.count()) + " records"
    print benign_db.name + ": " + str(benign_db.count()) + " records"
    print results_db.name + ": " + str(results_db.count()) + " records"
    return

def elaborate_all_data(db_target):
    for key in data_dictionary.iterkeys():
        elaborate(db_target, key)
    return

def elaborate(collection_target, field):
    """TODO check presence of db + field"""
    new_record = {"name": collection_target.name + "-" + field}
    if isinstance((collection_target.find_one({})[field]),list):
            print("Creating bargram for " + new_record["name"])
            new_record.update(_elab_sets(field,collection_target.find({})))
    before = results_db.find_one_and_replace({"name": new_record["name"]}, new_record)
    if before is None:
        results_db.insert_one(new_record)
        print "The result has been added to the db"
    else:
        print "The result has been updated"
    return

def _elab_sets(tag_field, iterator):
    out_dict = {}
    for record in iterator:
        for value in record[tag_field]:
            new_key = value.replace(".","-")
            if out_dict.has_key(new_key):
                out_dict[new_key] += 1
            else:
                out_dict.update({new_key : 1})
    return out_dict

def _elab_num():
    
    return