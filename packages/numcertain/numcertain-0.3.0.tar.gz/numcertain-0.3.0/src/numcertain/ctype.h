#pragma once

#include <math.h>
#include <stdbool.h>

typedef struct Uncertain {
  double nominal;
  double uncertainity;
} Uncertain_t;

Uncertain_t make_uncertain_longs(long nominal, long uncertainty);
Uncertain_t make_uncertain_long(long nominal);
Uncertain_t make_uncertain_doubles(double nominal, double uncertainty);
Uncertain_t make_uncertain_double(double nominal);
Uncertain_t uncertain_add(Uncertain_t a, Uncertain_t b);
Uncertain_t uncertain_subtract(Uncertain_t a, Uncertain_t b);
Uncertain_t uncertain_multiply(Uncertain_t a, Uncertain_t b);
Uncertain_t uncertain_divide(Uncertain_t a, Uncertain_t b);
bool uncertain_eq(Uncertain_t a, Uncertain_t b);
bool uncertain_ne(Uncertain_t a, Uncertain_t b);
double uncertain_nominal(Uncertain_t u);
double uncertain_uncertainty(Uncertain_t u);
double uncertain_double(Uncertain_t u);
long uncertain_long(Uncertain_t u);
int uncertain_nonzero(Uncertain_t u);
