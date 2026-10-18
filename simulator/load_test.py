
import statistics
import time
import urllib.error
import urllib.request

from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed


URL = "http://127.0.0.1:8080/"
TOTAL_REQUESTS = 100
CONCURRENT_WORKERS = 10
TIMEOUT_SECONDS = 10


def send_request(request_number):
    request = urllib.request.Request(
        URL,
        method="GET",
    )

    start = time.perf_counter()

    try:
        with urllib.request.urlopen(
            request,
            timeout=TIMEOUT_SECONDS,
        ) as response:
            response.read()

            duration_ms = (
                time.perf_counter() - start
            ) * 1000

            return {
                "number": request_number,
                "status": response.status,
                "duration_ms": duration_ms,
                "edge": response.headers.get(
                    "X-Edge-Server", "unknown"
                ),
                "cache": response.headers.get(
                    "X-Cache-Status", "unknown"
                ),
            }

    except (
        urllib.error.URLError,
        TimeoutError,
        OSError,
    ) as error:
        return {
            "number": request_number,
            "status": 0,
            "duration_ms": (
                time.perf_counter() - start
            ) * 1000,
            "error": str(error),
        }


def run_load_test():
    print(f"Total requests: {TOTAL_REQUESTS}")
    print(f"Concurrent workers: {CONCURRENT_WORKERS}")

    results = []

    test_start = time.perf_counter()

    with ThreadPoolExecutor(
        max_workers=CONCURRENT_WORKERS
    ) as executor:

        futures = [
            executor.submit(send_request, i)
            for i in range(1, TOTAL_REQUESTS + 1)
        ]

        for future in as_completed(futures):
            results.append(future.result())

    total_seconds = time.perf_counter() - test_start

    successful = [
        r for r in results
        if r["status"] == 200
    ]

    failed = TOTAL_REQUESTS - len(successful)

    
    success_rate = (
        len(successful) / TOTAL_REQUESTS
    ) * 100

    print(f"Success rate: {success_rate:.2f}%")


    print(f"\nSuccessful requests: {len(successful)}")
    print(f"Failed requests: {failed}")

    if successful:
        durations = [
            r["duration_ms"]
            for r in successful
        ]
        if len(durations) >= 2:
            p95 = statistics.quantiles(
                durations,
                n=100,
                method="inclusive",
        )[94]

        print(
                f"P95 response time: {p95:.2f} ms"
        )

        print(
            f"Average response time: "
            f"{statistics.mean(durations):.2f} ms"
        )

        print(
            f"Median response time: "
            f"{statistics.median(durations):.2f} ms"
        )

    print(
        f"Total test duration: {total_seconds:.2f} s"
    )

    print(
        f"Throughput: "
        f"{len(successful) / total_seconds:.2f} "
        f"successful requests/second"
    )

    print("\nRequests served by each edge:")

    edge_counts = Counter(
        r["edge"] for r in successful
    )

    for edge, count in sorted(edge_counts.items()):
        print(f"  {edge}: {count}")

    print("\nCache statuses:")

    cache_counts = Counter(
        r["cache"] for r in successful
    )

    for status, count in sorted(cache_counts.items()):
        print(f"  {status}: {count}")

    
    cache_hits = cache_counts.get("HIT", 0)

    cache_hit_ratio = (
        cache_hits / len(successful) * 100
        if successful
        else 0
    )

    print(
        f"\nCache hit ratio: {cache_hit_ratio:.2f}%"
    )



if __name__ == "__main__":
    run_load_test()
