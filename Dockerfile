FROM python:3.12-slim-bookworm AS base

# install pdm dependencies
RUN python -m pip install pdm --no-cache-dir

FROM base AS build
WORKDIR /app
COPY . /app
RUN pdm build

FROM python:3.12-alpine AS deployment
RUN addgroup -S nonroot \
    && adduser -S nonroot -G nonroot
WORKDIR /app
COPY --from=build /app/dist/*.whl .
RUN chown -R nonroot /app/*whl
USER nonroot
RUN pip install *.whl --no-cache-dir --prefer-binary
WORKDIR /home/nonroot/.local/lib/python3.12/site-packages/
COPY src/manage.py .
RUN python manage.py collectstatic
RUN chmod +rwx -R static
RUN pip install granian
EXPOSE 8000
CMD ["python", "-m", "granian", "--host", "0.0.0.0", "--interface", "wsgi", "billmate.wsgi:application"]
