#!/bin/sh
# Removes a whole bunch of binaries

shopt -s extglob

if [[ ! -f /.dockerenv ]];
then
    echo "We are not in docker. Exiting..."
    exit;
fi


cd /bin

for f in !(bash|cat|cp|dd|dir|dash|echo|false|grep|ls|ln|mkdir|mv|pwd|rm|rmdir|sed|sh|touch|true|su|which|shell|runuser)
do
    echo "Removing /bin/$f"
    rm $f
done

cd /usr/bin
for f in !(awk|base64|basename|clear|cmp|env|expr|find|id|head|groups|realpath|rev|seq|sort|split|sum|tee|tail|uniq|wc|which|touch|whoami)
do
    echo "Removing /usr/bin/$f"
    rm $f
done
