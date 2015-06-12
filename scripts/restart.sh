if ! ps -ef | grep /home/monitor/v2.6/bin/python | grep "MinKiyal"; then
        DATE=`date +%Y-%m-%d:%H:%M:%S`
        echo "$DATE :MinKiyal radio is not working, restarting process" >> /home/monitor/Workspace/PyMusic/logs/restartLog
        exec /home/monitor/Workspace/PyMusic/start1.sh &
fi

if ! ps -ef | grep /home/monitor/v2.6/bin/python | grep "Obondoru"; then
        DATE=`date +%Y-%m-%d:%H:%M:%S`
        echo "$DATE :Obondoru radio is not working, restarting process" >> /home/monitor/Workspace/PyMusic/logs/restartLog
        exec /home/monitor/Workspace/PyMusic/start2.sh &
fi

if ! ps -ef | grep /home/monitor/v2.6/bin/python | grep "Tumar"; then
        DATE=`date +%Y-%m-%d:%H:%M:%S`
        echo "$DATE :Tumar radio is not working, restarting process" >> /home/monitor/Workspace/PyMusic/logs/restartLog
        exec /home/monitor/Workspace/PyMusic/start3.sh &
fi

if ! ps -ef | grep /home/monitor/v2.6/bin/python | grep "Sanjyra"; then
	DATE=`date +%Y-%m-%d:%H:%M:%S`
    	echo "$DATE :Sanjyra radio is not working, restarting process" >> /home/monitor/Workspace/PyMusic/logs/restartLog
    	exec /home/monitor/Workspace/PyMusic/start4.sh &
fi

if ! ps -ef | grep /home/monitor/v2.6/bin/python | grep "ManasJanyrygy"; then
        DATE=`date +%Y-%m-%d:%H:%M:%S`
        echo "$DATE :ManasJanyrygy radio is not working, restarting process" >> /home/monitor/Workspace/PyMusic/logs/restartLog
        exec /home/monitor/Workspace/PyMusic/start5.sh &
fi

if ! ps -ef | grep /home/monitor/v2.6/bin/python | grep "Maral"; then
        DATE=`date +%Y-%m-%d:%H:%M:%S`
        echo "$DATE :Maral radio is not working, restarting process" >> /home/monitor/Workspace/PyMusic/logs/restartLog
        exec /home/monitor/Workspace/PyMusic/start6.sh &
fi

if ! ps -ef | grep /home/monitor/v2.6/bin/python | grep "KyrgyzRadiosu"; then
        DATE=`date +%Y-%m-%d:%H:%M:%S`
        echo "$DATE :KyrgyzRadiosu radio is not working, restarting process" >> /home/monitor/Workspace/PyMusic/logs/restartLog
        exec /home/monitor/Workspace/PyMusic/start7.sh &
fi

if ! ps -ef | grep /home/monitor/v2.6/bin/python | grep "OK"; then
        DATE=`date +%Y-%m-%d:%H:%M:%S`
        echo "$DATE :OK radio is not working, restarting process" >> /home/monitor/Workspace/PyMusic/logs/restartLog
        exec /home/monitor/Workspace/PyMusic/start8.sh &
fi

if ! ps -ef | grep /home/monitor/v2.6/bin/python | grep "ELFM"; then
        DATE=`date +%Y-%m-%d:%H:%M:%S`
        echo "$DATE :ELFM radio is not working, restarting process" >> /home/monitor/Workspace/PyMusic/logs/restartLog
        exec /home/monitor/Workspace/PyMusic/start9.sh &
fi

if ! ps -ef | grep /home/monitor/v2.6/bin/python | grep "Almaz"; then
        DATE=`date +%Y-%m-%d:%H:%M:%S`
        echo "$DATE :Almaz radio is not working, restarting process" >> /home/monitor/Workspace/PyMusic/logs/restartLog
        exec /home/monitor/Workspace/PyMusic/start10.sh &
fi

if ! ps -ef | grep /home/monitor/v2.6/bin/python | grep "ManasFM"; then
        DATE=`date +%Y-%m-%d:%H:%M:%S`
        echo "$DATE :ManasFM radio is not working, restarting process" >> /home/monitor/Workspace/PyMusic/logs/restartLog
        exec /home/monitor/Workspace/PyMusic/start11.sh &
fi

if ! ps -ef | grep /home/monitor/v2.6/bin/python | grep "Paralament"; then
        DATE=`date +%Y-%m-%d:%H:%M:%S`
        echo "$DATE :Paralament radio is not working, restarting process" >> /home/monitor/Workspace/PyMusic/logs/restartLog
        exec /home/monitor/Workspace/PyMusic/start12.sh &
fi

if ! ps -ef | grep /home/monitor/v2.6/bin/python | grep "1Radio"; then
        DATE=`date +%Y-%m-%d:%H:%M:%S`
        echo "$DATE :Radio1 is not working, restarting process" >> /home/monitor/Workspace/PyMusic/logs/restartLog
        exec /home/monitor/Workspace/PyMusic/start13.sh &
fi


