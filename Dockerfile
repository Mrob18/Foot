FROM python:3.10
RUN apt-get update && apt-get install -y ffmpeg git
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
RUN mkdir -p exports
CMD ["python", "bot.py"]
