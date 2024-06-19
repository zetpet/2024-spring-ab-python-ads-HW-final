build:
	docker build -t docker-image .

push:
	docker push docker-image

deploy:
	kubectl apply -f k8s-deployment.yaml
