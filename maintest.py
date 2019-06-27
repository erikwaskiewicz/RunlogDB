



# Import scripts
from scripts import add_to_db, parse_fqc, parse_hsmetrics, parse_fqc 
import sys

# Load run folder
results_runfolder = sys.argv[1]
print (results_runfolder)

#---------------------------------------------

# PARSE HSMETRICS 

# create empty dictionary

# parse (parameters set in function)





if  '_HsMetrics.txt' in results_runfolder: #TSO TSC
	hsdict = parse_hsmetrics.HSmetrics(results_runfolder)
	add_to_db.SampleMetrics_add(hsdict)
	print(hsdict)
if  'hs_metrics.txt' in results_runfolder:    #truesightmyeloid
	hsdict = parse_hsmetrics.HSmetrics(results_runfolder)
	add_to_db.SampleMetrics_add(hsdict)
	print(hsdict)
elif  '.HsMetrics.txt' in results_runfolder: #CRUK 
	hsdict = parse_hsmetrics.HSmetrics_CRUK(results_runfolder)
	add_to_db.SampleMetrics_add(hsdict)
	print(hsdict)
elif 'fastqc.txt' in results_runfolder: 
	fqcdict = parse_fqc.Fastqc(results_runfolder)
	add_to_db.Fastqc_add(fqcdict)
	print(fqcdict)
elif 'summary.txt' in results_runfolder: #myeloid and CRUK 
	fqcdict = parse_fqc.Fastqc_CRUK(results_runfolder)
	add_to_db.Fastqc_add(fqcdict)
	print(fqcdict)
else:
	quit()


# parse (parameters set in function)


#---------------------------------------------

# ADD TO DATABASE



















