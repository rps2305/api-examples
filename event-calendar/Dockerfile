FROM python:3.12-slim

WORKDIR /app

RUN groupadd --system calendar && useradd --system --gid calendar --home-dir /app --no-create-home calendar

COPY scripts ./scripts
COPY event-calendar/*.py ./event-calendar/
COPY event-calendar/assets ./event-calendar/assets
COPY event-calendar/index.html event-calendar/about.html event-calendar/technical.html event-calendar/disclaimer.html event-calendar/privacy.html event-calendar/styles.css event-calendar/app.js event-calendar/analytics-consent.js event-calendar/back-to-top.js event-calendar/loading-watchdog.js event-calendar/theme.js event-calendar/sw.js event-calendar/events.json event-calendar/events.ics event-calendar/favicon.ico event-calendar/robots.txt event-calendar/security.txt event-calendar/site.webmanifest event-calendar/sitemap.xml ./event-calendar/
COPY event-calendar/.well-known ./event-calendar/.well-known

WORKDIR /app/event-calendar
ENV PYTHONUNBUFFERED=1 \
    PORT=8080 \
    PYTHONDONTWRITEBYTECODE=1

RUN chown -R calendar:calendar /app
USER calendar

EXPOSE 8080

CMD ["python", "server.py"]
