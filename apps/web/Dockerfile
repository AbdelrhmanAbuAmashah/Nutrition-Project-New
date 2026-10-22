FROM node:22-bookworm-slim AS deps
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci --no-audit --no-fund

FROM deps AS builder
ENV NEXT_TELEMETRY_DISABLED=1
COPY . .
RUN npm run format:check && npm run typecheck && npm run build

FROM node:22-bookworm-slim AS runner
WORKDIR /app
ENV NODE_ENV=production NEXT_TELEMETRY_DISABLED=1 HOSTNAME=0.0.0.0 PORT=3000
RUN groupadd --gid 10001 nour && useradd --uid 10001 --gid nour --no-create-home nour
COPY --from=builder --chown=nour:nour /app/.next/standalone ./
COPY --from=builder --chown=nour:nour /app/.next/static ./.next/static
USER nour
EXPOSE 3000
CMD ["node", "server.js"]
