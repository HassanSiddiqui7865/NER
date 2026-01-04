FROM python:3.9-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Upgrade pip first
RUN pip install --upgrade pip

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Install MED7 vector-based (large) model from Hugging Face
# Download and rename the wheel file to avoid version parsing issues
RUN python -c "import urllib.request; urllib.request.urlretrieve('https://huggingface.co/kormilitzin/en_core_med7_lg/resolve/main/en_core_med7_lg-any-py3-none-any.whl', '/tmp/en_core_med7_lg.whl')" && \
    pip install /tmp/en_core_med7_lg.whl && \
    rm /tmp/en_core_med7_lg.whl

# Copy application code
COPY app.py /app/

# Expose port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
