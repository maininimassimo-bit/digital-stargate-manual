FROM python:3.12.14-slim-bookworm@sha256:9c47360a2a0355e2da18516d0b1c2126ec22c195d2185e97347c9d98398c5bef

ENV PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONHASHSEED=0 \
    PYTHONUNBUFFERED=1 \
    SOURCE_DATE_EPOCH=0 \
    XDG_CONFIG_HOME=/app/dsg/config \
    DSG_EXTERNAL_PROVIDER_POLICY=DENY \
    DSG_METHOD_PROFILE_PATH=/app/dsg/method-profile/BKL-031-F3-A3-METHOD-PROFILE-001.json \
    DSG_METHOD_PROFILE_SHA256=e69f60e5ed7f71cd982437f6ca3556b732d6ae9a46718995134aa64a7b7f67ca \
    DSG_IERS_ARTIFACT_PATH=/app/dsg/artifacts/iers/astropy_iers_data-0.2026.9.14.0.56.43-py3-none-any.whl \
    DSG_IERS_SHA256=43786a0a9b60c7a55a85e12307c0050d75ea0679710378141255ded9d1bd8ebc

WORKDIR /app/dsg

COPY container/requirements.lock /tmp/dsg/requirements.lock
COPY container/.build/wheels/ /tmp/dsg/wheels/

RUN python -m pip install \
      --no-index \
      --no-compile \
      --no-deps \
      --find-links=/tmp/dsg/wheels \
      --only-binary=:all: \
      --require-hashes \
      --requirement /tmp/dsg/requirements.lock \
    && mkdir -p /app/dsg/artifacts/iers \
    && cp /tmp/dsg/wheels/astropy_iers_data-0.2026.9.14.0.56.43-py3-none-any.whl /app/dsg/artifacts/iers/ \
    && rm -rf /tmp/dsg/wheels \
    && find /usr/local/lib/python3.12/site-packages /usr/local/bin /app/dsg \
      -xdev -exec touch -h -d "@${SOURCE_DATE_EPOCH}" {} +

COPY method-profile/BKL-031-F3-A3-METHOD-PROFILE-001.json /app/dsg/method-profile/BKL-031-F3-A3-METHOD-PROFILE-001.json
COPY container/BKL-031-F3-A3-CONTAINER-MANIFEST-002.json /app/dsg/container/BKL-031-F3-A3-CONTAINER-MANIFEST-002.json
COPY container/astropy.cfg /app/dsg/config/astropy/astropy.cfg
COPY container/preflight.py /app/dsg/container/preflight.py
COPY container/entrypoint.sh /app/dsg/container/entrypoint.sh

RUN groupadd --gid 65532 dsg \
    && useradd --uid 65532 --gid 65532 --no-create-home --no-log-init --shell /usr/sbin/nologin dsg \
    && chmod 0555 /app/dsg/container/entrypoint.sh \
    && chown -R 65532:65532 /app/dsg \
    && find /app/dsg -xdev -exec touch -h -d "@${SOURCE_DATE_EPOCH}" {} + \
    && touch -d "@${SOURCE_DATE_EPOCH}" \
      /etc /etc/passwd /etc/group /etc/shadow /etc/gshadow /etc/subuid /etc/subgid

USER 65532:65532

ENTRYPOINT ["/app/dsg/container/entrypoint.sh"]
CMD ["/bin/sh", "-c", "echo 'NOT_EXECUTED: scientific runner is not materialized' >&2; exit 78"]
