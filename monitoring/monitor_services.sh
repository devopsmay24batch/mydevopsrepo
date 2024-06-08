#!/bin/bash

# Path to the file containing the list of services
SERVICES_FILE="services.txt"
# Email address to send notifications to
EMAIL="your_email@example.com"
# Subject for the email notifications
SUBJECT="Service Down Notification"

# Function to check service status
check_service() {
    local service=$1
    if systemctl is-active --quiet "$service"; then
        echo "$(date): $service is up"
    else
        echo "$(date): $service is down"
        echo "$service is down on $(date)" | mail -s "$SUBJECT" "$EMAIL"
    fi
}

# Infinite loop to monitor services
while true; do
    if [ -f "$SERVICES_FILE" ]; then
        # Read services from file
        SERVICES=($(cat "$SERVICES_FILE"))
        
        for service in "${SERVICES[@]}"; do
            check_service "$service"
        done
    else
        echo "$(date): Services file not found"
    fi
    # Sleep for 60 seconds before checking again
    sleep 60
done

