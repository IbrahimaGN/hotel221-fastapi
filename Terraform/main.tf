# Recherche automatique de la derniere AMI Ubuntu 24.04 LTS disponible dans la region
data "aws_ami" "ubuntu_24" {
  most_recent = true
  owners      = ["099720109477"] # Identifiant officiel de Canonical (Ubuntu)

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd-gp3/ubuntu-noble-24.04-amd64-server-*"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
}



terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

# 1. Configuration du Pare-feu (Security Group)
resource "aws_security_group" "hotel221_sg" {
  name        = "hotel221-sg"
  description = "Autoriser HTTP, HTTPS et SSH"

  ingress {
    description = "SSH de nimporte ou" # <-- Nettoyé (plus d'apostrophe)
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "HTTP pour l API" # <-- Nettoyé (plus d'accent ni d'apostrophe)
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# 2. Création de l'instance AWS EC2
resource "aws_instance" "hotel221_server" {
  ami                    = data.aws_ami.ubuntu_24.id # <--- Ligne modifiee ici !
  instance_type          = "t3.micro"
  key_name               = var.key_name
  vpc_security_group_ids = [aws_security_group.hotel221_sg.id]

  tags = {
    Name = "Hotel221-FastAPI-Docker"
  }

  # 3. Script d'automatisation au démarrage (User Data)
  user_data = <<-EOF
              #!/bin/bash
              # Mise a jour du systeme
              apt-get update -y
              apt-get upgrade -y

              # Installation de Docker et Docker Compose
              apt-get install docker.io docker-compose git -y
              systemctl start docker
              systemctl enable docker
              usermod -aG docker ubuntu

              # Clonage du projet
              cd /home/ubuntu
              git clone https://github.com/ibrahimaGN/hotel221-fastapi.git
              chown -R ubuntu:ubuntu hotel221-fastapi

              # Lancement du projet avec Docker
              cd hotel221-fastapi
              docker-compose up --build -d
              EOF
}

# Afficher l'IP publique à la fin du script
output "instance_public_ip" {
  value       = aws_instance.hotel221_server.public_ip
  description = "L'IP publique du serveur créé"
}