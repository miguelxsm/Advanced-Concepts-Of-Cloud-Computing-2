# Builder stage: install all dependencies
FROM python:3.12-slim AS builder

WORKDIR /app

COPY requirements.txt .

# Install CPU-only PyTorch to keep image small
RUN pip install --no-cache-dir --index-url https://download.pytorch.org/whl/cpu \
    torch torchvision torchaudio && \
    pip install --no-cache-dir -r requirements.txt && \
    pip cache purge && \
    rm -rf /root/.cache/pip /tmp/* /var/lib/apt/lists/*

COPY app.py .

# Runtime stage: minimal final image
FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1
ENV PATH="/home/app/.local/bin:$PATH"
WORKDIR /app

# Copy only needed runtime dependencies from builder
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy app separately since files don't persist between stages
COPY app.py .

RUN ldconfig /usr/local/lib

EXPOSE 5000
CMD ["python", "app.py"]