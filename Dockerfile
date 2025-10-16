FROM python:3.10-slim
WORKDIR /app
COPY src/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY src/ ./
# if you pre-bake a model into the image (optionnel) you can run train at build-time
# RUN python train.py
EXPOSE 5000
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]

