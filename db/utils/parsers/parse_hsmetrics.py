
import csv 
import os 

print (os.environ["Sample_ID"])


def HSmetrics (file):

    with open (file) as file:
        hsfile = csv.reader(file, delimiter="\t") #reads the csv file seperated in tabs 

        hsdict = {}

        hsdict = {"UniqueID":"",
        "run_id":"",
        "SampleID":"", 
        "BAIT_SET":"", 
        "GENOME_SIZE":"", 
        "BAIT_TERRITORY":"", 
        "TARGET_TERRITORY":"", 
        "BAIT_DESIGN_EFFICIENCY":"", 
        "TOTAL_READS":"",
        "PF_READS":"", 
        "PF_UNIQUE_READS":"", 
        "PCT_PF_READS":"", 
        "PCT_PF_UQ_READS":"", 
        "PF_UQ_READS_ALIGNED":"", 
        "PCT_PF_UQ_READS_ALIGNED":"",
        "PF_BASES_ALIGNED":"",      
        "PF_UQ_BASES_ALIGNED":"",
        "ON_BAIT_BASES":"", 
        "NEAR_BAIT_BASES":"", 
        "OFF_BAIT_BASES":"", 
        "ON_TARGET_BASES":"", 
        "PCT_SELECTED_BASES":"", 
        "PCT_OFF_BAIT":"",
        "ON_BAIT_VS_SELECTED":"",
        "MEAN_BAIT_COVERAGE":"",
        "MEAN_TARGET_COVERAGE":"",
        "MEDIAN_TARGET_COVERAGE":"",
        "MAX_TARGET_COVERAGE":"",
        "PCT_USABLE_BASES_ON_BAIT":"",
        "PCT_USABLE_BASES_ON_TARGET":"",
        "FOLD_ENRICHMENT":"",
        "ZERO_CVG_TARGETS_PCT":"",
        "PCT_EXC_DUPE":"",
        "PCT_EXC_MAPQ":"",
        "PCT_EXC_BASEQ":"",
        "PCT_EXC_OVERLAP":"",
        "PCT_EXC_OFF_TARGET":"",
        "FOLD_80_BASE_PENALTY":"",
        "PCT_TARGET_BASES_1X":"",
        "PCT_TARGET_BASES_2X":"",
        "PCT_TARGET_BASES_10X":"",
        "PCT_TARGET_BASES_20X":"",
        "PCT_TARGET_BASES_30X":"",
        "PCT_TARGET_BASES_40X":"",
        "PCT_TARGET_BASES_50X":"",
        "PCT_TARGET_BASES_100X":"",
        "HS_LIBRARY_SIZE":"",
        "HS_PENALTY_10X":"",
        "HS_PENALTY_20X":"",
        "HS_PENALTY_30X":"",
        "HS_PENALTY_40X":"",
        "HS_PENALTY_50X":"",
        "HS_PENALTY_100X":"",
        "AT_DROPOUT":"",
        "GC_DROPOUT":"",
        "HET_SNP_SENSITIVITY":"",
        "HET_SNP_Q":""}

    def HSmetrics ():    
        for num, rowinfo in enumerate(hsfile, start=1): #enumerating rows
            #print ("row {}: {}".format(num, rowinfo))

            '''
            1. splitting row2 of HSfile to extract SampleID and RunID information from the 
            "INPUT=(...)" section. 

            2. extracting key metrics from HS file, all hsfile expected to have row 7 with 
            headers and row 8 displaying values

            '''

            if num in [2,6,7,8]:
                HSoutput = (num, rowinfo)
                if num == 2:
                    row2_split = rowinfo[0].split(" ")
                    for sampleinfo in row2_split:
                        if sampleinfo.startswith("INPUT="):
                            inputinfo = sampleinfo.split("=")
                            ID = inputinfo[1].split("_")
                            UniqueID = inputinfo[1].split(".bam")
                            UniqueID = UniqueID[0]
                            RunID = '_'.join(ID[:4])
                            SampleID = ID[-1].strip('.bam') 
                            hsdict["UniqueID"]=UniqueID
                            hsdict["run_id"]=RunID 
                            hsdict["SampleID"]=SampleID

                if num == 7:
                    Keys = rowinfo
                if num == 8:
                    Values = rowinfo
                    length = len(Keys) #to do: need to assert that the length of keys matches length of values

                    for i in range(length):
                        hsdict[Keys[i]] = Values[i] #matches the row 7 keys with corresponding row 8 values 
                        if Values[i] == "?":
                            blank = Values[i].replace("?", "")
                            hsdict[Keys[i]] = blank
                        
                
                    return (hsdict)




