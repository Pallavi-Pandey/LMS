#!/bin/sh

# Run the seeding script
echo "Seeding initial data..."
python upload_initial_data.py

# Start the application
echo "Starting Flask app..."
exec flask run --host=0.0.0.0 --port=5000
