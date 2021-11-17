#!/bin/sh
# Create necessary directories for non admins to run Silhouette Studio
# Suggested from https://github.com/autopkg/joshua-d-miller-recipes and thus https://github.com/JCSmillie
# Created in recipe October 5, 2021

# Make Directories
/bin/mkdir "/Library/Application Support/com.aspexsoftware.Silhouette_Studio"
/bin/mkdir "/Library/Application Support/com.aspexsoftware.Silhouette_Studio.license"
# Give all users access
/bin/chmod -R 777 "/Library/Application Support/com.aspexsoftware.Silhouette_Studio"
/bin/chmod -R 777 "/Library/Application Support/com.aspexsoftware.Silhouette_Studio.license"
