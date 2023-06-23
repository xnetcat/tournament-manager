FROM node:slim
WORKDIR /usr/src/app
COPY . .
RUN apt-get update || : && apt-get install python3 python-pip -y
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir discord.py uvicorn fastapi bs4 requests pydantic keyboard

RUN npm run build
EXPOSE 1347
WORKDIR "/usr/src/app/frontend"
CMD ["run start"]
ENTRYPOINT ["npm"]