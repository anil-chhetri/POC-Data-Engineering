FROM python:3.13-slim

WORKDIR .

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install OpenSSH server
RUN apt-get update && apt-get install -y openssh-server

# Create an SSH directory for the root user

# Copy the authorized keys (assuming you place it in the context)
COPY id_rsa.pub /root/.ssh/authorized_keys

# Set permissions for SSH directory and keys
RUN chmod 700 /root/.ssh && chmod 600 /root/.ssh/authorized_keys

# Start the SSH server
RUN service ssh start

# Expose the SSH port
EXPOSE 22


CMD ["bash", "-c", "service ssh start && tail -f /dev/null"]