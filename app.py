#!/usr/bin/env python3
import os

import aws_cdk as cdk
from aws_cdk import core

#web app with vpc asg and alb
from infraTemplates.vpc import VpcStack
from infraTemplates.compute import ComputeStack


app = core.App()
vpc_stack = VpcStack(app, "vpc-stack")
compute_stack = ComputeStack(app, "compute-stack", VPC=vpc_stack.VPC01)

app.synth()
