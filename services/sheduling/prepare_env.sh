echo -e "AIRFLOW_UID=$(id -u)\nAIRFLOW_GID=0" > .env
echo -e "CUR=services/sheduling" >> .env
echo -e "CUR_ABS=$(pwd)" >> .env
echo "AWS_CREDENTIALS='$(cat ~/.aws/credentials)'" >> .env
#"export PRIVATE_KEY='`cat ./gitbu.2018-03-23.private-key.pem`'"