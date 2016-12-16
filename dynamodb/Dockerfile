FROM makuk66/docker-oracle-java7

RUN mkdir /var/dynamodb_wd
WORKDIR /var/dynamodb_wd

EXPOSE 8000

RUN wget -O /var/dynamodb_wd/dynamodb_local_latest http://dynamodb-local.s3-website-us-west-2.amazonaws.com/dynamodb_local_latest
RUN tar xfz /var/dynamodb_wd/dynamodb_local_latest

ENTRYPOINT ["/usr/bin/java", "-Djava.library.path=.", "-jar", "DynamoDBLocal.jar", "-dbPath", "/var/dynamodb_local"]
CMD ["-port", "8000"]

VOLUME ["/var/dynamodb_local", "/var/dynamodb_wd"]

