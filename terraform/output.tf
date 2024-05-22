output "vpc_id" {
  description = "The ID of the VPC"
  value       = aws_vpc.devops_vpc.id
}

output "subnet_1_id" {
  description = "The ID of the first subnet"
  value       = aws_subnet.devops_subnet_1.id
}

output "subnet_2_id" {
  description = "The ID of the second subnet"
  value       = aws_subnet.devops_subnet_2.id
}

output "devops_server_1_id" {
  description = "The ID of the first DevOps server"
  value       = aws_instance.devops_server_1.id
}

output "devops_server_2_id" {
  description = "The ID of the second DevOps server"
  value       = aws_instance.devops_server_2.id
}


output "devops_server_1_private_ip" {
  description = "The private IP of the first DevOps server"
  value       = aws_instance.devops_server_1.private_ip
}

output "devops_server_2_private_ip" {
  description = "The private IP of the second DevOps server"
  value       = aws_instance.devops_server_2.private_ip
}

