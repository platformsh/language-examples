const http = require('http');
const config = require("platformsh").config();
const fs = require('fs');

var data = {};

// @todo Do this for all services.
data.MongoDB = require('./examples/MongoDB.js');
data.MongoDB.source = fs.readFileSync('./examples/MongoDB.js');

// Call all of the run() methods of all services, and store their output once.
const runData = async function(key) {
  let value = undefined;
  try{
    const method = data[key].run;
    value = await method();
  } catch (err) {
    console.error(err);
  }
  if (value) {
    data[key].output = value;
  }
};
// array of Promise<void>
const promises = Object.keys(data).map(runData);

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
    <style type="text/css">
        details {
            margin-top: 1em;
            border: 1px solid #aaa;
            border-radius: 4px;
            padding: 0.5em;
            wdith: 90%;
        }

        summary {
            font-weight: bold;
            margin: -.5em -.5em 0;
            padding: .5em;
        }

        details[open] {
            padding: .5em;
        }

        details[open] summary {
            border-bottom: 1px solid #aaa;
            margin-bottom: .5em;
        }

        table, table td, table th {
            border: 1px solid black;
        }
    </style>
</head>
<body>
<h1>Service examples for Node.js</h1>
`);

  Object.keys(data).forEach ((key) => {
     let name = key;
    response.write(`<details>
      <summary>${name} Sample Code</summary>
      <section>
      <h3>Source</h3>
      <pre>${data[key].source}</pre>
      </section>
      <section>
      <h3>Output</h3>
      ${data[key].output}
      </section>
      </details>
      `);
  });

  response.end(`</body></html>`);
});

server.listen(config.port);
