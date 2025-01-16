# 베이스 이미지 설정
FROM --platform=linux/amd64 python:3.10.8

# 기본 업데이트 및 필요한 패키지 설치
RUN apt-get update -y \
 && apt-get install -y --no-install-recommends apt-utils \
 && apt-get install -y \
    unixodbc \
    unixodbc-dev \
    freetds-dev \
    freetds-bin \
    tdsodbc \
    build-essential \
 && python -m pip install --upgrade pip setuptools \
 && pip install setuptools_scm

# 작업 디렉토리 설정 및 파일 복사
WORKDIR /app
COPY odbcinst.ini /etc/odbcinst.ini
COPY . .

# Python 패키지 설치
RUN pip install pyodbc \
 && pip install jupyter \
 && pip install notebook

# Jupyter Notebook을 실행하는 기본 명령어 설정
CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root"]