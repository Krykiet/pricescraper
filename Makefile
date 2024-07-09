NAME=gitlab.emacs.energy:5050/emacsdev/tge-scraper
TAG=latest

build:
	docker build -t $(NAME):$(TAG) .

push:
	docker push $(NAME):$(TAG)