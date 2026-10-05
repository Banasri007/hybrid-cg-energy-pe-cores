#ifndef RAPL_H
#define RAPL_H

/* Intel RAPL via the powercap sysfs interface (per Raffin & Trystram: prefer
 * powercap/perf over raw MSR). Domains on the i5-13500H: package-0, core,
 * uncore, psys. There is no DRAM domain on this mobile part. */

#define RAPL_MAXDOM 8

typedef struct {
    int n;
    char name[RAPL_MAXDOM][32];
    char path[RAPL_MAXDOM][512];
    unsigned long long max_uj[RAPL_MAXDOM];   /* wraparound range */
} rapl_t;

/* Discover readable domains. Returns how many (0 if energy_uj is not
 * readable, e.g. root-only permissions). */
int rapl_init(rapl_t *r);
/* Snapshot all domains into uj[]. Returns 0 on success. */
int rapl_read(const rapl_t *r, unsigned long long *uj);
/* Joules between two snapshots of domain d, handling one counter wrap. */
double rapl_joules(const rapl_t *r, int d, unsigned long long a, unsigned long long b);
/* Index of domain by name ("package-0", "core", "uncore", "psys"), or -1. */
int rapl_find(const rapl_t *r, const char *name);

/* Package temperature in deg C from the x86_pkg_temp thermal zone, or -1. */
double pkg_temp_c(void);
/* Sum of package + per-core thermal throttle event counters (any increase
 * during a run means it was throttled). -1 if unavailable. */
long throttle_events(void);

#endif
