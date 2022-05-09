const fs = require('fs');
const key = fs.readFileSync('./auths/key.pem');
const cert = fs.readFileSync('./auths/cert.pem');
const express = require('express');
const request = require('request');
const https = require('https');
const app = express();
const server = https.createServer({key: key, cert: cert }, app);

app.enable('trust proxy')
app.use(function(request, response, next) {

    if (process.env.NODE_ENV !== 'development' && !request.secure) {
       return response.redirect("https://" + request.headers.host + request.url);
    }

    next();
})

app.use(express.static('public'))
app.get('/', (req, res) => { res.send('this is an secure server') });
server.listen(443, () => { console.log('listening on 443') });
