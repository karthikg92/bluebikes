var http=require('http')
var fs = require('fs')

var server=http.createServer((function(request,response)
{
	if(request.url === "/index_server"){
   fs.readFile("index_server.html", function (err, data) {
      response.writeHead(200, {'Content-Type': 'text/html'});
      response.write(data);
      response.end();
   });
}

else {
   response.writeHead(200, {'Content-Type': 'text/html'});
   response.write('<b>Hey there!</b><br /><br />This is the default response. Requested URL is: ' + request.url);
   response.end();
}
}));
server.listen(8080);