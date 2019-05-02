#alpine is a package which is much smaller. You can also choose ubutu as basic image by change it to FROM ubuntu:latest
#FROM alpine

FROM golang:1.11 as builder

#as builder
LABEL maintainer="Rajat Jain <rajat.jain@aadhyatm.org>"

# create a working directory
WORKDIR $GOPATH/src/github.com/aadhyatm/jaincatalogue

# Log dir
RUN mkdir -p /logs

# install glide
RUN go get github.com/Masterminds/glide

COPY . .

# install packages
RUN glide install

EXPOSE 8080

# VOLUME ["/logs"]

# Set environment variables
ENV JAIN_CATALOGUE_ENVIRONMENT=staging
# ENV LOG_DIR=/logs

# build the source
CMD ["go", "run", "main.go"]