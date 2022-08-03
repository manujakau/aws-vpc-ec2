# aws-vpc-ec2
aws-cdk deployment

prerequisite
```
$ sudo apt install -y python3-pip
$ sudo apt install -y python3-venv
$ curl -sL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
$ sudo apt update -y
$ sudo apt-get install -y nodejs
$ sudo apt-get install -y build-essential
$ sudo npm install -g aws-cdk
```

Setup CDK project

Then follow the below steps to complete rest.
```
$ cdk init app --language python
$ python3 -m venv .venv
$ source .venv/bin/activate
$ pip3 install -r requirements.txt
```

Remove broken aws-cdk packages
```
pip3 freeze | grep -v "^-e" | xargs pip3 uninstall -y
```

At this point you can now synthesize the CloudFormation template for this code.

```
$ cdk bootstrap
$ cdk ls
$ cdk synth
```