FROM python:3
WORKDIR /usr/src/app
COPY . .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir uvicorn fastapi bs4 requests pydantic keyboard pyinstaller

EXPOSE 1347
CMD ["server.py"]
ENTRYPOINT ["python3"]