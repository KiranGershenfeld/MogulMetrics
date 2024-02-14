package utils

import "time"

func ParseTime(str string) (parsed *time.Time, err error) {
	t, err := time.Parse(time.RFC3339Nano, str)
	if err != nil {
		return nil, err
	}
	return &t, nil
}
