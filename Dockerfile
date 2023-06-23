FROM node:slim
WORKDIR /usr/src/app
COPY . .
RUN apt-get update || : && apt-get install python3 pyinstaller -y
WORKDIR "/usr/src/app/frontend"
RUN npm install
RUN npm run build
EXPOSE 1347
CMD ["run start"]
ENTRYPOINT ["npm"]