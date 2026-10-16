
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
