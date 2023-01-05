FROM python:3.9-slim-buster

ENV PYTHONUNBUFFERED=1

RUN mkdir app

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt \
&& apt update \
&& apt install poppler-utils -y

# FROM python:3.9-slim-buster as production

# ENV PYTHONUNBUFFERED=1

# RUN mkdir app

# WORKDIR /app

# COPY --from=builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages/
# COPY --from=builder /app /app/

# RUN 

CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8080"]