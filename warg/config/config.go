package config

import (
	"github.com/rs/zerolog"
	"github.com/spf13/viper"
	"os"
	"strings"
)

type Mongo struct {
	Host string //`validate: "required"`
	Port int32  //`validate: "required,lte=54000"`
}

type Config struct {
	Mongo Mongo
}

func GetConfiguration(configFilepath string) (*Config, error) {
	if len(configFilepath) > 0 {
		viper.SetConfigFile(configFilepath)
	}
	viper.SetEnvKeyReplacer(strings.NewReplacer(".", "_"))
	viper.SetDefault("MONGO.HOST", "mongodb")
	viper.SetDefault("MONGO.PORT", 27017)
	viper.AutomaticEnv()
	err := viper.ReadInConfig()
	if err != nil {
		_, ok := err.(viper.ConfigFileNotFoundError)
		if !ok {
			return nil, err
		}
	}
	config := &Config{}
	err = viper.Unmarshal(&config)
	if err != nil {
		return nil, err
	}
	return config, nil
}

func InitializeLogger() zerolog.Logger {
	logger := zerolog.New(os.Stdout)
	return logger
}
