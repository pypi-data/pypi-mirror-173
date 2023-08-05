#include "ctype.h"

Uncertain_t make_uncertain_longs(long nominal, long uncertainty) {
  Uncertain_t u = {nominal, uncertainty};
  return u;
};

Uncertain_t make_uncertain_long(long nominal) {
  return make_uncertain_longs(nominal, 0);
};

Uncertain_t make_uncertain_doubles(double nominal, double uncertainty) {
  Uncertain_t u = {nominal, uncertainty};
  return u;
};

Uncertain_t make_uncertain_double(double nominal) {
  return make_uncertain_doubles(nominal, 0);
};

Uncertain_t uncertain_add(Uncertain_t a, Uncertain_t b) {
  Uncertain_t result = {a.nominal + b.nominal,
                        hypot(a.uncertainity, b.uncertainity)};
  return result;
};

Uncertain_t uncertain_subtract(Uncertain_t a, Uncertain_t b) {
  Uncertain_t result = {a.nominal - b.nominal,
                        hypot(a.uncertainity, b.uncertainity)};
  return result;
};

Uncertain_t uncertain_multiply(Uncertain_t a, Uncertain_t b) {
  Uncertain_t result = {
      a.nominal * b.nominal,
      (a.nominal * b.nominal) *
          hypot(a.uncertainity / a.nominal, b.uncertainity / b.nominal)};
  return result;
};

Uncertain_t uncertain_divide(Uncertain_t a, Uncertain_t b) {
  Uncertain_t result = {
      a.nominal / b.nominal,
      (a.nominal / b.nominal) *
          hypot(a.uncertainity / a.nominal, b.uncertainity / b.nominal)};
  return result;
};

double uncertain_nominal(Uncertain_t u) { return u.nominal; };

double uncertain_uncertainty(Uncertain_t u) { return u.uncertainity; };

double uncertain_double(Uncertain_t u) { return u.nominal; };

long uncertain_long(Uncertain_t u) { return (long)u.nominal; };

bool uncertain_eq(Uncertain_t a, Uncertain_t b) {
  return a.nominal == b.nominal && a.uncertainity == b.uncertainity;
};

bool uncertain_ne(Uncertain_t a, Uncertain_t b) {
  return a.nominal != b.nominal || a.uncertainity != b.uncertainity;
};

int uncertain_nonzero(Uncertain_t u) {
  return u.nominal != 0 || u.uncertainity != 0;
};