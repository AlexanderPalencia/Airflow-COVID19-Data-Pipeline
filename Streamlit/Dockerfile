FROM python:3.7
RUN mkdir -p /root/.streamlit

WORKDIR /app 
RUN bash -c 'echo -e "\
[general]\n\
email = \"your-email@domain.com\"\n\
" > /root/.streamlit/credentials.toml'
COPY . /app
RUN pip install -r requirements.txt
EXPOSE 8501
CMD ["streamlit", "run", "appstream.py", "--server.enableCORS=false"]