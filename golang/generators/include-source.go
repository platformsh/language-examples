package main

import (
	"bytes"
	"errors"
	"io"
	"io/ioutil"
	"log"
	"os"
	"path/filepath"
	"strings"
)

const (
	sourceDirectory = "examples"
	outputFile      = "sources.go"
)

type noBacktickWriter struct {
	writer io.Writer
}

func (dw *noBacktickWriter) Write(buf []byte) (int, error) {
	if bytes.ContainsRune(buf, '`') {
		return 0, errors.New("source must not contains backtick, as golang does not allow to escape nested backticks in multiline strings. Use newlines and string concatenation instead")
	}

	_, err := dw.writer.Write(buf)
	return len(buf), err
}

// Reads all .go files in the examples/ folder
// and encodes them as strings literals in sources.go.
func main() {
	fs, _ := ioutil.ReadDir(sourceDirectory)
	out, _ := os.Create(outputFile)
	outFilterBacktick := &noBacktickWriter{writer: out}
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
				log.Fatalf("Writing inputFileStream content failed for file %q: %v.", file.Name(), err)
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
