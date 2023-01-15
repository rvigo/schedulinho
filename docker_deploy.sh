#!/bin/bash

# docker run --rm -e PUID="1000" -e PGID="2022" -e TZ="America/Sao_Paulo" -v /home/rafavigo/test_dir:/target --name schedulinho schedulinho
sudo docker run --rm "$@" --name schedulinho_test schedulinho:test
