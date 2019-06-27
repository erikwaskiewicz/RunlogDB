# To add to cron job:
set -euo pipefail

if bash add_run.sh $path >> runlog_upload_log.txt 2>&1; then
    :
fi

if bash add_nipt.sh >> runlog_upload_log.txt 2>&1; then
    :
fi
