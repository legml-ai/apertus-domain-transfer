FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY src/ src/
COPY results/ results/
ENV RESULTS_DIR=/app/results
ENTRYPOINT ["python", "-u", "src/evaluate.py"]
