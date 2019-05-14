package config

import (
	"fmt"
	"os"
	"path"

	"github.com/BurntSushi/toml"
	log "github.com/google/logger"
)

// Config The configuration parameters required for running app
type Config struct {
	// HTTP Server configs
	Port int

	// Static Data configs
	BaseDir              string
	HTMLDir              string
	TemplateDir          string
	DataDir              string
	CatalogueMetadataDir string

	// Environment
	Environment string
}

var config Config

// GetConfig Return the Config
func GetConfig() *Config {
	return &config
}

func (c *Config) toString() string {
	return fmt.Sprintf("Port: %d, BaseDir: %s, HTMLDir: %s, TemplateDir: %s, "+
		"DataDir: %s",
		c.Port, c.BaseDir, c.HTMLDir, c.TemplateDir, c.DataDir)
}

// InitConfig Initializes the config
func InitConfig(configFile string) {
	_, err := os.Stat(configFile)
	if err != nil {
		log.Fatal("Couldn't find config file: ", err.Error())
	}

	var environmentConfig map[string]Config
	_, err1 := toml.DecodeFile(configFile, &environmentConfig)
	if err1 != nil {
		log.Fatal("Couldn't parse config file: ", err1.Error())
	}

	if os.Getenv("JAIN_CATALOGUE_ENVIRONMENT") != "" {
		config = environmentConfig["production"]
		config.Environment = "production"
	} else {
		config = environmentConfig["development"]
		config.Environment = "development"
	}
	// Reinitialize BaseDir by appending GOPATH
	goPath := os.Getenv("GOPATH")
	config.BaseDir = path.Join(goPath, config.BaseDir)
	config.HTMLDir = path.Join(config.BaseDir, config.HTMLDir)
	config.TemplateDir = path.Join(config.BaseDir, config.TemplateDir)
	log.Info(config.toString())
}
