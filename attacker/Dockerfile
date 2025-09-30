FROM debian:bullseye-slim

RUN apt update && \
    apt install -y hping3 iproute2 && \
    apt clean

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

CMD ["/entrypoint.sh"]