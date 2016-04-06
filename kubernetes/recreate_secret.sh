#!/bin/bash
head -4 secret.yaml | kubectl delete -f -
cat secret.yaml|sed s#::SECRET::#$(cat limbo.env|base64 -w 0)#g |kubectl create -f -
