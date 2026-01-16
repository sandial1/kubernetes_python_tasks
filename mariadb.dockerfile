FROM mariadb:latest

# Optional: Add custom configuration
COPY my.cnf /etc/mysql/conf.d/

# Expose the default MariaDB port
EXPOSE 3306

# The entrypoint and cmd are inherited from the base image