package main

import (
	"flag"

	"github.com/aadhyatm/jaincatalogue/config"
	"github.com/aadhyatm/jaincatalogue/http"
	"github.com/aadhyatm/jaincatalogue/index"
	log "github.com/google/logger"

	"io/ioutil"
	"os"
	"path"
)

func main() {
	flag.Parse()

	// Initailize Logging
	logDir := os.Getenv("LOG_DIR")
	if logDir != "" {
		logPath := path.Join(logDir, "jaincatalogue.log")
		lf, err := os.OpenFile(logPath, os.O_CREATE|os.O_WRONLY|os.O_APPEND, 0660)
		if err != nil {
			log.Fatalf("Failed to open log file: %v", err)
		}
		defer lf.Close()
		// Log to system log and a log file, Info logs don't write to stdout.
		loggerOne := log.Init("JainCatalogue", false, true, lf)
		defer loggerOne.Close()
	} else {
		loggerOne := log.Init("JainCatalogue", true, false, ioutil.Discard)
		defer loggerOne.Close()
	}

	// Config file is present in the same directory as the binary
	configFileLoc := os.Getenv("JAIN_CATALOGUE_CONFIG_FILE")
	if configFileLoc == "" {
		configFileLoc = "config/config.toml"
	}
	config.InitConfig(configFileLoc)

	// Initialize index
	index.InitIndex()

	// Initialize HTTP Server
	http.InitHTTPServer()

	http.StartHTTPServer()
}
