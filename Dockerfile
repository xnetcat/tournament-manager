FROM python:3
WORKDIR /usr/src/app
COPY . .
RUN apt-get update || : && apt-get install nodejs npm -y
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir discord.py uvicorn fastapi bs4 requests pydantic keyboard pyinstaller

WORKDIR "/usr/src/app/frontend"
RUN npm install
RUN npm run build
EXPOSE 1347
ENTRYPOINT ["npm run start"]