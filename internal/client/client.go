package client

import (
	"encoding/json"
	"fmt"
	"net"
	"time"

	"github.com/kaushikafkk/ForgeOS/internal/api"
)

func Request(socketPath, action string) (api.Response, error) {
	connection, err := net.DialTimeout("unix", socketPath, 2*time.Second)
	if err != nil {
		return api.Response{}, fmt.Errorf("connect to forged: %w", err)
	}
	defer connection.Close()
	_ = connection.SetDeadline(time.Now().Add(3 * time.Second))

	if err := json.NewEncoder(connection).Encode(api.Request{Version: api.Version, Action: action}); err != nil {
		return api.Response{}, fmt.Errorf("send request: %w", err)
	}
	var response api.Response
	if err := json.NewDecoder(connection).Decode(&response); err != nil {
		return api.Response{}, fmt.Errorf("read response: %w", err)
	}
	return response, nil
}

