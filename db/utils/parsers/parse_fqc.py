import csv
import os
'''
Creating a Fastqc dictionary of sample quality metrics
'''


def Fastqc (file):
    with open (file) as file:
        fqcfile = csv.reader(file, delimiter="\t")
        fqcdict = {}
        for column in fqcfile:
                metrics = column[1]
                result = column[0]
                input = column[2].split("_")
                UniqueID = "_".join(input[:5])
                SampleID = input[4]
                Read_Group = input[-1].strip(".fastq")
                Lane = input[5]
                RunID = '_'.join(input[:4])
                fqcdict["UniqueID"] = UniqueID
                fqcdict["general_readinfo"]= column[2]
                fqcdict["SampleID"]= SampleID
                fqcdict["RunID"] = RunID
                fqcdict["Read_Group"] = Read_Group
                fqcdict["Lane"] = Lane
                fqcdict[metrics] = result

        return (fqcdict)


def Fastqc_CRUK (file):
    with open (file) as file:
        fqcfile = csv.reader(file, delimiter="\t")
        fqcdict = {}
        for column in fqcfile:
                metrics = column[1]
                result = column[0]
                input = column[2].split("_")
                print(input)
                Read_Group = input[3]
                Lane = input[2]
                fqcdict["UniqueID"] = os.environ["UniqueID"]
                fqcdict["general_readinfo"]= column[2]
                fqcdict["SampleID"]= os.environ["SampleID"]
                fqcdict["RunID"] = os.environ["RunID"]
                fqcdict["Read_Group"] = Read_Group
                fqcdict["Lane"] = Lane
                fqcdict[metrics] = result

        return (fqcdict)
