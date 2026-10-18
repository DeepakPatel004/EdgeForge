
# CDN Simulator — System Architecture

## Architecture Overview

The simulator uses five Nginx containers managed by Docker Compose.

```text
              Client
                 |
                 v
        Nginx Load Balancer
           /     |     \
          v      v      v
       Edge 1  Edge 2  Edge 3
        Cache   Cache   Cache
           \     |     /
            \    |    /
             Origin
         (Static Content)
```

## Components

### Load Balancer
- Single client-facing entry point.
- Supports round-robin and least-connections routing.
- Distributes HTTP requests across three edge servers.

### Edge Servers
- Three independently running Nginx containers.
- Each maintains its own local disk cache.
- Serves cache HIT responses directly.
- Fetches eligible content from the origin on cache MISS.

### Origin Server
- Stores original static files.
- Accessible internally through the Docker network.
- Serves content requested by edge servers.

## HTTP Request Flow

1. Client sends an HTTP GET request.
2. Load balancer selects an edge server.
3. Edge server checks its local cache.
4. On a HIT, cached content is returned.
5. On a MISS, the edge fetches content from origin.
6. Cacheable content is stored according to configured rules.
7. The response returns to the client.

## Networking

- Client-facing host port: 8080.
- Nginx container HTTP port: 80.
- Service discovery uses Docker DNS.
- Edge and origin containers are not directly published.

## Deployment Limitations

All five containers run on one host.

This architecture demonstrates CDN mechanisms but does not provide geographically distributed edge locations or host-level fault tolerance.

## Planned Performance Testing

Python scripts will measure response time, cache hit ratio, origin request reduction, and request distribution under controlled workloads.

## Edge Caching Strategy

Each edge maintains an independent Nginx disk cache.

Configuration:
- Cache directory: `/var/cache/nginx/cdn`
- Freshness TTL for HTTP 200 responses: 5 minutes
- Target disk cache size: 100 MB per edge
- Inactive entry retention: 10 minutes
- Cache eviction: Nginx cache-manager LRU behavior

Responses expose `X-Edge-Server` and `X-Cache-Status`
headers for troubleshooting and performance evaluation.

Requests containing `X-Bypass-Cache: 1` bypass the existing
cache and prevent the returned response from being stored.

The bypass header is intended for controlled experiments,
not as a production-ready public cache-control policy.

## Python Latency Simulator

The simulator is implemented in `simulator/latency_test.py`.

**Measurement flow:**

1. Python sends an HTTP request to the local Nginx load balancer.
2. The load balancer forwards the request to an edge server.
3. The edge serves a cached response or forwards the request to the origin.
4. Python reads the complete response and records the elapsed duration.
5. The simulator records the serving edge and cache status.
6. For regional simulations, Python adds a configured artificial delay.

**Cache comparison:** The benchmark warms the caches, alternates HIT and BYPASS requests, validates the returned cache statuses, and calculates their average durations.

**Limitations:** The delay profiles are simulated, not actual geographical measurements. All CDN containers currently share one Docker host. Earlier Python measurements showed unexpectedly high durations compared with a separate curl test; their cause has not been established.