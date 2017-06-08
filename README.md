# Deploy container on Rancher from Gitlab-CI

here is simple script, that deploys a container form Gitlab Registry, using Gitlab-CI


## Setup

It requires the `rancher-compose`, install in from here: https://github.com/rancher/rancher-compose/releases

you need also to install "python click": `pip install click`

then put the script `rancher-deploy.py` to `/bin/rancher-deploy.py` and do `chmod +x /bin/rancher-deploy.py`

here, check the script help

```
# rancher-deploy.py --help

Usage: rancher-deploy.py [OPTIONS]

Options:
  --service_name TEXT      service name in Rancher, Could be a name of gitlab
                           project  [required]
  --url TEXT               The URL for your Rancher server, eg:
                           http://rancher:8000  [required]
  --rancher_key TEXT       The environment API key  [required]
  --rancher_secret TEXT    The environment secret API key  [required]
  --docker_image TEXT      Docker Image: e.g.
                           dockerhub.example.com/docker/ubutnu  [required]
  --docker_image_tag TEXT  Docker Image Tag, e.g. latest
  --api_route TEXT         Rancher API route
  --help                   Show this message and exit.

```

## Integrate to GitLab

in gitlab create project variables:
```
RANCHER_ACCESS_KEY # Environment key
RANCHER_SECRET_KEY # Environment secret
RANCHER_URL	# URL of rancher host
```

and here is an example of CI script

```
stages:
  - build
  - deploy

build:
  stage: build
  script:
    - docker login -u gitlab-ci-token -p $CI_BUILD_TOKEN $CI_REGISTRY
    - docker build -t $CI_REGISTRY_IMAGE .
    - docker push $CI_REGISTRY_IMAGE

deploy:
  stage: deploy
  script:
    - rancher-deploy.py
```
