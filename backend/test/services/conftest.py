import os

import pytest
import boto3
from moto import mock_dynamodb, mock_s3


BOOTCAMP_BUCKET = "test"


@pytest.fixture(scope="module")
def aws_credentials():
    os.environ["environment"] = "bootcampengine_test_"
    os.environ["aws_account_id"] = "123456789012"
    os.environ["AWS_REGION"] = "eu-west-1"
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "eu-west-1"
    os.environ["BOOTCAMP_BUCKET"] = "test"
    os.environ["APPDYNAMICS_DISABLE_AGENT"] = "true"
    os.environ["GPG_SECRET_NAME"] = "bootcamp-test-gpg"


@pytest.fixture(scope="function")
def dynamodb(aws_credentials):
    with mock_dynamodb():
        yield boto3.client("dynamodb", region_name="eu-west-1")


@pytest.fixture(scope="function")
def workout_table(dynamodb):
    dynamodb.create_table(
        TableName="bootcampengine_test_workouts",
        AttributeDefinitions=[
            {
                "AttributeName": "workoutId",
                "AttributeType": "S"
            }
        ],
        KeySchema=[
            {
                "AttributeName": "workoutId",
                "KeyType": "HASH"
            }
        ],
        ProvisionedThroughput={
            "ReadCapacityUnits": 10,
            "WriteCapacityUnits": 10
        }
    )
    yield


@pytest.fixture(scope="function")
def workout_exercises_table(dynamodb):
    dynamodb.create_table(
        TableName="bootcampengine_test_workout-exercices",
        AttributeDefinitions=[
            {
                "AttributeName": "exerciseId",
                "AttributeType": "S"
            }
        ],
        KeySchema=[
            {
                "AttributeName": "exerciseId",
                "KeyType": "HASH"
            }
        ],
        ProvisionedThroughput={
            "ReadCapacityUnits": 10,
            "WriteCapacityUnits": 10
        }
    )
    yield


@pytest.fixture(scope='function')
def insert_exercises(workout_exercises_table):
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table("bootcampengine_test_workout-exercices")
    exercises = [
        {
            "exerciseId": "1",
            "exerciseName": "Push Up",
            "description": "A basic upper body exercise.",
            "category": "Strength",
            "youtubeLink": "https://www.youtube.com/watch?v=IODxDxX7oi4",
            "muscleGroups": ["Chest", "Triceps", "Shoulders"],
            "repetitions": 15,
            "totalSets": 3
        },
        {
            "exerciseId": "2",
            "exerciseName": "Squat",
            "description": "A fundamental lower body exercise.",
            "category": "Strength",
            "youtubeLink": "https://www.youtube.com/watch?v=aclHkVaku9U",
            "muscleGroups": ["Quadriceps", "Glutes", "Hamstrings"]
        },
        {
            "exerciseId": "3",
            "exerciseName": "Pull Up",
            "description": "An upper body pulling exercise.",
            "category": "Strength",
            "youtubeLink": "https://www.youtube.com/watch?v=eGo4IYlbE5g",
            "muscleGroups": ["Back", "Biceps", "Forearms"]
        },
        {
            "exerciseId": "4",
            "exerciseName": "Plank",
            "description": "A core strengthening exercise.",
            "category": "Core",
            "youtubeLink": "https://www.youtube.com/watch?v=pSHjTRCQxIw",
            "muscleGroups": ["Abdominals", "Lower Back"]
        },
        {
            "exerciseId": "5",
            "exerciseName": "Lunge",
            "description": "A lower body exercise targeting the legs and glutes.",
            "category": "Strength",
            "youtubeLink": "https://www.youtube.com/watch?v=COKYKgQ8KR0",
            "muscleGroups": ["Quadriceps", "Glutes", "Hamstrings"]
        }
    ]
    for exercise in exercises:
        table.put_item(Item=exercise)
    return exercises


@pytest.fixture(scope='function')
def insert_workouts(workout_table, insert_exercises):
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table("bootcampengine_test_workouts")
    workouts = [
        {
            'workoutId': '1',
            'workoutName': 'Upper Body Workout',
            'workoutDate': '2024-08-27',
            'exerciseIds': ['1', '3'],
            'notes': '',
            'workoutDuration': 10,
            'deleted': False
        },
        {
            'workoutId': '2',
            'workoutName': 'Lower Body Workout',
            'workoutDate': '',
            'exerciseIds': ['2', '5'],
            'notes': '',
            'workoutDuration': 0,
            'deleted': False
        },
        {
            'workoutId': '3',
            'workoutName': 'Core Workout',
            'workoutDate': '',
            'exerciseIds': [],
            'notes': '',
            'workoutDuration': 0,
            'deleted': False
        }
    ]
    for workout in workouts:
        table.put_item(Item=workout)
    return workouts


@pytest.fixture(scope="function")
def s3bucket(aws_credentials):
    with mock_s3():
        yield boto3.client("s3", region_name="eu-west-1")


@pytest.fixture(scope="function")
def bootcamp_bucket(s3bucket):
    s3bucket.create_bucket(
        Bucket=BOOTCAMP_BUCKET,
        CreateBucketConfiguration={"LocationConstraint": "eu-west-1"}
    )
    return BOOTCAMP_BUCKET
