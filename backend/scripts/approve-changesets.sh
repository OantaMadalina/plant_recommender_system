#!/bin/bash

###
# This script takes a list of cloudformation stack names
# It gets the ID of the latest changeset and approves it
# For each stack in the list
###

printf "%s\n%s\neu-west-1\njson" "$AWS_ACCESS_KEY_ID" "$AWS_SECRET_ACCESS_KEY" | aws configure

stacks_array=($STACK_NAMES)

for STACK_NAME in "${stacks_array[@]}"; do
    # Get latest changeset name

    CHANGESET_INFO=$(aws cloudformation list-change-sets --stack-name $STACK_NAME)

    CHANGESET_ID=$(echo $CHANGESET_INFO \
                    | jq '.Summaries[-1].ChangeSetId' \
                    | tr -d '"')
    
    CHANGESETNAME=$(echo $CHANGESET_INFO \
                    | jq '.Summaries[-1].ChangeSetName' \
                    | tr -d '"')

    changeset_status=$(aws cloudformation describe-change-set --change-set-name $CHANGESETNAME --stack-name $STACK_NAME | jq '.Status')
    # Wait until changeset has finished creating so we can query it
    until [[ $changeset_status != "\"CREATE_IN_PROGRESS"\" ]]; do
        echo "Changeset still creating, polling in 10s intervals until complete"
        sleep 10
        changeset_status=$(aws cloudformation describe-change-set --change-set-name $CHANGESETNAME --stack-name $STACK_NAME | jq '.Status')
    done
    aws cloudformation execute-change-set --change-set-name $CHANGESET_ID

    # If sequential flag is enabled then wait until one stack is deployed before executing the others
    # Not checking for deploy failures here, that's what check-status is for
    if [ $SEQUENTIAL == "True" ]; then
        echo "Sequential deployment, waiting for $STACK_NAME to finish updating"
        stack_status=$(aws cloudformation describe-stacks --stack-name $STACK_NAME | jq '.Stacks[0].StackStatus')
        until [[ $stack_status != "\"CREATE_IN_PROGRESS"\" && $stack_status != "\"UPDATE_IN_PROGRESS"\" && $stack_status != "\"UPDATE_COMPLETE_CLEANUP_IN_PROGRESS"\" ]]; do
            echo "Stack still updating, polling in 10s intervals until complete"
            sleep 10
            stack_status=$(aws cloudformation describe-stacks --stack-name $STACK_NAME | jq '.Stacks[0].StackStatus')
        done
    fi
done