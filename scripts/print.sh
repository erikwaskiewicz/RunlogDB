#!/bin/bash

echo ""
echo "Runlog table"
echo "----------------"
sqlite3 -column -header /data/diagnostics/apps/RunlogDB/runlog/runlogdb.sqlite3 "select * from db_runlog"

echo ""
echo "MiSeq table"
echo "----------------"
sqlite3 -column -header /data/diagnostics/apps/RunlogDB/runlog/runlogdb.sqlite3 "select * from db_miseq"

echo ""
echo "HiSeq table"
echo "----------------"
sqlite3 -column -header /data/diagnostics/apps/RunlogDB/runlog/runlogdb.sqlite3 "select * from db_hiseq"

echo ""
echo "NextSeq table"
echo "----------------"
sqlite3 -column -header /data/diagnostics/apps/RunlogDB/runlog/runlogdb.sqlite3 "select * from db_nextseq"

