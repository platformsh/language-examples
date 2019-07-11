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
	"net/url"
	"sync"
)

type exampleDef struct {
	callback       func() string
	Source         string
	Name           string
	Output         string
	RenderedOutput template.HTML
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
	{{ .RenderedOutput }}
	</section>
</details>
{{ end }}

</body>
</html>
`

func exampleDefinitions() exampleList {
	exList := exampleList{}

	// The source constants are generated by `go generate` in the sources.go file.
	exList["mysql"] = &exampleDef{Name: "MySQL", callback: examples.UsageExampleMySQL, Source: mysql}
	exList["postgresql"] = &exampleDef{Name: "PostgreSQL", callback: examples.UsageExamplePostgreSQL, Source: postgresql}
	exList["solr"] = &exampleDef{Name: "Solr", callback: examples.UsageExampleSolr, Source: solr}
	exList["mongodb"] = &exampleDef{Name: "MongoDB", callback: examples.UsageExampleMongoDB, Source: mongodb}
	exList["rabbitmq"] = &exampleDef{Name: "RabbitMQ", callback: examples.UsageExampleRabbitMQ, Source: rabbitmq}
	exList["memcached"] = &exampleDef{Name: "Memcached", callback: examples.UsageExampleMemcached, Source: memcached}

	// Precompute the Output for each service, since it's not going to change.
	var wg sync.WaitGroup
	for idx, _ := range exList {
		wg.Add(1)
		serviceID := idx
		go func() {
			defer wg.Done()
			exList[serviceID].Output = exList[serviceID].callback()
			exList[serviceID].RenderedOutput = template.HTML(exList[serviceID].Output)
		}()
	}
	wg.Wait()

	return exList
}

func debug(v interface{}) {
	fmt.Printf("%+v\n", v)
}

func basePath() string {
	basePath := ""
	route, ok := Config.PshConfig.Route("golang")
	if ok {
		parsedUrl, err := url.Parse(route.Url)
		if err != nil {
			log.Fatal("Error parsing URL for base path: ", err)
		}
		basePath = parsedUrl.EscapedPath()
	}

	return basePath
}

func defineRoutes(basePath string, definitions exampleList) *gin.Engine {
	engine := gin.Default()

	group := engine.Group(basePath)

	// Compile the page template once, ahead of time.
	pageTpl, err := template.New("service").Parse(pageTemplate)
	if err != nil {
		log.Fatal("Error parsing page template", err)
	}

	// One route to show the example source.
	group.GET("/:service", func(c *gin.Context) {
		service := c.Param("service")
		c.String(http.StatusOK, definitions[service].Source)
	})

	// One route to show the service output.
	group.GET("/:service/output", func(c *gin.Context) {
		service := c.Param("service")
		c.String(http.StatusOK, definitions[service].Output)
	})

	// One route to bring them all and in a single page bind them.
	group.GET("/", func(c *gin.Context) {
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

	return engine
}

func main() {
	definitions := exampleDefinitions()
	basePath := basePath()

	ginInstance := defineRoutes(basePath, definitions)

	// Listen and Server in the port defined by Platform.sh.
	err := ginInstance.Run(":" + Config.PshConfig.Port())
	if err != nil {
		log.Fatal(err)
	}
}
