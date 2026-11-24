package api

import "time"

const Version = "forgeos.dev/v1"

type Request struct {
	Version string `json:"version"`
	Action  string `json:"action"`
}

type Response struct {
	Version string      `json:"version"`
	OK      bool        `json:"ok"`
	Data    interface{} `json:"data,omitempty"`
	Error   *Error      `json:"error,omitempty"`
}

type Error struct {
	Code    string `json:"code"`
	Message string `json:"message"`
}

type Status struct {
	Product      string            `json:"product"`
	Release      string            `json:"release"`
	API          string            `json:"api"`
	Mode         string            `json:"mode"`
	Healthy      bool              `json:"healthy"`
	StartedAt    time.Time         `json:"started_at"`
	Capabilities []string          `json:"capabilities"`
	Safety       map[string]string `json:"safety"`
}
