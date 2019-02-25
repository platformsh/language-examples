const express = require('express');
const router = express.Router();

function index() {
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
}


router.get('/', index);

router.get('/:service', (req, res) => {

    let options = {
        root: __dirname + '/examples/',
        dotfiles: 'deny',
        headers: {
            'Content-Type': 'text/plain',
        }
    };

    res.sendFile(`${req.params.service}.js`, options);
});

router.get('/:service/output', (req, res) => {

});

module.exports = router;
