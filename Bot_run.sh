#!/bin/sh

source /home/felipe/.cache/pypoetry/virtualenvs/domesticeconomy-XstqN5mN-py3.11/bin/activate  # todo alter to poetry
if [ -n "domesticeconomy-py3.11" ]; then
  echo "Ambiente virtual ativado com sucesso."
  RC=1
  while [ $RC -ne 0 ]; do
     python economybot.py
     RC=$?
  done
else
  echo "Falha ao ativar o ambiente virtual."
fi
