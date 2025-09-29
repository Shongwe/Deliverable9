# Base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy project files
COPY . /app

# Install dependencies
RUN pip install --upgrade pip && \
    pip install pandas numpy scikit-learn matplotlib joblib

# Optional: expose port if you plan to stream alerts
EXPOSE 8080

# Entry point
CMD ["python", "train.py"]