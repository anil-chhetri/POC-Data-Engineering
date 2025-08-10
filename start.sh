#!/usr/bin/env bash
set -e  # Exit immediately if a command fails

VENV_PATH="./dbt/.venv"

# Install uv (if not already installed)
if ! command -v uv &> /dev/null; then
    echo "Installing uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.cargo/bin:$PATH"
else
    echo "uv is already installed."
fi

# Create virtual environment if it doesn't exist
if [ ! -d "$VENV_PATH" ]; then
    echo "Creating virtual environment at $VENV_PATH..."
    uv venv "$VENV_PATH"
else
    echo "Virtual environment already exists at $VENV_PATH."
fi

# Activate virtual environment
echo "Activating virtual environment..."
source "$VENV_PATH/bin/activate"

# Install dbt-core and dbt-duckdb
echo "Installing dbt-core and dbt-duckdb..."
uv pip install dbt-core dbt-duckdb dbt-postgres

# Install DuckDB CLI
if ! command -v duckdb &> /dev/null; then
    echo "Installing DuckDB CLI..."
    curl https://install.duckdb.org | sh
    export PATH="$HOME/.duckdb/bin:$PATH"  # Add to PATH if the installer uses this directory
else
    echo "DuckDB CLI is already installed."
fi


# Start Docker containers
echo "Starting Docker containers..."
docker compose -f docker-compose.yml up -d --build --wait

# Update bash prompt
echo "Updating bash prompt..."
if ! grep -q 'export PS1="\\W> "' ~/.bashrc; then
    echo "export PS1=\"\\W> \"" >> ~/.bashrc
fi

# Start SSH service in container
echo "Starting SSH service in 'playground' container..."
docker exec playground service ssh start

# Check SSH service status
echo "Checking SSH service status in 'playground' container..."
docker exec playground service ssh status

echo "Setup complete!"
echo "Activate your environment manually with: source $VENV_PATH/bin/activate"
