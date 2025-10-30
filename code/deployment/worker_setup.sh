#!/bin/bash
set -e

LOG_FILE="/var/log/worker_setup.log"

# Redirect all output (stdout and stderr) to the log file
exec > >(tee -a "$LOG_FILE") 2>&1

echo "======================================="
echo "Starting Worker setup"
echo "Date: $(date)"
echo "======================================="

# Variables
PROJECT_DIR="/home/ec2-user"
REPO_URL="https://github.com/miguelxsm/Advanced-Concepts-Of-Cloud-Computing-2.git"

# Update system and install dependencies
echo "Updating system and installing dependencies..."
sudo yum update -y
sudo yum install -y docker awscli git

# Enable and start Docker service
echo "Starting Docker..."
sudo systemctl enable docker
sudo systemctl start docker
sudo usermod -aG docker ec2-user

# Wait a few seconds to ensure Docker is ready
sleep 5

# Clone the repository
cd /home/ec2-user
if [ -d "Advanced-Concepts-Of-Cloud-Computing-2" ]; then
    echo "Repository already exists, removing to reclone..."
    sudo rm -rf Advanced-Concepts-Of-Cloud-Computing-2
fi

echo "Cloning repository from GitHub..."
sudo git clone  "$REPO_URL"
if [ $? -ne 0 ]; then
    echo "Error: Failed to clone repository from $REPO_URL"
    exit 1
fi
echo "Repository cloned successfully."

# Navigate to the code directory
cd Advanced-Concepts-Of-Cloud-Computing-2/code

# Verify docker-compose file exists
if [ ! -f "deployment/docker-compose.worker.yml" ]; then
    echo "Error: deployment/docker-compose.worker.yml file not found"
    exit 1
fi

# Install Docker Compose if not available
if ! docker compose version >/dev/null 2>&1; then
    echo "Installing Docker Compose plugin..."
    sudo mkdir -p /usr/local/lib/docker/cli-plugins
    sudo curl -SL "https://github.com/docker/compose/releases/latest/download/docker-compose-linux-$(uname -m)" \
        -o /usr/local/lib/docker/cli-plugins/docker-compose
    sudo chmod +x /usr/local/lib/docker/cli-plugins/docker-compose
    echo "Docker Compose installed successfully."
fi

# Install Docker Buildx (required for docker compose build)
echo "Installing Docker Buildx (≥0.17 required for compose build)..."
BUILDX_VERSION="0.17.1"
sudo curl -LO "https://github.com/docker/buildx/releases/download/v${BUILDX_VERSION}/buildx-v${BUILDX_VERSION}.linux-amd64"
sudo mkdir -p /usr/local/lib/docker/cli-plugins
sudo mv "buildx-v${BUILDX_VERSION}.linux-amd64" /usr/local/lib/docker/cli-plugins/docker-buildx
sudo chmod +x /usr/local/lib/docker/cli-plugins/docker-buildx
echo "Buildx installed successfully: $(docker buildx version)"

# Build and start worker containers
echo "Building and starting worker containers..."
sudo -u ec2-user bash <<EOF
cd /home/ec2-user/Advanced-Concepts-Of-Cloud-Computing-2/code
docker compose -f deployment/docker-compose.worker.yml up -d
EOF

# Finish
echo "Worker configured successfully and running."
echo "Completed at: $(date)"
echo "======================================="
