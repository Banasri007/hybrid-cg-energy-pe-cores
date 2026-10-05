/* Idle power baseline: average RAPL power per domain over N seconds of sleep.
 * Usage: rapl_idle [seconds=10]
 * Output: one key=value line (W per domain, -1 if unreadable). */
#define _DEFAULT_SOURCE
#include "rapl.h"
#include "csr.h"
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int main(int argc, char **argv) {
    double secs = argc > 1 ? atof(argv[1]) : 10.0;
    rapl_t r;
    unsigned long long a[RAPL_MAXDOM], b[RAPL_MAXDOM];
    int ok = rapl_init(&r) > 0 && rapl_read(&r, a) == 0;
    double temp0 = pkg_temp_c(), t0 = wall_time();
    usleep((useconds_t)(secs * 1e6));
    double dt = wall_time() - t0;
    ok = ok && rapl_read(&r, b) == 0;
    const char *dn[4] = {"package-0", "core", "uncore", "psys"}, *key[4] = {"pkg", "core", "uncore", "psys"};
    printf("idle_s=%.2f", dt);
    for (int d = 0; d < 4; d++) {
        int k = ok ? rapl_find(&r, dn[d]) : -1;
        printf(" p_%s_w=%.3f", key[d], k >= 0 ? rapl_joules(&r, k, a[k], b[k]) / dt : -1.0);
    }
    printf(" temp_start_c=%.1f temp_end_c=%.1f\n", temp0, pkg_temp_c());
    return ok ? 0 : 2;
}
