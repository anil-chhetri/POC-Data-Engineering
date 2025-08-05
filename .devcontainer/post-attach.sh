# Run start.sh
if [ -f "./start.sh" ]; then
    echo "Running start.sh..."
    bash ./start.sh
else
    echo "Warning: start.sh not found, skipping..."
fi