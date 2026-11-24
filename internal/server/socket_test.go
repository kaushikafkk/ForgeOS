//go:build unix

package server

import (
	"encoding/json"
	"net"
	"path/filepath"
	"testing"
	"time"

	"github.com/kaushikafkk/ForgeOS/internal/api"
)

func TestUnixSocketRoundTrip(t *testing.T) {
	path := filepath.Join(t.TempDir(), "forged.sock")
	listener, err := net.Listen("unix", path)
	if err != nil {
		t.Fatal(err)
	}
	defer listener.Close()

	done := make(chan error, 1)
	go func() { done <- New().ServeListener(listener) }()

	connection, err := net.DialTimeout("unix", path, time.Second)
	if err != nil {
		t.Fatal(err)
	}
	defer connection.Close()
	if err := json.NewEncoder(connection).Encode(api.Request{Version: api.Version, Action: "status.read"}); err != nil {
		t.Fatal(err)
	}
	var response api.Response
	if err := json.NewDecoder(connection).Decode(&response); err != nil {
		t.Fatal(err)
	}
	if !response.OK {
		t.Fatalf("expected successful socket response: %#v", response.Error)
	}
}
