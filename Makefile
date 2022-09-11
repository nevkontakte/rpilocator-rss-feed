IMAGE := "ghcr.io/nevkontakte/rpilocator-rss-feed"

.PHONY: build run

docker-build:
	docker build -t $(IMAGE) .
	docker images $(IMAGE):latest

docker-push: docker-build
	docker push $(IMAGE)
