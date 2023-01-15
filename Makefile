.PHONY: help

help: 
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

build: ## build image locally
	./custom_requirements.sh
	sudo docker build . -t schedulinho:test

run: ## merge requirements content and start container with `docker_deploy_args` content
	./docker_deploy.sh $(cat docker_deploy_args.txt)

all: build run
