package main

import (
	"encoding/json"
	"flag"
	"fmt"
	"os"

	"github.com/kaushikafkk/ForgeOS/internal/api"
	"github.com/kaushikafkk/ForgeOS/internal/client"
)

func main() {
	statusFlags := flag.NewFlagSet("status", flag.ExitOnError)
	jsonOutput := statusFlags.Bool("json", false, "print machine-readable JSON")
	socket := statusFlags.String("socket", "/run/forgeos/forged.sock", "forged Unix socket")

	if len(os.Args) < 2 || os.Args[1] != "status" {
		fmt.Fprintln(os.Stderr, "usage: forge status [--json] [--socket PATH]")
		os.Exit(2)
	}
	_ = statusFlags.Parse(os.Args[2:])

	response, err := client.Request(*socket, "status.read")
	if err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
	if *jsonOutput {
		_ = json.NewEncoder(os.Stdout).Encode(response)
		return
	}
	if !response.OK {
		fmt.Fprintf(os.Stderr, "%s: %s\n", response.Error.Code, response.Error.Message)
		os.Exit(1)
	}

	payload, err := json.Marshal(response.Data)
	if err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
	var status api.Status
	if err := json.Unmarshal(payload, &status); err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
	fmt.Printf("%s %s\n", status.Product, status.Release)
	fmt.Printf("health:  %t\n", status.Healthy)
	fmt.Printf("mode:    %s\n", status.Mode)
	fmt.Printf("api:     %s\n", status.API)
}
