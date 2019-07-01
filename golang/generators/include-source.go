package main

import (
	"bytes"
	"io"
	"io/ioutil"
	"log"
	"os"
	"path/filepath"
	"strings"
)

const (
	sourceDirectory = "examples"
	backTick        = "\\x60"
	outputFile      = "sources.go"
)

type debacktickWriter struct {
	writer io.Writer
}

func (dw *debacktickWriter) Write(buf []byte) (int, error) {
	_, err := dw.writer.Write(bytes.ReplaceAll(buf, []byte("`"), []byte(backTick)))
	return len(buf), err
}

// Reads all .go files in the examples/ folder
// and encodes them as strings literals in sources.go.
func main() {
	fs, _ := ioutil.ReadDir(sourceDirectory)
	out, _ := os.Create(outputFile)
	outFilterBacktick := &debacktickWriter{writer: out}
	_, err := out.Write([]byte("package main \n\nconst (\n"))
	if err != nil {
		log.Fatal("Writing header failed: ", err)
	}
	for _, file := range fs {
		if strings.HasSuffix(file.Name(), ".go") {
			_, err := out.Write([]byte(strings.TrimSuffix(file.Name(), ".go") + " = `"))
			if err != nil {
				log.Fatal("Writing line prefix failed: ", err)
			}
			inputFileStream, err := os.Open(filepath.Join(sourceDirectory, file.Name()))
			if err != nil {
				log.Fatal("Opening inputFileStream failed: ", err)
			}
			_, err = io.Copy(outFilterBacktick, inputFileStream)
			if err != nil {
				log.Fatal("Writing inputFileStream content failed: ", err)
			}
			_, err = out.Write([]byte("`\n"))
			if err != nil {
				log.Fatal("Writing header failed", err)
			}
			_ = inputFileStream.Close()
		}
	}
	_, _ = outFilterBacktick.Write([]byte(")\n"))
}
