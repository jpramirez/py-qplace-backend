FROM faizanbashir/python-datascience

# Packages that we need 
COPY requirements.txt /app/
WORKDIR /app
RUN pip install -r requirements.txt
COPY . /app

ENTRYPOINT ["python"]

EXPOSE 3000
# We want to start app.py file. (change it with your file name) # Argument to python command
CMD ["webapp.py"]