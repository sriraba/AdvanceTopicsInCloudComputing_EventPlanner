import json
import boto3
import os

dynamodb = boto3.client('dynamodb')
sqs_client = boto3.client('sqs')

def lambda_handler(event, context):
    event_type=event['eventtype']
    date = event['date']
    print(date)
    print('The type is : ', type(date))

    if event_type == 'wedding':
        response = dynamodb.query(
            TableName='wedding_slots_new1',
            KeyConditionExpression='event_date = :pk',
            ExpressionAttributeValues={
                ':pk': {'S': date}
            }
        )
    else:
        response = dynamodb.query(
            TableName='birthday_slots_new1',
            KeyConditionExpression='event_date = :pk',
            ExpressionAttributeValues={
                ':pk': {'S': date}
            }
        )

    print(' response["Items"]', response['Items'])
    for item in response['Items']:
        slot_count = item['max_bookings']
        print('slot_count ', slot_count['S'])

    if slot_count['S'] != '0':
        updateSlotCount(slot_count, date)
        if event_type == 'wedding':
            queueUrl = os.environ['weedingconfirmurl']
        else:
            queueUrl = os.environ['birthdayconfirmurl']
        final_response=sendMessageToConfirmQueue(queueUrl,event)
        print(final_response)
    else:
        if event_type == 'wedding':
            queueUrl = os.environ['weedingnotconfirmurl']
        else:
            queueUrl = os.environ['birthdaynotconfirmurl']
        final_response=sendMessageToNotAvailableQueue(queueUrl,event)
        print(final_response)
    return final_response


def updateSlotCount(slot_count, date):
    updated_count = int(slot_count['S']) - 1
    dict_data = {
        'date': date,
        'count': str(updated_count)
    }
    result = dynamodb.update_item(
        TableName='wedding_slots_new1',
        Key={
            'event_date': {'S': dict_data['date']}
        },
        UpdateExpression='SET max_bookings = :val',
        ExpressionAttributeValues={
            ':val': {'S': dict_data['count']}
        }
    )


def sendMessageToConfirmQueue(queueUrl,event):
    slot_response = {
            'type': 'QUEUE',
            'returnCode': 0,
            'email': event['email'],
            'firstname': event['firstname'],
            'phone': event['phone'],
            'city': event['city'],
            'guestcount': event['guestcount'],
            'date': event['date'],
            'budget': event['budget']
        }
    response = sqs_client.send_message(
         QueueUrl=queueUrl,
           MessageBody=json.dumps(slot_response)
        )
    return slot_response


def sendMessageToNotAvailableQueue(queueUrl,event):
    slot_response = {
            'type': 'APP',
            'returnCode': 0,
            'email': event['email'],
            'firstname': event['firstname'],
            'phone': event['phone'],
            'city': event['city'],
            'guestcount': event['guestcount'],
            'date': event['date'],
            'budget': event['budget']
        }
    response = sqs_client.send_message(
         QueueUrl=queueUrl,
           MessageBody=json.dumps(slot_response)
        )
    return slot_response