def HSmetrics_CRUK (file):

    with open (file) as file:
        hsfile = csv.reader(file, delimiter="\t") #reads the csv file seperated in tabs 

        hsdict = {}

        hsdict = {"UniqueID":"",
        "run_id":"",
        "SampleID":"", 
        "BAIT_SET":"", 
        "GENOME_SIZE":"", 
        "BAIT_TERRITORY":"", 
        "TARGET_TERRITORY":"", 
        "BAIT_DESIGN_EFFICIENCY":"", 
        "TOTAL_READS":"",
        "PF_READS":"", 
        "PF_UNIQUE_READS":"", 
        "PCT_PF_READS":"", 
        "PCT_PF_UQ_READS":"", 
        "PF_UQ_READS_ALIGNED":"", 
        "PCT_PF_UQ_READS_ALIGNED":"",
        "PF_BASES_ALIGNED":"",      
        "PF_UQ_BASES_ALIGNED":"",
        "ON_BAIT_BASES":"", 
        "NEAR_BAIT_BASES":"", 
        "OFF_BAIT_BASES":"", 
        "ON_TARGET_BASES":"", 
        "PCT_SELECTED_BASES":"", 
        "PCT_OFF_BAIT":"",
        "ON_BAIT_VS_SELECTED":"",
        "MEAN_BAIT_COVERAGE":"",
        "MEAN_TARGET_COVERAGE":"",
        "MEDIAN_TARGET_COVERAGE":"",
        "MAX_TARGET_COVERAGE":"",
        "PCT_USABLE_BASES_ON_BAIT":"",
        "PCT_USABLE_BASES_ON_TARGET":"",
        "FOLD_ENRICHMENT":"",
        "ZERO_CVG_TARGETS_PCT":"",
        "PCT_EXC_DUPE":"",
        "PCT_EXC_MAPQ":"",
        "PCT_EXC_BASEQ":"",
        "PCT_EXC_OVERLAP":"",
        "PCT_EXC_OFF_TARGET":"",
        "FOLD_80_BASE_PENALTY":"",
        "PCT_TARGET_BASES_1X":"",
        "PCT_TARGET_BASES_2X":"",
        "PCT_TARGET_BASES_10X":"",
        "PCT_TARGET_BASES_20X":"",
        "PCT_TARGET_BASES_30X":"",
        "PCT_TARGET_BASES_40X":"",
        "PCT_TARGET_BASES_50X":"",
        "PCT_TARGET_BASES_100X":"",
        "HS_LIBRARY_SIZE":"",
        "HS_PENALTY_10X":"",
        "HS_PENALTY_20X":"",
        "HS_PENALTY_30X":"",
        "HS_PENALTY_40X":"",
        "HS_PENALTY_50X":"",
        "HS_PENALTY_100X":"",
        "AT_DROPOUT":"",
        "GC_DROPOUT":"",
        "HET_SNP_SENSITIVITY":"",
        "HET_SNP_Q":""}

    #def HSmetrics ():    
        for num, rowinfo in enumerate(hsfile, start=1): #enumerating rows
            #print ("row {}: {}".format(num, rowinfo))

            '''
            1. splitting row2 of HSfile to extract SampleID and RunID information from the 
            "INPUT=(...)" section. 

            2. extracting key metrics from HS file, all hsfile expected to have row 7 with 
            headers and row 8 displaying values

            '''

            if num in [2,6,7,8]:
                HSoutput = (num, rowinfo)
                if num == 2:
                    row2_split = rowinfo[0].split(" ")
                    for sampleinfo in row2_split:
                        if sampleinfo.startswith("INPUT="):
                            inputinfo = sampleinfo.split("=")
                            hsdict["UniqueID"]=os.environ["Unique_ID"]
                            hsdict["run_id"]=os.environ["Run_ID"] 
                            hsdict["SampleID"]=os.environ["Sample_ID"]

                if num == 7:
                    Keys = rowinfo
                if num == 8:
                    Values = rowinfo
                    length = len(Keys) #to do: need to assert that the length of keys matches length of values

                    for i in range(length):
                        hsdict[Keys[i]] = Values[i] #matches the row 7 keys with corresponding row 8 values 
                        if Values[i] == "?":
                            blank = Values[i].replace("?", "")
                            hsdict[Keys[i]] = blank
                        
                
                    return (hsdict)


