
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

**In development.** Infrastructure configuration and performance benchmarks have not yet been implemented.

## Deployment Scope

The simulator runs multiple containers on one host. Geographic network latency is simulated, not measured across real distributed edge locations.

## Performance Evaluation

Planned metrics include response latency, cache hit ratio, origin request reduction, and load distribution. Results will be added after testing.
  