FROM python:3.10.11 AS compilation_stage

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_DISABLE_PIP_VERSION_CHECK 1

RUN apt-get update && \
    apt-get install -y curl && \
    apt-get install -y git

RUN curl -LO https://github.com/neovim/neovim/releases/latest/download/nvim.appimage \
    && chmod u+x nvim.appimage \
    && ./nvim.appimage --appimage-extract \
    && mv squashfs-root /opt/nvim \
    && ln -s /opt/nvim/usr/bin/nvim /usr/local/bin/nvim

WORKDIR /django
COPY requirements.txt .
RUN python -m venv /opt/venv

RUN pip config set global.trusted-host "pypi.org files.pythonhosted.org pypi.python.org"

ENV PATH="/opt/venv/bin:$PATH"
RUN apt-get install -y gcc \
 && pip install --no-cache-dir --upgrade pip \
 && pip install --no-cache-dir setuptools wheel \
 && pip install --no-cache-dir -r requirements.txt \
 && rm -rf /var/lib/apt/lists/*

COPY . .

ENV DJANGO_SETTINGS_MODULE=beri_box.settings
ENV LANG=ru_RU.UTF-8
ENV TZ=Europe/Moscow

ENTRYPOINT sleep 10 && \
           python3 hospital/manage.py makemigrations && \
           python3 hospital/manage.py migrate && \
           python3 hospital/manage.py collectstatic --no-input && \
            python3 hospital/manage.py runserver 0.0.0.0:8000