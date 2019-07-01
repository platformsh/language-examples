//go:generate go run generators/include-source.go

package main

import (
	"fmt"
	"github.com/gin-gonic/gin"
	Config "github.com/platformsh/language-examples/conf"
	"github.com/platformsh/language-examples/examples"
	"html/template"
	"log"
	"net/http"
	"sync"
)

type exampleDef struct {
	callback func() string
	Source   string
	Name     string
	Output   string
}

// This is a map of struct pointers so that we can update it inline later in main().
type exampleList map[string]*exampleDef

const pageTemplate = `<html>
<head>
    <title>Platform.sh Go service examples</title>
    <style type="text/css">
        details {
            margin-top: 1em;
            border: 1px solid #aaa;
            border-radius: 4px;
            padding: 0.5em;
            width: 90%;
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

<h1>Service examples for Go</h1>

{{ range  .DefList }}
<details>
	<summary>{{.Name}} Sample Code</summary>
	<section>
	<h3>Source</h3>
	<pre>{{.Source}}</pre>
	</section>
	<section>
	<h3>Output</h3>
	<pre>{{.Output}}</pre>
	</section>
</details>
{{ end }}

</body>
</html>
`

func exampleDefinitions() exampleList {
	exList := exampleList{}

	// The source constants are generated by `go generate` in the sources.go file.
	exList["mysql"] = &exampleDef{Name: "MySQL", callback: examples.MySQL, Source: mysql}
	//exList["postgresql"] = exampleDef{Name: "PostgreSQL", callback: examples.Postgresql, Source: postgresql}

	// Precompute the Output for each service, since it's not going to change.
	var wg sync.WaitGroup
	for idx, _ := range exList {
		wg.Add(1)
		go func() {
			defer wg.Done()
			exList[idx].Output = exList[idx].callback()
		}()
	}
	wg.Wait()

	return exList
}

func debug(v interface{}) {
	fmt.Printf("%+v\n", v)
}

func main() {
	r := gin.Default()

	definitions := exampleDefinitions()

	// Compile the page template once, ahead of time.
	pageTpl, err := template.New("service").Parse(pageTemplate)
	if err != nil {
		log.Fatal("Error parsing page template", err)
	}

	// One route to show the example source.
	r.GET("/:service", func(c *gin.Context) {
		service := c.Param("service")
		c.String(http.StatusOK, definitions[service].Source)
	})

	// One route to show the service output.
	r.GET("/:service/output", func(c *gin.Context) {
		service := c.Param("service")
		c.String(http.StatusOK, definitions[service].Output)
	})

	// One route to bring them all and in a single page bind them.
	r.GET("/", func(c *gin.Context) {
		c.Status(http.StatusOK)
		c.Header("Content-Type", "text/html")

		page := struct {
			DefList exampleList
		}{DefList: definitions}

		err = pageTpl.Execute(c.Writer, page)
		if err != nil {
			log.Fatal("Failed rendering template: ", err)
		}
	})

	// Listen and Server in the port defined by Platform.sh.
	err = r.Run(":" + Config.PshConfig.Port())
	if err != nil {
		log.Fatal(err)
	}
}
