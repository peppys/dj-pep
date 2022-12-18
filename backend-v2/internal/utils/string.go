package utils

func DerefString(s *string, fallback string) string {
	if s != nil {
		return *s
	}

	return fallback
}
