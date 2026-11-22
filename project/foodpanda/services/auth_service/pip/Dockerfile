# Stage 1: Build stage with build dependencies for speed, consistency, and smaller final images
# Official lightweight Python 3.11 image as the base for building dependencies.
FROM python:3.11-slim as builder

# Set the working directory inside the container. Any COPY, RUN, CMD after this will run from /usr/src/app.
WORKDIR /usr/src/app

# Prevent Python from creating .pyc files (saves space).
ENV PYTHONDONTWRITEBYTECODE 1

# Ensure logs are written directly to stdout/stderr (important for Docker logging).
ENV PYTHONUNBUFFERED 1

COPY requirements.txt .

# Caching the wheels
# --mount=type=cache Uses Docker BuildKit’s cache mount feature.
# target=/root/.cache/pip inside the container, and persist it across builds.

# Install dependencies in wheel format (prebuilt, binary distribution format for Python packages)
# pip wheel Instead of installing packages directly, this command builds wheel files (.whl).
# --no-deps Do not automatically install dependencies of the listed packages.
#--wheel-dir  Specifies where to place the generated .whl files.
#-r requirements.txt Tells pip to read package names and versions from the requirements.txt file.
RUN --mount=type=cache,target=/root/.cache/pip \
    pip wheel -r requirements.txt --wheel-dir /usr/src/app/wheels \


# Stage 2: Final production stage
# Start a fresh, clean image (without compilers/build tools). This ensures the final image is much smaller.
FROM python:3.11-slim

WORKDIR /usr/src/app

# Copy pre-built wheels from the builder stage
COPY --from=builder /usr/src/app/wheels /wheels
RUN pip install --no-cache /wheels/*

# Delete /wheels to keep the image small.
RUN rm -rf /wheels

# Copy application code
COPY ./app /usr/src/app

EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]