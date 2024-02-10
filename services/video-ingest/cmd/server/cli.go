package main

import (
	"fmt"
	"video-ingest/internal/channels"
	channelDB "video-ingest/internal/channels/database"

	"video-ingest/internal/config"
	"video-ingest/internal/database"

	"github.com/spf13/cobra"
)

var channelCmd = &cobra.Command{
	Use:   "channel",
	Short: "Manage channels",
	Run:   runChannelManager,
}

var addChannelCmd = &cobra.Command{
	Use:   "add",
	Short: "Add a channel",
	Run: func(cmd *cobra.Command, args []string) {
		runChannelManager(cmd, args)
	},
}

func runChannelManager(cmd *cobra.Command, args []string) {
	channelID, err := cmd.Flags().GetString("channel_id")
	channelName, err := cmd.Flags().GetString("channel_name")
	subscribe, err := cmd.Flags().GetBool("subscribe")
	subscriberCount, err := cmd.Flags().GetInt("subscriberCount")

	if err != nil {
		fmt.Println(err)
		return
	}

	conf, err := config.Load(configFile)
	if err != nil {
		fmt.Println(err)
		return
	}

	db, err := database.NewDatabase(conf)
	if err != nil {
		fmt.Println(err)
		return
	}

	channelDB := channelDB.NewChannelDB(db)
	handler := channels.NewHandler(conf, channelDB)
	handler.AddChannel(channelID, channelName, subscribe, subscriberCount)
}
