build:
	docker build -t your-docker-image .

push:
	docker push your-docker-image

deploy:
	kubectl apply -f k8s-deployment.yaml
