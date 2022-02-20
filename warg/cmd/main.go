package main

import (
	"flag"
	"warg/config"
	"warg/controller"
)

func main() {
	configFileName := flag.String("config-file", "", "--config-file config")
	flag.Parse()
	logger := config.InitializeLogger()
	logger.Info().Msg("Loaded config file " + *configFileName)
	configuration, err := config.GetConfiguration(*configFileName)
	if err != nil {
		logger.Fatal().Msg("configuration file could not be read because of " + err.Error())
	}
	con := controller.NewController(logger, configuration)
	con.Start()
}
