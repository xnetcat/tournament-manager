FROM node:slim
WORKDIR /usr/src/app
COPY . .
RUN apt-get update || : && apt-get install python3 python3-pip -y
RUN pip install pyinstaller

WORKDIR "/usr/src/app/frontend"
RUN npm install
RUN npm run build
EXPOSE 1347
CMD ["run start"]
ENTRYPOINT ["npm"]