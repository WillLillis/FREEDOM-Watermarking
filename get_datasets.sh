#!/bin/bash

# URL of KRI dataset in question
DATA_URL="https://repository.library.northeastern.edu/downloads/neu:m044q523j?datastream_id=content"
# relative folder to download the data into once we're done...
DATA_DIR="data"

# Make sure DOWNLOAD_DIR exists...
mkdir -v -p "$DATA_DIR"

# Clean the tmp directory
printf "Cleaning out %s/tmp..." "$DATA_DIR"
if rm -rf "$DATA_DIR/tmp"; then
    printf "done\n"
else
    printf "Failed to clean %s/tmp, exiting.\n" "$DATA_DIR"
    exit 1
fi

# Download the zip 
printf "Downloading KRI-16IQImbalances-DemodulatedData...\n"

# Check for download failure
if wget "$DATA_URL" -P "$DATA_DIR/tmp"; then
    printf "Download successful.\n"
else
    printf "Download failed! Exiting.\n"
    exit 1
fi

# find the newly downloaded zip
NEW_FILE=$(find "$DATA_DIR/tmp" -type f)
if [[ -z "$NEW_FILE" ]]; then
    printf "Error! Failed to find downloaded zip file, exiting.\n"
    exit 1
else
    # Uncompress the zip
    printf "Extracting %s into %s...\n" "$NEW_FILE" "$DATA_DIR"

    if unzip "$NEW_FILE" -d "$DATA_DIR"; then
        printf "Done\n"
    else
        printf "Extraction failed, exiting.\n"
        exit 1
    fi
    printf "Cleaning up..."
    if rm -rf "$DATA_DIR/tmp"; then 
        printf "done\n"
    else
        printf "Cleanup failed! Please inspect %s/tmp\n" "$DATA_DIR"
        exit 1
    fi
fi
