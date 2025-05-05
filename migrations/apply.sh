SCRIPT_DIR="$(dirname "$(readlink -f "$0")")"

# while psql -U $POSTGRES_USER -d $POSTGRES_DB -c "select 1" > /dev/null 2>&1
# do
#   sleep 1
# done


ls -d ${SCRIPT_DIR}/*/ | while read -r dir
do
    psql -U ${POSTGRES_USER} -d ${POSTGRES_DB} -f ${dir}/up.sql
done
