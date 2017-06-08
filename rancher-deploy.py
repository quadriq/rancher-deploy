#!/usr/bin/env python
import click
import io
import os
import sys

comopose_template="""version: '2'
services:
  %s:
    labels:
      io.rancher.container.pull_image: always
    image: %s
    stdin_open: true
    tty: true
"""

@click.command()
@click.option('--service_name', envvar='CI_PROJECT_NAME', required=True,
              help="service name in Rancher, Could be a name of gitlab project")
@click.option('--url', envvar='RANCHER_URL', required=True,
              help='The URL for your Rancher server, eg: http://rancher:8000')
@click.option('--rancher_key', envvar='RANCHER_ACCESS_KEY', required=True,
              help="The environment API key")
@click.option('--rancher_secret', envvar='RANCHER_SECRET_KEY', required=True,
              help="The environment secret API key")
@click.option('--docker_image', envvar='CI_REGISTRY_IMAGE', required=True,
              help="Docker Image: e.g. dockerhub.example.com/docker/ubutnu")
@click.option('--docker_image_tag', envvar='IMAGE_TAG', required=False,
              help="Docker Image Tag, e.g. latest", default='latest')
@click.option('--api_route', required=False, help="Rancher API route", default='v2-beta')

def doit(service_name, url, rancher_key, rancher_secret, docker_image, docker_image_tag, api_route):

    service_name = service_name.replace("_", "")

    compose = comopose_template % (service_name, "%s:%s" % (docker_image, docker_image_tag) )

    with io.open('docker-compose.yml', 'w') as file:
        file.write(compose)

    cmd  = "rancher-compose --url %s/%s --access-key \"%s\" --secret-key \"%s\" --debug up -d --force-upgrade" % (
        url,
        api_route,
        rancher_key,
        rancher_secret
    )
    print("executing: %s" % cmd)
    out = os.system(cmd)
    if out != 0:
        print("execution failed: %s" % cmd)
        sys.exit(1)

if __name__ == '__main__':
    doit()
