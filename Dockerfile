FROM python:3.12-slim


# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy application code
COPY . .

# Create history directory inside the container
RUN mkdir -p /app/history

# Default command
CMD ["python", "run.py"]