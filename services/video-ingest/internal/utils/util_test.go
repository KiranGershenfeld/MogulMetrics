package utils

import (
	"testing"
	"time"
)

func TestParseTime(t *testing.T) {
	testCases := []struct {
		name     string
		input    string
		expected *time.Time
		wantErr  bool
	}{
		{
			name:  "Valid time string",
			input: "2024-02-10T02:00:31+00:00",
			expected: func() *time.Time {
				t, _ := time.Parse(time.RFC3339Nano, "2024-02-10T02:00:31+00:00")
				return &t
			}(),
			wantErr: false,
		},
		{
			name:    "Invalid time string",
			input:   "invalid time",
			wantErr: true,
		},
		// Add more test cases as needed
	}

	for _, tc := range testCases {
		t.Run(tc.name, func(t *testing.T) {
			got, err := ParseTime(tc.input)

			if (err != nil) != tc.wantErr {
				t.Errorf("parseTime() error = %v, wantErr %v", err, tc.wantErr)
				return
			}

			if !tc.wantErr && got.String() != tc.expected.String() {
				t.Errorf("parseTime() = %v, want %v", got, tc.expected)
			}
		})
	}
}
