#!/bin/sh

tail -f /dev/null | tail -f /dev/null &
PID2=$!
PID1=$(jobs -p %+)

tail -f /dev/null | tail -f /dev/null &
PID4=$!
PID3=$(jobs -p %+)

#echo PIDS: $PID1 $PID2
#echo PIDS: $PID3 $PID4

exec 3>/proc/$PID1/fd/1 4</proc/$PID2/fd/0
exec 5>/proc/$PID3/fd/1 6</proc/$PID4/fd/0


/get_flag <&6 >&3 &
read <&4
read chal <&4
echo $(($chal))  >&5
read flag <&4
echo $flag
disown $PID1 $PID3
kill $PID1 $PID2 $PID3 $PID4
