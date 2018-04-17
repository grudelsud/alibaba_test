DOCKER_IMAGE = alibaba_test
DOCKER_CONTAINER = alibaba_test_container

help:
	@echo "--- MAKE HELP ---"
	@echo "\t make docker-build"
	@echo "\t make docker-run"
	@echo "\t make docker-stop-rm"
	@echo ""

default: help

docker-build:
	# building docker image: $(DOCKER_IMAGE)
	@sudo docker build -t $(DOCKER_IMAGE) .

docker-run:
	# starting docker container
	@sudo docker run \
		--name=$(DOCKER_CONTAINER) \
		-e ALI_ACCESSKEYID=$(ALI_ACCESSKEYID) \
		-e ALI_ACCESSKEYSECRET=$(ALI_ACCESSKEYSECRET) \
		-e ALI_ACCOUNTID=$(ALI_ACCOUNTID) \
		-d $(DOCKER_IMAGE)

docker-stop-rm:
	# stopping docker container
	@sudo docker stop $(DOCKER_CONTAINER)
	# removing docker container
	@sudo docker rm $(DOCKER_CONTAINER)
