from aws_cdk import (
    core,
    aws_ec2,
    aws_iam,
    aws_elasticloadbalancingv2 as aws_elbv2,
    aws_autoscaling as aws_asg
)

class ComputeStack(core.Stack):
    def __init__(self, scope: core.Construct, construct_id: str, VPC, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        try:
            with open("userDataScripts/setup.sh", mode="r") as file:
                USER_DATA = file.read()
        except OSError:
            print('Userdata can not apply')
        
        AWS_LINUX_AMI = aws_ec2.MachineImage.latest_amazon_linux(
            generation=aws_ec2.AmazonLinuxGeneration.AMAZON_LINUX_2,
            edition=aws_ec2.AmazonLinuxEdition.STANDARD,
            storage=aws_ec2.AmazonLinuxStorage.GENERAL_PURPOSE,
            virtualization=aws_ec2.AmazonLinuxVirt.HVM
        )


        ALB = aws_elbv2.ApplicationLoadBalancer(
            self,
            "ALBID",
            vpc=VPC,
            internet_facing=True,
            load_balancer_name="ApplicationALB"
        )

        ALB.connections.allow_from_any_ipv4(
            aws_ec2.Port.tcp(80),
            description="Allow Web Traffic"
        )

        LISTENER = ALB.add_listener(
            "AlbListenerID",
            port=80,
            open=True
        )


        ALB_ROLE = aws_iam.Role(
            self,
            "ALBRoleID",
            assumed_by=aws_iam.ServicePrincipal(
                'ec2.amazonaws.com'
            ),
            managed_policies= [
                aws_iam.ManagedPolicy.from_aws_managed_policy_name(
                    'AmazonSSMManagedInstanceCore'
                ),
                aws_iam.ManagedPolicy.from_aws_managed_policy_name(
                    'AmazonS3ReadOnlyAccess'
                )
            ]
        )


        LC_ASG = aws_asg.AutoScalingGroup(
            self,
            "AppLcAsgID",
            vpc=VPC,
            vpc_subnets=aws_ec2.SubnetSelection(
                subnet_type=aws_ec2.SubnetType.PRIVATE
            ),
            instance_type=aws_ec2.InstanceType(
                instance_type_identifier="t3.medium"
            ),
            machine_image=AWS_LINUX_AMI,
            role=ALB_ROLE,
            min_capacity=2,
            max_capacity=3,
            desired_capacity=2,
            user_data=aws_ec2.UserData.custom(USER_DATA)
        )

        LC_ASG.connections.allow_from(
            ALB,
            aws_ec2.Port.tcp(80),
            description="Allow autoscalling traffic from ALB"
        )

        LISTENER.add_targets(
            "AlbListenerID",
            port=80,
            targets=[
                LC_ASG
            ]
        )


        ALB_OUTPUT = core.CfnOutput(
            self,
            "AlbUrl",
            value=ALB.load_balancer_dns_name,
            description="WEB URL"
        )