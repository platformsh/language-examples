const http = require('http');
const config = require("platformsh").config();
const fs = require('fs');

var data = {};

// @todo Do this for all services.
data.MongoDB = require('./examples/MongoDB.js');
data.MongoDB.source = fs.readFileSync('./examples/MongoDB.js');

// Call all of the run() methods of all services, and store their output once.
const promises = Object.keys(data).map(async (key) => { data[key].output = await data[key].run(); });

var server = http.createServer(async function (request, response) {
  try {
    await Promise.all(promises);
  }
  catch (error) {
    console.error(error);
  }

  response.writeHead(200, {"Content-Type": "text/html"});

  response.write(`<html>
<head>
<title>Platform.sh Node.js service examples</title>
</head>
<body>
<h1>Service examples for Node.js</h1>
`);

  Object.keys(data).forEach (function (key) {
     let name = key;
    response.write(`<details>
      <summary>${name} Sample Code</summary>    
      <section>
      <h3>Source</h3>
      ${data[key].source}
      </section>
      <section>
      <h3>Output</h3>
      ${data[key].output}
      </section>
      <section>
      <h3>Relationship</h3>
      <pre>${data[key].relationship()}</pre>
      </section>
      </details>
      `);
  });

  response.end(`</body></html>`);
});

server.listen(config.port);
