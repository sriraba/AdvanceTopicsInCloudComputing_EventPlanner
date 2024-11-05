import json
import boto3

def lambda_handler(event, context):
    sqs = boto3.client("sqs")
    sns_client = boto3.client("sns")
    print('inside util lambda')
    queue_records=event['Records']
    print('queue_records', queue_records)
    record=queue_records[0]['body']
    jsonMessage = json.loads(record)
    print(jsonMessage['email'])
    
    if(jsonMessage['type'] == 'QUEUE'):
        message = "Thanks for booking with us. We will reach you out shortly !!"
        subject = "Your booking update"
    else:
        message = "Sorry, we're at maximum capacity. Please try again in few days."
        subject = "Your booking update"
    
    
    response2 = sns_client.list_topics()['Topics']
    print(response2)
    
        # Loop through each topic and retrieve its subscribers
    for topic in response2:
        topic_arn = topic['TopicArn']
        if(topic_arn != 'arn:aws:sns:us-east-1:096938558188:RedshiftSNS'):
            subscribers = sns_client.list_subscriptions_by_topic(TopicArn=topic_arn)['Subscriptions']
            # Print the topic and its subscribers
            print('Topic:', topic_arn)
            print('Subscribers:')
            for subscriber in subscribers:
                if(subscriber['Endpoint'] == jsonMessage['email']):
                    # message = "Thanks for booking with us. We will reach you out shortly !!"
                    response = sns_client.publish(TopicArn = topic_arn, Message = message, Subject=subject)
                    print(subscriber['Endpoint'])
    
    return response
