import boto3
import traceback


def get_target_ec2_instances(ec2_client):
    # type: (boto3.EC2.Client) -> list[dict]
    """Return EC2 instance IDs for start or stop.

    :return: A list of dictionaries has EC2 instance ID and instance name getted from tag "Name".
        Example: [{"instance_id": "abcdefg1234567890", "instance_name": "demo-instance"}]
    """

    responce = ec2_client.describe_instances(
        Filters=[{'Name': 'tag:AutoStartStop', "Values": ['TRUE']}])

    target_instances = []
    for reservation in responce['Reservations']:
        if 'Instances' in reservation.keys() and len(reservation['Instances']) > 0:
            for instance in reservation['Instances']:
                if instance['State']['Name'] == 'running' or instance['State']['Name'] == 'stopped':
                    instance_name = ''
                    for tag in instance['Tags']:
                        if tag['Key'] == 'Name':
                            instance_name = tag['Value']
                            break

                    target_instances.append({
                        'instance_id': instance['InstanceId'],
                        'instance_name': instance_name
                    })

    return target_instances


def start_stop_instance(ec2_client, instance, action):
    # type: (boto3.EC2.Client, dict, str) -> bool
    if action == 'start':
        return start_instance(ec2_client, instance)
    elif action == 'stop':
        return stop_instance(ec2_client, instance)
    else:
        print('Invalid action.')
        return False


def start_instance(ec2_client, instance):
    # type: (boto3.EC2.Client, dict) -> bool
    try:
        print('starting instance (ID: {id} Name: {name})'.format(
            id=instance['instance_id'], name=instance['instance_name']))

        res = ec2_client.start_instances(InstanceIds=[instance['instance_id']])
        print(res)

        return True
    except Exception:
        print('[ERROR] failed to start an EC2 instance.')
        print(traceback.format_exc())
        return False


def stop_instance(ec2_client, instance):
    # type: (boto3.EC2.Client, dict) -> bool
    try:
        print('stopping instance (ID: {id} Name: {name})'.format(
            id=instance['instance_id'], name=instance['instance_name']))

        res = ec2_client.stop_instances(InstanceIds=[instance['instance_id']])
        print(res)

        return True
    except Exception:
        print('[ERROR] failed to stop an EC2 instance.')
        print(traceback.format_exc())
        return False


def return_responce(status_code, message):
    # type: (int, str) -> dict
    return {
        'statusCode': status_code,
        'message': message}


def main(event, context):
    # type: (dict, dict) -> dict
    try:
        region = event['Region']
        action = event['Action']

        if action not in ['start', 'stop']:
            message = 'Invalid action. "action" support "start" or "stop".'
            print(message)
            return_responce(400, message)

        client = boto3.client('ec2', region)
        target_instances = get_target_ec2_instances(client)

        if len(target_instances) == 0:
            message = 'There are no instances subject to automatic {}.'.format(
                action)
            print(message)
            return_responce(200, message)

        for instance in target_instances:
            start_stop_instance(client, instance, action)

        return {
            'statusCode': 200,
            'message': ('Finished automatic {action} EC2 instances process. '
                        '[Region: {region}, Action: {action}]').format(
                            region=event['Region'], action=event['Action'])}
    except Exception:
        print(traceback.format_exc())
        return {
            'statusCode': 500,
            'message': 'An error occured at automatic start / stop EC2 instances process.'}
