SHELL := /bin/bash
PROJECT := cyber-lab-foundry
COMPOSE := docker compose
COMPOSE_FILE := docker-compose.yml

.DEFAULT_GOAL := help

help:
	@echo "Available targets:"
	@grep -E '^[a-zA-Z_-]+:.*##' Makefile | awk 'BEGIN {FS = "\\:.*## "} {printf "  %-20s %s\n", $$1, $$2}'

up: ## Launch the lab environment
	$(COMPOSE) up -d --build

rebuild: ## Rebuild all containers
	$(COMPOSE) build --no-cache

attack: ## Run a red team scenario (NAME=01-ssh-bruteforce)
	@if [ -z "$(NAME)" ]; then \
		echo "Usage: make attack NAME=<scenario-folder>"; exit 1; \
	fi
	$(COMPOSE) run --rm attacker /opt/redteam/run_scenario.sh "$(NAME)"

pcap: ## Start packet capture rotation on mitm-gateway
	$(COMPOSE) run --rm mitm-gateway /opt/capture/capture.sh

detect: ## Import detections and verify SIEM pipelines
	$(COMPOSE) run --rm defender-siem /opt/detect/import.sh

docs-serve: ## Serve MkDocs documentation locally
	pip install -r docs/requirements.txt
	mkdocs serve

down: ## Stop the lab containers
	$(COMPOSE) down

clean: ## Remove containers, volumes, and artifacts
	$(COMPOSE) down -v --remove-orphans
	mkdir -p telemetry/capture/pcaps telemetry/parsers/output
	rm -f telemetry/capture/pcaps/*.pcap telemetry/parsers/output/*.csv || true

.PHONY: help up rebuild attack pcap detect docs-serve down clean
