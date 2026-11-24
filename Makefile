.PHONY: test build validate

test:
	go test ./...

build:
	mkdir -p bin
	go build -o bin/forged ./cmd/forged
	go build -o bin/forge ./cmd/forge

validate:
	./scripts/validate-config.sh

