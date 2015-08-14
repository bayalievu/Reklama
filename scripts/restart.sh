sleep 2

if ! ps -ef | grep /home/monitor/Reklama/Reklama/identify.py | grep "MinKiyal"; then
        DATE=`date +%Y-%m-%d_%H:%M:%S`
        echo "$DATE :MinKiyal stopped working, restarting process" >> /home/monitor/Reklama/Reklama/logs/restartLog
        exec /home/monitor/Reklama/Reklama/scripts/start1.sh &
fi
sleep 1

if ! ps -ef | grep /home/monitor/Reklama/Reklama/identify.py | grep "Obondoru"; then
        DATE=`date +%Y-%m-%d_%H:%M:%S`
        echo "$DATE :Obondoru stopped working, restarting process" >> /home/monitor/Reklama/Reklama/logs/restartLog
        exec /home/monitor/Reklama/Reklama/scripts/start2.sh &
fi
sleep 1

if ! ps -ef | grep /home/monitor/Reklama/Reklama/identify.py | grep "HitFM"; then
        DATE=`date +%Y-%m-%d_%H:%M:%S`
        echo "$DATE :HitFM stopped  working, restarting process" >> /home/monitor/Reklama/Reklama/logs/restartLog
        exec /home/monitor/Reklama/Reklama/scripts/start14.sh &
fi
sleep 1


if ! ps -ef | grep /home/monitor/Reklama/Reklama/identify.py | grep "Europa"; then
        DATE=`date +%Y-%m-%d_%H:%M:%S`
        echo "$DATE :Europa stopped  working, restarting process" >> /home/monitor/Reklama/Reklama/logs/restartLog
        exec /home/monitor/Reklama/Reklama/scripts/start15.sh &
fi
sleep 1

if ! ps -ef | grep /home/monitor/Reklama/Reklama/identify.py | grep "Retro"; then
        DATE=`date +%Y-%m-%d_%H:%M:%S`
        echo "$DATE :Retro stopped working, restarting process" >> /home/monitor/Reklama/Reklama/logs/restartLog
        exec /home/monitor/Reklama/Reklama/scripts/start16.sh &
fi

