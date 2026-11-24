package server

import (
	"testing"

	"github.com/kaushikafkk/ForgeOS/internal/api"
)

func TestStatus(t *testing.T) {
	response := New().Handle(api.Request{Version: api.Version, Action: "status.read"})
	if !response.OK {
		t.Fatalf("expected status request to succeed: %#v", response.Error)
	}
	status, ok := response.Data.(api.Status)
	if !ok || !status.Healthy {
		t.Fatalf("expected healthy typed status, got %#v", response.Data)
	}
}

func TestRejectsUnknownVersion(t *testing.T) {
	response := New().Handle(api.Request{Version: "unknown/v9", Action: "status.read"})
	if response.OK || response.Error == nil || response.Error.Code != "unsupported_version" {
		t.Fatalf("expected unsupported_version, got %#v", response)
	}
}

func TestRejectsUnknownAction(t *testing.T) {
	response := New().Handle(api.Request{Version: api.Version, Action: "shell.run"})
	if response.OK || response.Error == nil || response.Error.Code != "unsupported_action" {
		t.Fatalf("expected unsupported_action, got %#v", response)
	}
}