'''


    UniqueID = models.CharField(max_length=100, primary_key=True)
    run_id = models.ForeignKey(
        'Runlog',
        on_delete=models.CASCADE,
    )
    SampleID = models.CharField(max_length=10)
    BAIT_SET = models.CharField(max_length=100)



INTEGERS 
    GENOME_SIZE = models.BigIntegerField()
    BAIT_TERRITORY = models.BigIntegerField(blank=True, null=True) 
    TARGET_TERRITORY = models.BigIntegerField(blank=True, null=True)
    BAIT_DESIGN_EFFICIENCY = models.BigIntegerField(blank=True, null=True)
    TOTAL_READS = models.IntegerField(blank=True, null=True)
    PF_READS = models.IntegerField(blank=True, null=True)
    PF_UNIQUE_READS = models.IntegerField(blank=True, null=True)
    PCT_PF_READS = models.IntegerField(blank=True, null=True)
    PF_UQ_READS_ALIGNED = models.IntegerField(blank=True, null=True)
    PCT_PF_UQ_READS_ALIGNED = models.IntegerField(blank=True, null=True) 
    PF_BASES_ALIGNED = models.IntegerField(blank=True, null=True)
    PF_UQ_BASES_ALIGNED = models.IntegerField(blank=True, null=True)
    ON_BAIT_BASES = models.IntegerField(blank=True, null=True) 
    NEAR_BAIT_BASES = models.IntegerField(blank=True, null=True)
    OFF_BAIT_BASES = models.IntegerField(blank=True, null=True)
    ON_TARGET_BASES = models.IntegerField(blank=True, null=True)
    HET_SNP_Q = models.IntegerField(blank=True, null=True)



DECIMALS
    PCT_PF_UQ_READS = models.DecimalField(max_digits=20, decimal_places=10, blank=True, null=True)
    PCT_SELECTED_BASES = models.DecimalField(max_digits=20, decimal_places=10, blank=True, null=True)
    PCT_OFF_BAIT = models.DecimalField(max_digits=20, decimal_places=10, blank=True, null=True)
    ON_BAIT_VS_SELECTED = models.DecimalField(max_digits=20, decimal_places=10, blank=True, null=True)
    MEAN_BAIT_COVERAGE = models.DecimalField(max_digits=20, decimal_places=10, blank=True, null=True)
    MEAN_TARGET_COVERAGE = models.DecimalField(max_digits=20, decimal_places=10, blank=True, null=True)
    MEDIAN_TARGET_COVERAGE = models.DecimalField(max_digits=20, decimal_places=10, blank=True, null=True)
    MAX_TARGET_COVERAGE = models.DecimalField(max_digits=20, decimal_places=10, blank=True, null=True)
    PCT_USABLE_BASES_ON_BAIT = models.DecimalField(max_digits=20, decimal_places=10, blank=True, null=True)
    PCT_USABLE_BASES_ON_TARGET = models.DecimalField(max_digits=20, decimal_places=10, blank=True, null=True)
    FOLD_ENRICHMENT = models.DecimalField(max_digits=20, decimal_places=10, blank=True, null=True)
    ZERO_CVG_TARGETS_PCT = models.DecimalField(max_digits=20, decimal_places=10, blank=True, null=True)
    PCT_EXC_DUPE = models.DecimalField(max_digits=20, decimal_places=10, blank=True, null=True)
    PCT_EXC_MAPQ = models.DecimalField(max_digits=20, decimal_places=10, blank=True, null=True)
    PCT_EXC_BASEQ = models.DecimalField(max_digits=20, decimal_places=10, blank=True, null=True)
    PCT_EXC_OVERLAP = models.DecimalField(max_digits=20, decimal_places=10, blank=True, null=True)
    PCT_EXC_OFF_TARGET = models.DecimalField(max_digits=20, decimal_places=10, blank=True, null=True)
    FOLD_80_BASE_PENALTY = models.DecimalField(max_digits=20, decimal_places=10, blank=True, null=True)
    PCT_TARGET_BASES_1X =  models.DecimalField(max_digits=20, decimal_places=10, blank=True, null=True)
    PCT_TARGET_BASES_2X = models.DecimalField(max_digits=20, decimal_places=10, blank=True, null=True)
    PCT_TARGET_BASES_10X = models.DecimalField(max_digits=20, decimal_places=10, blank=True, null=True)
    PCT_TARGET_BASES_20X = models.DecimalField(max_digits=20, decimal_places=10, blank=True, null=True)
    PCT_TARGET_BASES_30X = models.DecimalField(max_digits=20, decimal_places=10, blank=True, null=True)
    PCT_TARGET_BASES_40X = models.DecimalField(max_digits=20, decimal_places=10, blank=True, null=True)
    PCT_TARGET_BASES_50X = models.DecimalField(max_digits=20, decimal_places=10, blank=True, null=True)
    PCT_TARGET_BASES_100X = models.DecimalField(max_digits=20, decimal_places=10, blank=True, null=True)
    HS_LIBRARY_SIZE = models.DecimalField(max_digits=20, decimal_places=10, blank=True, null=True)
    HS_PENALTY_10X = models.DecimalField(max_digits=20, decimal_places=10, blank=True, null=True) 
    HS_PENALTY_20X = models.DecimalField(max_digits=20, decimal_places=10, blank=True, null=True)
    HS_PENALTY_30X = models.DecimalField(max_digits=20, decimal_places=10, blank=True, null=True)
    HS_PENALTY_40X = models.DecimalField(max_digits=20, decimal_places=10, blank=True, null=True)
    HS_PENALTY_50X = models.DecimalField(max_digits=20, decimal_places=10, blank=True, null=True)
    HS_PENALTY_100X = models.DecimalField(max_digits=20, decimal_places=10, blank=True, null=True)
    AT_DROPOUT = models.DecimalField(max_digits=20, decimal_places=10, blank=True, null=True)
    GC_DROPOUT = models.DecimalField(max_digits=20, decimal_places=10, blank=True, null=True)
    HET_SNP_SENSITIVITY = models.DecimalField(max_digits=20, decimal_places=10, blank=True, null=True)




'''


