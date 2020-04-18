FROM node:10

WORKDIR /opt/app

ADD public /opt/app/public
ADD src /opt/app/src
ADD package.json /opt/app
ADD yarn.lock /opt/app

RUN yarn install

EXPOSE 3000

ENTRYPOINT ["yarn", "start"]
