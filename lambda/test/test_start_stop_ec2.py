import boto3
import importlib
from moto import mock_ec2

MOCK_REGION = 'ap-northeast-1'
MOCK_AMI_ID = '/aws/service/ami-amazon-linux-latest/amzn-ami-hvm-x86_64-ebs'
MOCK_INSTANCE_TYPE = 't3.nano'
MOCK_INSTANCE_NAME = 'mock_instance'


@mock_ec2
class TestStartStopEc2:
    assec2 = importlib.import_module('lambda.auto-start-stop-ec2')
    ec2_client = None
    mock_instance = {}

    def setup_method(self, method):
        self.ec2_client = boto3.client('ec2', region_name=MOCK_REGION)
        res = self.ec2_client.run_instances(ImageId=MOCK_AMI_ID,
                                            InstanceType=MOCK_INSTANCE_TYPE,
                                            MinCount=1,
                                            MaxCount=1,
                                            TagSpecifications=[
                                                {
                                                    'ResourceType': 'instance',
                                                    'Tags': [
                                                        {
                                                            'Key': 'AutoStartStop',
                                                            'Value': 'TRUE'
                                                        },
                                                        {
                                                            'Key': 'Name',
                                                            'Value': MOCK_INSTANCE_NAME
                                                        }
                                                    ]}
                                            ])
        self.mock_instance = {
            'instance_id': res['Instances'][0]['InstanceId'],
            'instance_name': MOCK_INSTANCE_NAME
        }

    def teardown_method(self, method):
        self.ec2_client.terminate_instances(
            InstanceIds=[self.mock_instance['instance_id']])

    def test_describe_instances(self):
        res = self.ec2_client.describe_instances(
            Filters=[{'Name': 'tag:AutoStartStop', "Values": ['TRUE']}])

        first_instance = res['Reservations'][0]['Instances'][0]

        assert len(res['Reservations'][0]['Instances']) == 1
        assert first_instance['State']['Name'] == 'running'
        self.mock_instance = {
            'instance_id': first_instance['InstanceId'],
            'instance_name': ''
        }

    def test_get_target_ec2_instances(self):
        res = self.assec2.get_target_ec2_instances(self.ec2_client)

        assert len(res) == 1
        assert res[0]['instance_name'] == MOCK_INSTANCE_NAME

    def test_stop_ec2_instance(self):
        res = self.assec2.stop_instance(self.ec2_client, self.mock_instance)
        assert res is True

    def test_start_ec2_instance(self):
        res = self.assec2.start_instance(self.ec2_client, self.mock_instance)
        assert res is True
