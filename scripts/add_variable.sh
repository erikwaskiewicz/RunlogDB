

#testing temporary script 

source activate runlogdb-env


results_runfolder=$1 #data/results/runID

DB='/Users/Seemu/RunlogDB'

#create runid, unique id and sample id variables 


Panel=$(basename $results_runfolder*/)
#echo $Panel








if test "$Panel" == "SMP2v2"
then 
	echo "working"
		
	for filename in $results_runfolder*/*/*/*
	do
		ext=$(basename $filename)
		prefix=$(dirname $filename)
		Run_ID=$(echo $prefix | rev | cut -d/ -f4 |rev)
		echo $prefix 
		echo $ext
		echo $Run_ID
	done
		case "$ext" in 
			"*HsMetrics.txt")
	
				prefix=$(dirname $filename) # HSmetrics = /Users/Seemu/CRUK_test/SMP2v2/metrics/Sample2  fqc=/Users/Seemu/CRUK_test/SMP2v2/Sample1/trimmed
				Sample_ID=$(basename $prefix)
				Join="_"
				Run_ID=$(echo $prefix | cut -d/ -l1)
				Unique_ID="$Run_ID$Join$Sample_ID"
				echo $Run_ID
				#python3.6 $DB/scripts/parse_hsmetrics.py $SampleID
				#python3.6 $DB/scripts/parse_hsmetrics.py $RunID
				#python3.6 $DB/scripts/parse_hsmetrics.py $UniqueID
				#xport Sample_ID
				#export Run_ID
				#export Unique_ID
				#python3.6 $DB/maintest.py $filename
		esac
fi




source deactivate