FROM python:3.12-slim

RUN apt-get update \
  && apt-get install -y --no-install-recommends git \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app
COPY config ./config
COPY static ./static

ENV PROJECTS_BASE=/repos
ENV PORT=8080

# Fly/CI: 공개 GitHub 저장소를 빌드 시 clone (로컬 docker build --build-arg CLONE_REPOS=0 로 생략 가능)
ARG CLONE_REPOS=1
RUN if [ "$CLONE_REPOS" = "1" ]; then \
      mkdir -p /repos && \
      git clone --depth 1 https://github.com/Hyungmo1234/261015python.git /repos/261015python && \
      git clone --depth 1 https://github.com/Hyungmo1234/mobile_invitationByCursor.git /repos/mobile_invitationByCursor && \
      git clone --depth 1 https://github.com/Hyungmo1234/prophecy.git /repos/prophecy; \
    fi

EXPOSE 8080

CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT}"]
