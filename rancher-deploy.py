#!/usr/bin/env python
import click
import io
import os
import sys
import subprocess

comopose_template="""version: '2'
services:
  %s:
    labels:
      io.rancher.container.pull_image: always
    image: %s
    stdin_open: true
    tty: true
%s
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

@click.option('--rancher_option_force_all', required=False, help="Force Rancher to recreate/upgrade machine", default=False)
@click.option('--rancher_option_ports', required=False, help="Exposed Ports,separated by space; example: '8080:80 222:22'", default=False)
@click.option('--rancher_dynamic_ports', required=False, help="By using dynamic ports in Rancher, this would produce additional rancher-compose commit without ports", default=False)

@click.option('--docker_image', envvar='CI_REGISTRY_IMAGE', required=True,
              help="Docker Image: e.g. dockerhub.example.com/docker/ubutnu")
@click.option('--docker_image_tag', envvar='IMAGE_TAG', required=False,
              help="Docker Image Tag, e.g. latest", default='latest')

@click.option('--api_route', required=False, help="Rancher API route", default='v2-beta')


def doit(service_name, url, rancher_key, rancher_secret,
         rancher_option_force_all, rancher_option_ports, rancher_dynamic_ports,
         docker_image, docker_image_tag, api_route):

    service_name = service_name.replace("_", "")
    ports = ''
    if rancher_option_ports:
        ports_arr = rancher_option_ports.split(' ')
        for i, s in enumerate(ports_arr):
            ports_arr[i] = "     - \"%s/tcp\"" %s
        ports = "\n".join(ports_arr)
        ports = "    ports:\n" + ports
        noportsrun = False

    if rancher_dynamic_ports:
       compose_and_run(
           comopose_template % (service_name, "%s:%s" % (docker_image, docker_image_tag), ''),
           url,
           api_route,
           rancher_key,
           rancher_secret,
           rancher_option_force_all
       )

    compose_and_run(
        comopose_template % (service_name, "%s:%s" % (docker_image, docker_image_tag), ports),
        url,
        api_route,
        rancher_key,
        rancher_secret,
        rancher_option_force_all
    )

def compose_and_run(
        compose,
        url,
        api_route,
        rancher_key,
        rancher_secret,
        rancher_option_force_all
    ):
    print "create composer file:"
    print compose
    with io.open('docker-compose.yml', 'w') as file:
        file.write(compose)

    force = ''
    if rancher_option_force_all:
        force = "--pull --force-recreate --confirm-upgrade"

    cmd  = "rancher-compose --url %s/%s --access-key \"%s\" --secret-key \"%s\" --debug up -d %s" % (
        url,
        api_route,
        rancher_key,
        rancher_secret,
        force
    )
    print("executing: %s" % cmd)
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    process.wait()

    print process.returncode

if __name__ == '__main__':
    doit()
