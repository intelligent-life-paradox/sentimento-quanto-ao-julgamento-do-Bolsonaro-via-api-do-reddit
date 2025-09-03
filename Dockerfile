
FROM python:3.9-slim

# 2. O Diretório de Trabalho
WORKDIR /app


COPY . .


RUN ls -la


RUN pip install --no-cache-dir -r requirements.txt


EXPOSE 8501

CMD ["streamlit", "run", "app.py"]
