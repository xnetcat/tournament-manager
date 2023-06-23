FROM python:3
WORKDIR /usr/src/app
COPY . .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir discord.py uvicorn fastapi bs4 requests pydantic keyboard

CMD ["main.py"]
ENTRYPOINT ["python3"]