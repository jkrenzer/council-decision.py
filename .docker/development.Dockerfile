FROM python:3.10-alpine as base

ARG WORK_DIR=/workspaces/council-decision.py

RUN apk add --no-cache git git-lfs
RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN git lfs install

FROM base as builder

RUN apk add --no-cache gcc g++
WORKDIR ${WORK_DIR}
COPY ./* ./
RUN poetry install --with=dev

