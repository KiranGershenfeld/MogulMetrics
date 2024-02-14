FROM golang:1.21.6-alpine AS build

RUN mkdir -p /go/src/local-trending ~/.ssh && \
    apk add --no-cache git openssh-client make gcc libc-dev
WORKDIR /go/src/local-trending
COPY . .
RUN make build

FROM alpine:3
COPY --from=build /go/src/local-trending/video-ingest /bin/video-ingest

CMD /bin/video-ingest