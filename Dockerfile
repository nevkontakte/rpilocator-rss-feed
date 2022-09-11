FROM python:3-alpine
RUN pip3 install pipenv
COPY Pipfile* .
RUN pipenv install --system
COPY . .
ENV FEED_URL 'https://rpilocator.com/feed/'
ENV TELEGRAM_BOT_TOKEN ''
ENV TELEGRAM_CHAT_ID ''
CMD ["python3", "rpilocator_telegram.py"]