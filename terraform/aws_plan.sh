#!/bin/bash

DEPLOYMENT_DIR="../project"
TERRAFORM_DIR=$(pwd)

terraform init

pip install -r ../requirements.txt -t $DEPLOYMENT_DIR

cp ../main.py $DEPLOYMENT_DIR
cp ../spotify_etl.py $DEPLOYMENT_DIR
cp ../exceptions.py $DEPLOYMENT_DIR

cd $DEPLOYMENT_DIR

zip -r ../lambda.zip *

cd $TERRAFORM_DIR
rm -rf $DEPLOYMENT_DIR

terraform plan
