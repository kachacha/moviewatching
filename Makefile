IMAGE=registry.zylliondata.local/idsg/translate-tool:1.0.0
.PHONY: build push


build:
	docker-compose build --no-cache

push: build
	docker push $(IMAGE)
