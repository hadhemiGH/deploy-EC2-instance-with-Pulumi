import pulumi
import pulumi_aws as aws

size = 't2.micro'
ami=aws.get_ami(most_recent=True,
    filters=[
        aws.GetAmiFilterArgs(
            name="name",
            values=["ubuntu/images/hvm-ssd/ubuntu-bionic-18.04-amd64-server-*"],
        ),
        aws.GetAmiFilterArgs(
            name="virtualization-type",
            values=["hvm"],
        ),
    ],
    owners=["099720109477"])

#my_key_pair=aws.ec2.KeyPair("deployer", public_key="ss..")
#lg_key_pair = aws.lightsail.KeyPair("Pulumi_KeyPair", public_key=(lambda path: open(path).read())("key.pem"))


group = aws.ec2.SecurityGroup('sg_test',
    description=' Pulumi- allow all traffic',
    ingress=[
        { 'protocol': '-1', 'from_port': 0, 'to_port': 0, 'cidr_blocks': ['0.0.0.0/0'] }
    ])



user_data = """
#!/bin/bash

"""
server = aws.ec2.Instance('server',
    instance_type=size,
    vpc_security_group_ids=[group.id], # reference security group from above
    user_data=user_data,
    ami=ami.id,
    key_name= "key" )


pulumi.export('publicIp', server.public_ip)
pulumi.export('publicHostName', server.public_dns)