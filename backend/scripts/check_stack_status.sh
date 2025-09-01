#!/bin/bash
###
# this script is to check the status of each of cf stacks and trigger rollback if in failed state
# and continue on to next stack if in complete state

printf "%s\n%s\neu-west-1\njson" "$AWS_ACCESS_KEY_ID" "$AWS_SECRET_ACCESS_KEY" | aws configure

stacks_array=($STACK_NAMES)
echo "the stack names are $STACK_NAMES"
for STACK_NAME in "${stacks_array[@]}"; do

    # Check status of each stack and wait until finished creating/updating so we can see whether it passed or failed
    stack_status=$(aws cloudformation describe-stacks --stack-name $STACK_NAME | jq '.Stacks[] | .StackStatus')
    until [[ $stack_status != "\"CREATE_IN_PROGRESS"\" && $stack_status != "\"UPDATE_IN_PROGRESS"\" && $stack_status != "\"UPDATE_COMPLETE_CLEANUP_IN_PROGRESS"\" ]]; do
        echo "Stack $STACK_NAME still creating/updating, polling in 10s intervals until complete"
        sleep 10
        stack_status=$(aws cloudformation describe-stacks --stack-name $STACK_NAME | jq '.Stacks[] | .StackStatus')
    done

    #if the stack status is complete then print and move onto next stack
    if [[ $stack_status = "\"CREATE_COMPLETE"\" || $stack_status = "\"UPDATE_COMPLETE"\" ]]; then
        echo "Stack $STACK_NAME created/updated successfully with status $stack_status, check next stack"
        continue
    #else if stack status contains failed then set rollback status to true and exit for loop
    elif [[ $stack_status =~ .*"_FAILED".* ]]; then
        echo "Stack $STACK_NAME failed to create/be updated with status $stack_status, setting rollback status to true"
        echo "##vso[task.setvariable variable=rollback]true"
        echo "##vso[task.setvariable variable=deployment_failed]true"
        break
        #else if stack status contains rollback then set rollback status to true and exit for loop
    elif [[ $stack_status =~ .*"ROLLBACK".* ]]; then
        echo "Stack $STACK_NAME having rollback with status $stack_status, setting rollback status to true"
        echo "##vso[task.setvariable variable=rollback]true"
        echo "##vso[task.setvariable variable=deployment_failed]true"
        break
    #else print the status (would only be in progress, so should investigate what's in progress)
    else
        echo "Stack $STACK_NAME has status $stack_status, please investigate and see link to types of status messages: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-describing-stacks.html"
    fi
done