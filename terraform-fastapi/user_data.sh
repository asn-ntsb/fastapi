#!/bin/bash
sudo yum update -y
sudo yum install docker -y
sudo yum install git -y
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker ec2-user

git clone https://github.com/asn-ntsb/fastapi.git /home/ec2-user/fastapi-app

cd /home/ec2-user/fastapi-app
docker build -t fastapi-app .
docker run -d -p 80:80 fastapi-app