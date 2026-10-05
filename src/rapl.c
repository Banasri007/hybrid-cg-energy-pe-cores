#define _DEFAULT_SOURCE
#include "rapl.h"
#include <glob.h>
#include <stdio.h>
#include <string.h>

static int read_ull(const char *path, unsigned long long *v) {
    FILE *f = fopen(path, "r");
    if (!f) return -1;
    int ok = fscanf(f, "%llu", v) == 1;
    fclose(f);
    return ok ? 0 : -1;
}

static int read_str(const char *path, char *buf, size_t len) {
    FILE *f = fopen(path, "r");
    if (!f) return -1;
    if (!fgets(buf, (int)len, f)) { fclose(f); return -1; }
    fclose(f);
    buf[strcspn(buf, "\n")] = 0;
    return 0;
}

int rapl_init(rapl_t *r) {
    memset(r, 0, sizeof *r);
    glob_t g;
    /* "intel-rapl:*" matches intel-rapl:0, :0:0, :0:1, :1 but not the
     * intel-rapl-mmio duplicate of the package domain */
    if (glob("/sys/class/powercap/intel-rapl:*", 0, NULL, &g) != 0) return 0;
    for (size_t i = 0; i < g.gl_pathc && r->n < RAPL_MAXDOM; i++) {
        char p[480];
        unsigned long long v;
        snprintf(p, sizeof p, "%s/energy_uj", g.gl_pathv[i]);
        if (read_ull(p, &v)) continue;                     /* not readable */
        snprintf(r->path[r->n], sizeof r->path[0], "%s", p);
        snprintf(p, sizeof p, "%s/name", g.gl_pathv[i]);
        if (read_str(p, r->name[r->n], sizeof r->name[0])) continue;
        snprintf(p, sizeof p, "%s/max_energy_range_uj", g.gl_pathv[i]);
        if (read_ull(p, &r->max_uj[r->n])) continue;
        r->n++;
    }
    globfree(&g);
    return r->n;
}

int rapl_read(const rapl_t *r, unsigned long long *uj) {
    for (int d = 0; d < r->n; d++)
        if (read_ull(r->path[d], &uj[d])) return -1;
    return 0;
}

double rapl_joules(const rapl_t *r, int d, unsigned long long a, unsigned long long b) {
    unsigned long long diff = b >= a ? b - a : r->max_uj[d] - a + b + 1;
    return diff * 1e-6;
}

int rapl_find(const rapl_t *r, const char *name) {
    for (int d = 0; d < r->n; d++)
        if (strcmp(r->name[d], name) == 0) return d;
    return -1;
}

double pkg_temp_c(void) {
    glob_t g;
    double t = -1.0;
    if (glob("/sys/class/thermal/thermal_zone*", 0, NULL, &g) != 0) return t;
    for (size_t i = 0; i < g.gl_pathc; i++) {
        char p[512], type[64];
        unsigned long long v;
        snprintf(p, sizeof p, "%s/type", g.gl_pathv[i]);
        if (read_str(p, type, sizeof type) || strcmp(type, "x86_pkg_temp")) continue;
        snprintf(p, sizeof p, "%s/temp", g.gl_pathv[i]);
        if (read_ull(p, &v) == 0) t = v / 1000.0;
        break;
    }
    globfree(&g);
    return t;
}

long throttle_events(void) {
    glob_t g;
    long total = 0;
    unsigned long long v;
    if (read_ull("/sys/devices/system/cpu/cpu0/thermal_throttle/package_throttle_count", &v))
        return -1;
    total += (long)v;
    if (glob("/sys/devices/system/cpu/cpu[0-9]*/thermal_throttle/core_throttle_count", 0, NULL, &g) == 0) {
        for (size_t i = 0; i < g.gl_pathc; i++)
            if (read_ull(g.gl_pathv[i], &v) == 0) total += (long)v;
        globfree(&g);
    }
    return total;
}
