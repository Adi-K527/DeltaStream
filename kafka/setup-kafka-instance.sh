#!/bin/bash

KEY_PATH="C:\Users\adika\Downloads\terraform-key.pem"


# ---------------- LAUNCH INSTANCE --------------------
INSTANCE_ID=$(aws ec2 run-instances \
                --image-id ami-00ca32bbc84273381 \
                --count 1 \
                --instance-type t3.small \
                --key-name terraform-key \
                --security-group-ids sg-0774d975bfbbe9192 sg-0ddddce5bca8ed821 \
                --subnet-id subnet-07d7c9388862a4887 \
                --query 'Instances[0].InstanceId' \
                --output text)
echo "Instance launched with ID: $INSTANCE_ID"

aws ec2 wait instance-running --instance-ids "$INSTANCE_ID"
echo "Instance is running"

aws ec2 wait instance-status-ok --instance-ids "$INSTANCE_ID"
echo "Instance status is OK"


# -------- UPDATE DOCKER COMPOSE WITH INSTANCE IP --------
INSTANCE_IP=$(aws ec2 describe-instances \
                --instance-ids "$INSTANCE_ID" \
                --query 'Reservations[0].Instances[0].PublicIpAddress' \
                --output text)

sed "s/\[INSTANCE_IP\]/$INSTANCE_IP/g" docker-compose.yaml > docker-compose-revised.yaml
scp -i "$KEY_PATH" docker-compose-revised.yaml "ec2-user@$INSTANCE_IP:~/docker-compose.yaml"

echo "Docker-compose updated"


# ---------- INSTALL DEPENDENCIES AND RUN KAFKA ----------
ssh -i "$KEY_PATH" ec2-user@$INSTANCE_IP << 'EOF'

    sudo yum update -y
    sudo yum install -y docker
    sudo amazon-linux-extras enable selinux-ng
    sudo yum clean metadata
    sudo yum install -y selinux-policy-targeted
    sudo systemctl enable docker
    sudo systemctl start docker
    sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
    sudo docker-compose -f ~/docker-compose.yaml up -d

EOF

echo "Kafka is running"