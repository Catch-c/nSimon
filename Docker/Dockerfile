FROM python:3.10

# 2. EXPOSE PORT
EXPOSE 8080

# 3. Install dependencies
RUN pip install blinker pytest-playwright py-mon mariadb certifi==2023.7.22 charset-normalizer==3.2.0 click==8.1.7 colorama==0.4.6 Flask==2.3.3 greenlet==2.0.2 idna==3.4 itsdangerous==2.1.2 Jinja2==3.1.2 MarkupSafe==2.1.3 playwright==1.37.0 pyee==9.0.4 requests==2.31.0 typing_extensions==4.7.1 urllib3==2.0.4 waitress==2.1.2 Werkzeug==2.3.7
RUN playwright install --with-deps chromium

CMD ["python3"]
