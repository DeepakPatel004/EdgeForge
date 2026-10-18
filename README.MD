
# CDN Simulator

A containerized Content Delivery Network (CDN) simulator designed to demonstrate HTTP load balancing, edge caching, network latency simulation, and fault tolerance.

## Project Objectives

- Distribute HTTP requests across three simulated edge servers.
- Cache static content to reduce origin server requests.
- Compare round-robin and least-connections load balancing.
- Configure cache TTL, LRU eviction, and cache bypass.
- Simulate network latency using Python.
- Test edge failure handling and measure CDN performance.
- Deploy the simulator to a single AWS EC2 instance.

## Technology Stack

- Nginx — reverse proxy, load balancing, and caching
- Docker Compose — container orchestration
- Python — network simulation and benchmarking
- AWS EC2 — cloud hosting
- Linux — deployment environment
- Git — version control

## Architecture

Client → Nginx Load Balancer → 3 Caching Edge Servers → Origin Server

Each edge server maintains its own cache and contacts the origin when necessary.

See [Architecture Documentation](docs/architecture.md) for details.

## Project Status

**In development — Day 3 completed.**

Implemented and locally verified:
- Five-container CDN architecture using Docker Compose.
- Nginx reverse proxy and load balancing.
- Independent edge caching with HIT/MISS tracking.
- Cache TTL, expiration, and LRU-based eviction configuration.
- Cache bypass using a request header.

Upcoming:
- Python network latency simulation.
- Fault tolerance and load testing.
- AWS EC2 deployment.
- Performance benchmarking and measured results.

## Deployment Scope

The simulator runs multiple containers on one host. Geographic network latency is simulated, not measured across real distributed edge locations.

## Performance Evaluation

Planned metrics include response latency, cache hit ratio, origin request reduction, and load distribution. Results will be added after testing.

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


  