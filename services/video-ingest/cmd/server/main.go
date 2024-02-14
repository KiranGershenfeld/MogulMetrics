package main

import (
	"log"
	"os"

	"github.com/spf13/cobra"
)

var configFile string

var rootCmd = &cobra.Command{
	Use:  "",
	Long: "Root cmd",
	Run: func(cmd *cobra.Command, args []string) {
		runApplication()
	},
}

func init() {
	rootCmd.AddCommand(serverCmd)
	rootCmd.AddCommand(channelCmd)
	channelCmd.AddCommand(addChannelCmd)

	addChannelCmd.Flags().String("channel_id", "", "Channel ID")
	addChannelCmd.Flags().String("channel_name", "", "Channel Name")
	addChannelCmd.Flags().Bool("subscribe", false, "Subscribe")
	addChannelCmd.Flags().Int("subscriberCount", 0, "Subscriber Count")

	rootCmd.PersistentFlags().StringVarP(&configFile, "conf", "", "", "config file path")
}

func main() {
	if err := rootCmd.Execute(); err != nil {
		log.Printf("failed to execute command. err: %v", err)
		os.Exit(1)
	}
}
