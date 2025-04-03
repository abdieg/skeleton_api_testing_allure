# Automatically stop and delete old container to create and run the new one
docker rm -f skeleton_api_testing 2>/dev/null || true && \
docker run -d --name skeleton_api_testing --network skeleton_api_skeleton_api skeleton_api_testing
