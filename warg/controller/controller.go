package controller

import (
	"fmt"
	"github.com/rs/zerolog"
)
import "warg/config"

type controller struct {
	logger        zerolog.Logger
	configuration config.Config
}

func (c controller) Start() {
	fmt.Println(c.configuration.Mongo.Port)
}

func NewController(logger zerolog.Logger, configuration *config.Config) *controller {
	logger.Info().Msg("Initializing controller")
	return &controller{logger: logger, configuration: *configuration}
}
