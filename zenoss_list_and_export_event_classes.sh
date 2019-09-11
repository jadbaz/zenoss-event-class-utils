SCRIPT_NAME="$(basename $0)"
SCRIPT_FULL_PATH="$(readlink -f $0)"
DIR="$(dirname ${SCRIPT_FULL_PATH})"

pip install pyyaml --user

basename="zenoss_event_classes_`date +'%Y_%m_%d_%H_%M_%S'`"
out_yml="${basename}.yml"
out_csv="${basename}.csv"

echo "Started extracting event classes to ${out_yml}"
echo "*************************************"
time ZENHOME=/opt/zenoss /opt/zenoss/bin/zendmd --script ${DIR}/zenoss_list_event_classes.py | tail -n +2 > ${out_yml}
echo "Finished extracting event classes to ${out_yml}"

echo "*************************************"

echo "Started exporting event classes to ${out_csv}"
echo "*************************************"
time python2.7 ${DIR}/zenoss_export_event_classes_csv.py ${out_yml} ${out_csv}
echo "Finished exporting event classes to ${out_csv}"

