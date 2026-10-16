#!/usr/bin/env bash
# 전날 공부 노트 작성 + git push (공부량 있을 때만)
set -euo pipefail

export PATH="${HOME}/.local/bin:${PATH}"
REPO="$(cd "$(dirname "$0")/.." && pwd)"
LOG_DIR="${REPO}/logs"
mkdir -p "${LOG_DIR}"
LOG_FILE="${LOG_DIR}/daily_study_$(date +%Y%m%d_%H%M%S).log"

{
  echo "=== daily study publish $(date -Is) ==="
  cd "${REPO}"

  # git 커밋 신원 (config 미설정 환경 대비)
  export GIT_AUTHOR_NAME="${GIT_AUTHOR_NAME:-Hyungmo1234}"
  export GIT_AUTHOR_EMAIL="${GIT_AUTHOR_EMAIL:-tytyrrr13@gmail.com}"
  export GIT_COMMITTER_NAME="${GIT_AUTHOR_NAME}"
  export GIT_COMMITTER_EMAIL="${GIT_AUTHOR_EMAIL}"

  python3 "${REPO}/scripts/daily_study_publish.py" "$@"
  echo "=== done ==="
} 2>&1 | tee -a "${LOG_FILE}"
