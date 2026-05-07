#include <cstdio>
#include <cstdint>
#include <chrono>

int main() {
    using namespace std::chrono;
    const uint64_t iterations = 200000000ULL;

    auto start = high_resolution_clock::now();

    double result = 1.0;

    uint64_t i = 1;
    uint64_t end_unrolled = iterations / 8 * 8; // largest multiple of 8 <= iterations

    // Prevent vectorization to keep operation order consistent with Python
    #pragma clang loop vectorize(disable)
    for (; i <= end_unrolled; i += 8) {
        uint64_t k = (i << 2);
        result -= 1.0 / double(k - 1);
        result += 1.0 / double(k + 1);

        k += 4;
        result -= 1.0 / double(k - 1);
        result += 1.0 / double(k + 1);

        k += 4;
        result -= 1.0 / double(k - 1);
        result += 1.0 / double(k + 1);

        k += 4;
        result -= 1.0 / double(k - 1);
        result += 1.0 / double(k + 1);

        k += 4;
        result -= 1.0 / double(k - 1);
        result += 1.0 / double(k + 1);

        k += 4;
        result -= 1.0 / double(k - 1);
        result += 1.0 / double(k + 1);

        k += 4;
        result -= 1.0 / double(k - 1);
        result += 1.0 / double(k + 1);

        k += 4;
        result -= 1.0 / double(k - 1);
        result += 1.0 / double(k + 1);
    }

    for (; i <= iterations; ++i) {
        uint64_t k = (i << 2);
        result -= 1.0 / double(k - 1);
        result += 1.0 / double(k + 1);
    }

    result *= 4.0;

    auto end = high_resolution_clock::now();
    double elapsed = duration_cast<duration<double>>(end - start).count();

    std::printf("Result: %.12f\n", result);
    std::printf("Execution Time(Python): %.6f seconds\n", elapsed);

    return 0;
}