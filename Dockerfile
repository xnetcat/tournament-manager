FROM python:3
WORKDIR /usr/src/app
COPY . .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir discord.py uvicorn fastapi bs4 requests pydantic keyboard

EXPOSE 1347
CMD ["frontend/main.py"]
ENTRYPOINT ["python3"]