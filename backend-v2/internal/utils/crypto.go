package utils

import (
	"crypto/md5"
	"encoding/base64"
)

func Md5Hash(val string) string {
	hasher := md5.New()
	hasher.Write([]byte(val))
	return base64.URLEncoding.EncodeToString(hasher.Sum(nil))
}
