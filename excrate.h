#ifndef EXCRATE_H
#define EXCRATE_H

#include <sys/poll.h>
#include <sys/types.h>

#include "external.h"
#include "list.h"
#include "library.h"

struct excrate {
    struct list excrates;
    unsigned int refcount;

    /* State of the external scan process */

    struct list rig;
    pid_t pid;
    int fd;
    struct pollfd *pe;

    /* State of reader */

    struct rb rb;
    struct crate *target;
};

struct excrate* excrate_get_by_scan(const char *script, const char *search,
                                    struct crate *target);

void excrate_get(struct excrate *e);
void excrate_put(struct excrate *e);

/* Used by the rig and main thread */

void excrate_pollfd(struct excrate *tr, struct pollfd *pe);
void excrate_handle(struct excrate *tr);

#endif
