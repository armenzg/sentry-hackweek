FROM python:3.8.10-slim

ENV PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app
# Re-create the requirements layer if the requirements change
COPY requirements.txt /app/
RUN pip install wheel
RUN pip install gunicorn==20.1.0
RUN pip install -r requirements.txt

# Source code
COPY src/ /app/src/

# 1 worker, 4 worker threads should be more than enough.
# --worker-class gthread is automatically set if --threads > 1.

# In my experience this configuration hovers around 100 MB
# baseline (noop app code) memory usage in Cloud Run.

# --timeout 0 disables gunicorn's automatic worker restarting.
# "Workers silent for more than this many seconds are killed and restarted."

# If things get bad you might want to --max-requests, --max-requests-jitter, --workers 2.
CMD ["gunicorn", "--bind", ":8080", "--workers", "1", "--threads", "4", "--timeout", "0", "src.main:app"]