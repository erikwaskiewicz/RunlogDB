#!/bin/bash
DB='/Users/Seemu/RunlogDB/runlog/runlogdb.sqlite3'
#DB="/Users/erik/Projects/RunlogDB/run/runlogdb.sqlite3"

echo ""
echo "Runlog table"
echo "----------------"
sqlite3 -column -header $DB "select * from db_runlog"

echo ""
echo "MiSeq table"
echo "----------------"
sqlite3 -column -header $DB "select * from db_miseq"

echo ""
echo "HiSeq table"
echo "----------------"
sqlite3 -column -header $DB "select * from db_hiseq"

echo ""
echo "NextSeq table"
echo "----------------"
sqlite3 -column -header $DB "select * from db_nextseq"

echo ""
echo "Sample table"
echo "----------------"
sqlite3 -column -header $DB "select * from db_SampleMetrics"
