
#set -euo pipefail 

source activate runlogdb-env


results_runfolder=$1 #data/results/runID

#DB='/Users/Seemu/RunlogDB'
DB='/export/home/sa/RunlogDB'



#----------------------------------

for filename in $results_runfolder*/*/*
do
	ext=$(basename $filename)
	echo $ext
	case "$ext" in
	*HsMetrics.txt) python3.6 $DB/maintest.py $filename  
			;;
esac
done	


for filename in $results_runfolder*/*/*
do
	ext=$(basename $filename)
	case "$ext" in
	*fastqc.txt) python3.6 $DB/maintest.py $filename 
			;;
esac
done	


#----------------------------------------------------------------------------------

#Truesightmyeloid

case "$Panel" in
	TrueSightMyeloid) 
		for filename in $results_runfolder*/*/*/*
		do
			ext=$(basename $filename)
			echo $ext 
			case "$ext" in
			*summary.txt) python3.6 $DB/maintest.py $filename
			prefix=$(dirname $filename) # HSmetrics = /Users/Seemu/CRUK_test/SMP2v2/metrics/Sample2  fqc=/Users/Seemu/CRUK_test/SMP2v2/Sample1/trimmed
			Join="_"
			#SampleID=$(echo $prefix | cut -d/ -f6)
			SampleID=$(echo $prefix | rev | cut -d/ -f2 |rev)
			echo $SampleID
			#RunID=$(echo $prefix | cut -d/ -f4)
			Run_ID=$(echo $prefix | rev | cut -d/ -f4 |rev)
			UniqueID="$RunID$Join$SampleID"
			export SampleID
			export RunID
			export UniqueID
			python3.6 $DB/maintest.py $filename

					;;
		esac
		done  ;
esac


#-----------------------------------------------------------------------------------

#CRUK 

Panel=$(basename $results_runfolder*/)
#echo $Panel
case "$Panel" in
	SMP2v2) 
		
		for filename in $results_runfolder*/*/*/*
		do
			ext=$(basename $filename)
			prefix=$(dirname $filename)
			echo $ext 
			echo $prefix
			case "$ext" in
			*HsMetrics.txt) 
			prefix=$(dirname $filename) # HSmetrics = /Users/Seemu/CRUK_test/SMP2v2/metrics/Sample2  fqc=/Users/Seemu/CRUK_test/SMP2v2/Sample1/trimmed/fqc
			Sample_ID=$(basename $prefix)
			Join="_"
			Run_ID=$(echo $prefix | rev | cut -d/ -f4 |rev)
			Unique_ID="$Run_ID$Join$Sample_ID"
			export Sample_ID
			export Run_ID
			export Unique_ID
			python3.6 $DB/maintest.py $filename
					;;

		esac
		done  ;
esac




case "$Panel" in
	SMP2v2) 
		for filename in $results_runfolder*/*/*/*/*
		do
			ext=$(basename $filename)
			echo $ext 
			case "$ext" in
			*summary.txt) #python3.6 $DB/maintest.py $filename
			prefix=$(dirname $filename) # HSmetrics = /Users/Seemu/CRUK_test/SMP2v2/metrics/Sample2  fqc=/Users/Seemu/CRUK_test/SMP2v2/Sample1/trimmed/fqc
			Join="_"
			echo $prefix
			SampleID=$(echo $prefix | rev | cut -d/ -f3 |rev)
			echo $SampleID
			RunID=$(echo $prefix | rev | cut -d/ -f5 |rev)
			UniqueID="$RunID$Join$SampleID"
			export SampleID
			export RunID
			export UniqueID
			python3.6 $DB/maintest.py $filename

					;;
		esac
		done  ;
esac









source deactivate
