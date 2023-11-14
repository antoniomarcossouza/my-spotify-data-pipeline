#!/bin/bash

TERRAFORM_DIR=$(pwd)
PROJECT_DIR=$(dirname "$TERRAFORM_DIR")
DEPLOY_DIR="$PROJECT_DIR/deploy"
PKG_DIR="$PROJECT_DIR/python"

# Removing previous files

rm -rf $PROJECT_DIR/*.zip

# Requests layer

rm -rf $PKG_DIR && mkdir -p $PKG_DIR

pip install requests -t $PKG_DIR

rm -rf $PKG_DIR/*.dist-info $PKG_DIR/__pycache__

cd $PROJECT_DIR
zip -r9 ./requests.zip ./python

# Lambda function

rm -rf $DEPLOY_DIR && mkdir -p $DEPLOY_DIR

cp $PROJECT_DIR/lambda_function.py $DEPLOY_DIR
cp $PROJECT_DIR/spotify_etl.py $DEPLOY_DIR
cp $PROJECT_DIR/exceptions.py $DEPLOY_DIR

cd $DEPLOY_DIR
zip -r $PROJECT_DIR/lambda.zip *

# Removing files

rm -rf $PKG_DIR $DEPLOY_DIR

# Terraform

cd $TERRAFORM_DIR
terraform init
terraform plan
