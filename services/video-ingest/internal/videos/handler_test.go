package videos

import (
	"encoding/xml"
	"reflect"
	"testing"
)

func TestHandleXML(t *testing.T) {
	testCases := []struct {
		name     string
		input    string
		expected Feed
		wantErr  bool
	}{
		{
			name: "Valid time string",
			input: `<?xml version='1.0' encoding='UTF-8'?>
			<feed xmlns:yt="http://www.youtube.com/xml/schemas/2015" xmlns="http://www.w3.org/2005/Atom"><link rel="hub" href="https://pubsubhubbub.appspot.com"/><link rel="self" href="https://www.youtube.com/xml/feeds/videos.xml?channel_id=UCaYxyR9mzVlTrOOyZD0XAmA"/><title>YouTube video feed</title><updated>2024-02-10T02:00:37.417148436+00:00</updated><entry>
			  <id>yt:video:nL7rNmAT7Dc</id>
			  <yt:videoId>nL7rNmAT7Dc</yt:videoId>
			  <yt:channelId>UCaYxyR9mzVlTrOOyZD0XAmA</yt:channelId>
			  <title>The Super Bowl Limiteds are INSANE!</title>
			  <link rel="alternate" href="https://www.youtube.com/watch?v=nL7rNmAT7Dc"/>
			  <author>
			   <name>MMG</name>
			   <uri>https://www.youtube.com/channel/UCaYxyR9mzVlTrOOyZD0XAmA</uri>
			  </author>
			  <published>2024-02-10T02:00:31+00:00</published>
			  <updated>2024-02-10T02:00:37.417148436+00:00</updated>
			 </entry></feed>`,
			expected: Feed{
				XMLName: xml.Name{
					Space: "http://www.w3.org/2005/Atom",
					Local: "feed",
				},
				Link: []Link{
					{
						Rel:  "hub",
						Href: "https://pubsubhubbub.appspot.com",
					},
					{
						Rel:  "self",
						Href: "https://www.youtube.com/xml/feeds/videos.xml?channel_id=UCaYxyR9mzVlTrOOyZD0XAmA",
					},
				},
				Title:   "YouTube video feed",
				Updated: "2024-02-10T02:00:37.417148436+00:00",
				Entry: Entry{
					ID:        "yt:video:nL7rNmAT7Dc",
					YoutubeID: "nL7rNmAT7Dc",
					ChannelID: "UCaYxyR9mzVlTrOOyZD0XAmA",
					Title:     "The Super Bowl Limiteds are INSANE!",
					Link: Link{
						Rel:  "alternate",
						Href: "https://www.youtube.com/watch?v=nL7rNmAT7Dc",
					},
					Author: Author{
						Name: "MMG",
						URI:  "https://www.youtube.com/channel/UCaYxyR9mzVlTrOOyZD0XAmA",
					},
					Published: "2024-02-10T02:00:31+00:00",
					Updated:   "2024-02-10T02:00:37.417148436+00:00",
				},
			},
			wantErr: false,
		},
		// Add more test cases as needed
	}

	for _, tc := range testCases {
		t.Run(tc.name, func(t *testing.T) {
			var got Feed
			if err := xml.Unmarshal([]byte(tc.input), &got); err != nil && !tc.wantErr {
				t.Errorf("Could not unmarshal xml to feed: %v", err)
			}

			// if (err != nil) != tc.wantErr {
			// 	t.Errorf("parseTime() error = %v, wantErr %v", err, tc.wantErr)
			// 	return
			// }

			if !tc.wantErr && !reflect.DeepEqual(got, tc.expected) {
				t.Errorf("got %v, want %v", got, tc.expected)
			}
		})
	}
}
