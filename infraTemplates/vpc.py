from aws_cdk import (
    core,
    aws_ec2
)

class VpcStack(core.Stack):
    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        VPC_CONFIG = self.node.try_get_context('envs')['prod']

        self.VPC01 = aws_ec2.Vpc(
            self,
            "CustomVpcID",
            cidr=VPC_CONFIG['vpc_config']['vpc_cidr'],
            max_azs=2,
            nat_gateways=1,
            subnet_configuration=[
                aws_ec2.SubnetConfiguration(
                    name="PublicSubnet", 
                    cidr_mask=VPC_CONFIG['vpc_config']['cidr_mask'],
                    subnet_type=aws_ec2.SubnetType.PUBLIC
                ),
                aws_ec2.SubnetConfiguration(
                    name="PrivateSubnet",
                    cidr_mask=VPC_CONFIG['vpc_config']['cidr_mask'],
                    subnet_type=aws_ec2.SubnetType.PRIVATE_WITH_NAT
                )
            ]
        )

        core.Tags.of(self.VPC01).add("Name", "CDK-VPC")

        core.CfnOutput(
            self,
            "CustomVpcIDoutput",
            value=self.VPC01.vpc_id,
            export_name="CustomVpcID"
        )