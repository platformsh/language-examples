package examples

import (
  "os"
  "encoding/base64"
	"encoding/json"
)

type Credential struct {
	Scheme   string `json:"scheme"`
	Cluster  string `json:"cluster"`
	Service  string `json:"service"`
	Username string `json:"username"`
	Password string `json:"password"`
	Host     string `json:"host"`
	Path     string `json:"path"`
	Public   bool   `json:"public"`
	Fragment string `json:"fragment"`
	Ip       string `json:"ip"`
	Rel      string `json:"rel"`
	Type     string `json:"type"`
	Port     int    `json:"port"`
	Hostname string `json:"hostname"`
  Query    interface{} `json:"query"`
}

type Credentials map[string]Credential

func UsageExampleElasticsearch() string {

  relationships := os.Getenv("PLATFORM_RELATIONSHIPS")

  jsonRelationships, err := base64.StdEncoding.DecodeString(relationships)
  if err != nil {
    panic(err)
  }

  var rels Credentials

  err = json.Unmarshal([]byte(jsonRelationships), &rels)
  if err != nil {
    panic(err)
  }

  credentials := rels["elasticsearch"]

  return credentials.Host

}
