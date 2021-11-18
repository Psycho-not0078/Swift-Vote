#!/bin/sh

ssh root@127.0.0.1:5500 <<EOF
  cd Swift_Vote
  git pull
  source /opt/envs/Swift_Vote/bin/activate
  pip install -r requirements.txt
  ./manage.py migrate
  sudo supervisorctl restart Swift_Vote
  exit
EOF
