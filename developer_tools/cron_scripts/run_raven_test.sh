#!/bin/bash

DATE_STRING=`date '+%F_%R'`
echo "Started" > $HOME/raven/logs/cron_started_${DATE_STRING}

#XXX some versions of bash have the problem that if output is redirected,
# sourcing and eval do not work.

source /etc/profile #2>&1 | tee -a $HOME/raven/logs/cron_output_${DATE_STRING}

eval `/usr/bin/modulecmd bash load pbs raven-devel-gcc` #2>&1 | tee -a $HOME/raven/logs/cron_output_${DATE_STRING}

env 2>&1 | tee -a $HOME/raven/logs/cron_output_${DATE_STRING}

$HOME/raven/falcon/fal_pack/raven/work_in_progress/cron_work/checkout_build_and_test.sh 2>&1 | tee -a $HOME/raven/logs/cron_output_${DATE_STRING}

tail -n 500 $HOME/raven/logs/cron_output_${DATE_STRING} | mailx -s "RAVEN cron output ${DATE_STRING}" joshua.cogliati@inl.gov