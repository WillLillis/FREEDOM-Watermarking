#!/bin/bash

# URL of KRI dataset in question
DATA_URL="https://repository.library.northeastern.edu/downloads/neu:m044q523j?datastream_id=content"
# relative folder to download the data into once we're done...
DATA_DIR="data"

# Make sure DOWNLOAD_DIR exists...
mkdir -v -p "$DATA_DIR"

# Clean the tmp directory
echo -n "Cleaning out $DATA_DIR/tmp..."
if rm -rf "$DATA_DIR/tmp"; then
    echo "done"
else
    echo "Failed to clean $DATA_DIR/tmp, exiting"
    exit 1
fi

# Download the zip 
echo -n "Downloading KRI-16IQImbalances-DemodulatedData..."

# Check for download failure
if wget "$DATA_URL" -P "$DATA_DIR/tmp"; then
    echo "Download successful."
else 
    echo "Download failed! Exiting"
    exit 1
fi

# find the newly downloaded zip
NEW_FILE=$(find "$DATA_DIR/tmp" -type f)
if [[ -z "$NEW_FILE" ]]; then
    echo "Error! Failed to find downloaded zip file, exiting"
    exit 1
else
    # Uncompress the zip
    echo "Extracting $NEW_FILE into $DATA_DIR..."

    if unzip "$NEW_FILE" -d "$DATA_DIR"; then
        echo "done"
    else
        echo "Extraction failed, exiting"
        exit 1
    fi
    echo -n "Cleaning up..."
    if rm -rf "$DATA_DIR/tmp"; then 
        echo "done"
    else
        echo "Cleanup failed! Please inspect $DATA_DIR/tmp"
        exit 1
    fi
fi
