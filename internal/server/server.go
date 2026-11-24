package server

import (
	"encoding/json"
	"fmt"
	"io"
	"net"
	"os"
	"path/filepath"
	"time"

	"github.com/kaushikafkk/ForgeOS/internal/api"
)

type Server struct {
	startedAt time.Time
}

func New() *Server {
	return &Server{startedAt: time.Now().UTC()}
}

func (s *Server) Handle(req api.Request) api.Response {
	if req.Version != api.Version {
		return failure("unsupported_version", fmt.Sprintf("expected %s", api.Version))
	}

	switch req.Action {
	case "status.read":
		return api.Response{
			Version: api.Version,
			OK:      true,
			Data: api.Status{
				Product:   "ForgeOS",
				Release:   "0.1-dev",
				API:       api.Version,
				Mode:      "read-only milestone zero",
				Healthy:   true,
				StartedAt: s.startedAt,
				Capabilities: []string{
					"status.read",
					"snapshot.list.planned",
					"update.plan.planned",
				},
				Safety: map[string]string{
					"mutations": "disabled until Polkit and recovery tests land",
					"telemetry": "disabled",
				},
			},
		}
	default:
		return failure("unsupported_action", "the requested operation is not available")
	}
}

func (s *Server) Serve(socketPath string) error {
	if err := os.MkdirAll(filepath.Dir(socketPath), 0o755); err != nil {
		return fmt.Errorf("create socket directory: %w", err)
	}
	_ = os.Remove(socketPath)

	listener, err := net.Listen("unix", socketPath)
	if err != nil {
		return fmt.Errorf("listen on %s: %w", socketPath, err)
	}
	defer listener.Close()
	if err := os.Chmod(socketPath, 0o660); err != nil {
		return fmt.Errorf("set socket permissions: %w", err)
	}
	return s.ServeListener(listener)
}


// ServeListener accepts requests from an existing listener. This allows
// systemd socket activation to own the Unix socket and pass descriptor 3 to
// forged without a second process trying to bind the same path.
func (s *Server) ServeListener(listener net.Listener) error {
	for {
		conn, acceptErr := listener.Accept()
		if acceptErr != nil {
			return acceptErr
		}
		go s.handleConnection(conn)
	}
}

func (s *Server) handleConnection(conn net.Conn) {
	defer conn.Close()
	decoder := json.NewDecoder(io.LimitReader(conn, 64*1024))
	encoder := json.NewEncoder(conn)
	var req api.Request
	if err := decoder.Decode(&req); err != nil {
		_ = encoder.Encode(failure("invalid_request", "request must be valid JSON"))
		return
	}
	_ = encoder.Encode(s.Handle(req))
}

func failure(code, message string) api.Response {
	return api.Response{
		Version: api.Version,
		OK:      false,
		Error:   &api.Error{Code: code, Message: message},
	}
}

