
import statistics
import time
import urllib.error
import urllib.request


CDN_URL = "http://127.0.0.1:8080/"

REGION_DELAYS_MS = {
    "nearby": 10,
    "regional": 60,
    "distant": 150,
}

SAMPLES = 10


def measure_request(url, bypass=False):
    headers = {}

    if bypass:
        headers["X-Bypass-Cache"] = "1"

    request = urllib.request.Request(
        url,
        headers=headers,
        method="GET",
    )

    start_time = time.perf_counter()

    try:
        with urllib.request.urlopen(
            request,
            timeout=10,
        ) as response:
            body = response.read()

            elapsed_ms = (
                time.perf_counter() - start_time
            ) * 1000

            return {
                "http_status": response.status,
                "edge": response.headers.get(
                    "X-Edge-Server", "unknown"
                ),
                "cache_status": response.headers.get(
                    "X-Cache-Status", "unknown"
                ),
                "response_time_ms": elapsed_ms,
                "bytes_received": len(body),
            }

    except (urllib.error.URLError, TimeoutError) as error:
        return {"error": str(error)}


def simulate_region(url, region, bypass=False):
    delay_ms = REGION_DELAYS_MS[region]
    result = measure_request(url, bypass=bypass)

    if "error" in result:
        return {"region": region, **result}

    time.sleep(delay_ms / 1000)

    return {
        **result,
        "region": region,
        "artificial_delay_ms": delay_ms,
        "simulated_total_ms": (
            result["response_time_ms"] + delay_ms
        ),
    }


def compare_cache_modes(url):
    print("Warming edge caches...")

    # Each edge has an independent cache.
    for _ in range(9):
        result = measure_request(url)
        if result.get("http_status") != 200:
            raise RuntimeError(
                f"Cache warm-up failed: {result}"
            )

    timings = {
        "HIT": [],
        "BYPASS": [],
    }

    for sample in range(1, SAMPLES + 1):
        # Alternate the first mode to reduce order bias.
        modes = (
            (False, True)
            if sample % 2
            else (True, False)
        )

        for bypass in modes:
            result = measure_request(url, bypass=bypass)

            expected = "BYPASS" if bypass else "HIT"

            if (
                result.get("http_status") != 200
                or result.get("cache_status") != expected
            ):
                raise RuntimeError(
                    f"Expected {expected}, received: {result}"
                )

            timings[expected].append(
                result["response_time_ms"]
            )

    hit_avg = statistics.mean(timings["HIT"])
    bypass_avg = statistics.mean(timings["BYPASS"])

    reduction = (
        (bypass_avg - hit_avg) / bypass_avg
    ) * 100

    print(f"Cache HIT average: {hit_avg:.3f} ms")
    print(f"Cache BYPASS average: {bypass_avg:.3f} ms")
    print(f"Measured latency reduction: {reduction:.2f}%")

    return timings


if __name__ == "__main__":
    compare_cache_modes(CDN_URL)
