import json
import boto3

dynamo_client = boto3.client('dynamodb')
sns_client = boto3.client('sns')

def lambda_handler(event, context):
    body = event
    # body = json.loads(body)
    print(body['email'])
    # TODO implement
    data = dynamo_client.put_item(
    TableName='users_new',
    Item={
        'email': {
          'S': body['email']
        },
        'firstname': {
          'S': body['firstname']
        },
        'lastname': {
          'S': body['lastname']
        },
        'password': {
          'S': body['password']
        }
    }
  )
    data1 = dynamo_client.put_item(
    TableName='wedding_slots_new1',
    Item={
        'event_date': {
          'S': '12-04-2023'
        },
        'max_bookings': {
          'S': '1'
        }
    }
  )
    data2 = dynamo_client.put_item(
    TableName='birthday_slots_new1',
    Item={
        'event_date': {
          'S': '12-04-2023'
        },
        'max_bookings': {
          'S': '1'
        }
    }
  )
    topic_name = body['firstname'] + '-' + body['lastname']
    
    # Create a topic
    response = sns_client.create_topic(Name=str(topic_name))
    
    # Get the ARN of the topic
    topic_arn = response['TopicArn']
    
    # Subscribe an email address to the topic
    response = sns_client.subscribe(
        TopicArn=topic_arn,
        Protocol='email',
        Endpoint=body['email']
    )
    
    return {
      'statusCode': 200,
      'body': 'successfully created item!',
      'headers': {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*'
      }
  }