#!/bin/bash

# Path to the file containing the list of URLs and texts to check
URLS_FILE="urls.txt"
# Email address to send notifications to
EMAIL="karthickoncloud@gmail.com"
# Subject for the email notifications
SUBJECT="Website Down Notification"

# Function to check webpage content
check_website() {
    local url=$1
    local text=$2
    response=$(curl -s "$url")

    if echo "$response" | grep -q "$text"; then
        echo "$(date): $url is up"
    else
        echo "$(date): $url is down or the text '$text' was not found"
        echo "$url is down or the text '$text' was not found on $(date)" | mail -s "$SUBJECT" "$EMAIL"
    fi
}

# Infinite loop to monitor websites
while true; do
    if [ -f "$URLS_FILE" ]; then
        # Read URLs and texts from file
        while IFS=, read -r url text; do
            check_website "$url" "$text"
        done < "$URLS_FILE"
    else
        echo "$(date): URLs file not found"
    fi
    # Sleep for 60 seconds before checking again
    sleep 60
done

