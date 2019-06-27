import json 

with open('/users/seemuali/runlog_resources/output.json') as file:
    output_dict = json.load(file)
    file.close()

    runinfo_dict = {}
    ws_dict = {}
    sample_dict = {}
 
    for key, val in output_dict["Header"].items():
        runinfo_dict[key] = val

    for key, val in output_dict["Reads"].items():
        runinfo_dict[key]= val

    
    for key, val in output_dict["Data"].items():
        ws_dict = val
        for key, val in (ws_dict["samples"].items()):
            sample_dict[key] = val
            #sample_dict = val 
            sample_dict["sample_id"]= key
            #upload sample_dict to database 
            
print(runinfo_dict)
#print(sample_dict)
#harcode the sample dict keys ??  