FROM node:18

WORKDIR /app

COPY package*.json ./
RUN npm install
RUN npm install socket.io-client chart.js react-chartjs-2

COPY . .

EXPOSE 3000

CMD ["npm", "start", "--", "--host", "0.0.0.0"]