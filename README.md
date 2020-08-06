To run type `docker-compose up -d --build` <br>
by default service can be accessed at port 8947 (nginx),<br>
but port and other settings regarding application and docker <br>
configuration can be changed in `.env` file<br><br>

If build can't download packages and you are behind proxy <br>
try adding proxy to `app/Dockerfile`<br>
`ENV HTTP_PROXY http://address:port` <br>
`ENV HTTPS_PROXY http://address:port`
