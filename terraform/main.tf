terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
      version = "5.49.0"
    }
  }
}

provider "aws" {
  region  = "us-east-1"
 // profile = "default"
}


resource "aws_vpc" "devops_vpc" {
 cidr_block = "10.0.0.0/16"
}

resource "aws_subnet" "devops_subnet_1" {
 vpc_id = aws_vpc.devops_vpc.id
 cidr_block = "10.0.1.0/24"
 availability_zone = "us-east-1a"
}

resource "aws_subnet" "devops_subnet_2" {
 vpc_id = aws_vpc.devops_vpc.id
 cidr_block = "10.0.2.0/24"
 availability_zone = "us-east-1b"
}



resource "aws_instance" "devops_server_1" {
  ami           = "ami-04b70fa74e45c3917"
  instance_type = "t2.micro"
  subnet_id = aws_subnet.devops_subnet_1.id

  tags = {
    Name = "devopsserver1"
  }
}

resource "aws_instance" "devops_server_2" {
  ami           = "ami-04b70fa74e45c3917"
  instance_type = "t2.micro"
  subnet_id = aws_subnet.devops_subnet_2.id

  tags = {
    Name = "devopsserver2"
  }
}
