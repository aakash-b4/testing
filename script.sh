#!/usr/bin/env bash
nohup /usr/local/openjdk-8/bin/java -jar icici-0.0.1.jar &

echo Starting Gunicorn.
exec gunicorn -w 3 -b 0.0.0.0:80 payout.wsgi --timeout 120