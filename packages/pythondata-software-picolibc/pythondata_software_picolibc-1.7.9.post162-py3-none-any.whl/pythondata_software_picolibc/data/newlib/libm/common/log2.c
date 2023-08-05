/* Double-precision log2(x) function.
   Copyright (c) 2018 Arm Ltd.  All rights reserved.

   SPDX-License-Identifier: BSD-3-Clause

   Redistribution and use in source and binary forms, with or without
   modification, are permitted provided that the following conditions
   are met:
   1. Redistributions of source code must retain the above copyright
      notice, this list of conditions and the following disclaimer.
   2. Redistributions in binary form must reproduce the above copyright
      notice, this list of conditions and the following disclaimer in the
      documentation and/or other materials provided with the distribution.
   3. The name of the company may not be used to endorse or promote
      products derived from this software without specific prior written
      permission.

   THIS SOFTWARE IS PROVIDED BY ARM LTD ``AS IS'' AND ANY EXPRESS OR IMPLIED
   WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
   MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
   IN NO EVENT SHALL ARM LTD BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
   SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED
   TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
   PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
   LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
   NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
   SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE. */

#include "fdlibm.h"
#if !__OBSOLETE_MATH_DOUBLE

#include <math.h>
#include <stdint.h>
#include "math_config.h"

#define T __log2_data.tab
#define T2 __log2_data.tab2
#define B __log2_data.poly1
#define A __log2_data.poly
#define InvLn2hi __log2_data.invln2hi
#define InvLn2lo __log2_data.invln2lo
#define N (1 << LOG2_TABLE_BITS)
#define OFF 0x3fe6000000000000

/* Top 16 bits of a double.  */
static inline uint32_t
top16 (double x)
{
  return asuint64 (x) >> 48;
}

double
(log2) (double x)
{
  /* double_t for better performance on targets with FLT_EVAL_METHOD==2.  */
  double_t z, r, r2, r4, y, invc, logc, kd, hi, lo, t1, t2, t3, p;
  uint64_t ix, iz, tmp;
  uint32_t top;
  int k, i;

  ix = asuint64 (x);
  top = top16 (x);

#if LOG2_POLY1_ORDER == 11
# define LO asuint64 (1.0 - 0x1.5b51p-5)
# define HI asuint64 (1.0 + 0x1.6ab2p-5)
#endif
  if (unlikely (ix - LO < HI - LO))
    {
      /* Handle close to 1.0 inputs separately.  */
      /* Fix sign of zero with downward rounding when x==1.  */
      if (WANT_ROUNDING && unlikely (ix == asuint64 (1.0)))
	return 0;
      r = x - 1.0;
#if _HAVE_FAST_FMA
      hi = r * InvLn2hi;
      lo = r * InvLn2lo + fma (r, InvLn2hi, -hi);
#else
      double_t rhi, rlo;
      rhi = asdouble (asuint64 (r) & -1ULL << 32);
      rlo = r - rhi;
      hi = rhi * InvLn2hi;
      lo = rlo * InvLn2hi + r * InvLn2lo;
#endif
      r2 = r * r; /* rounding error: 0x1p-62.  */
      r4 = r2 * r2;
#if LOG2_POLY1_ORDER == 11
      /* Worst-case error is less than 0.54 ULP (0.55 ULP without fma).  */
      p = r2 * (B[0] + r * B[1]);
      y = hi + p;
      lo += hi - y + p;
      lo += r4 * (B[2] + r * B[3] + r2 * (B[4] + r * B[5])
		  + r4 * (B[6] + r * B[7] + r2 * (B[8] + r * B[9])));
      y += lo;
#endif
      return y;
    }
  if (unlikely (top - 0x0010 >= 0x7ff0 - 0x0010))
    {
      /* x < 0x1p-1022 or inf or nan.  */
      if (ix * 2 == 0)
	return __math_divzero (1);
      if (ix == asuint64 ((double) INFINITY)) /* log(inf) == inf.  */
	return x;
      if ((top & 0x8000) || (top & 0x7ff0) == 0x7ff0)
	return __math_invalid (x);
      /* x is subnormal, normalize it.  */
      ix = asuint64 (x * 0x1p52);
      ix -= 52ULL << 52;
    }

  /* x = 2^k z; where z is in range [OFF,2*OFF) and exact.
     The range is split into N subintervals.
     The ith subinterval contains z and c is near its center.  */
  tmp = ix - OFF;
  i = (tmp >> (52 - LOG2_TABLE_BITS)) % N;
  k = (int64_t) tmp >> 52; /* arithmetic shift */
  iz = ix - (tmp & 0xfffULL << 52);
  invc = T[i].invc;
  logc = T[i].logc;
  z = asdouble (iz);
  kd = (double_t) k;

  /* log2(x) = log2(z/c) + log2(c) + k.  */
  /* r ~= z/c - 1, |r| < 1/(2*N).  */
#if _HAVE_FAST_FMA
  /* rounding error: 0x1p-55/N.  */
  r = fma (z, invc, -1.0);
  t1 = r * InvLn2hi;
  t2 = r * InvLn2lo + fma (r, InvLn2hi, -t1);
#else
  double_t rhi, rlo;
  /* rounding error: 0x1p-55/N + 0x1p-65.  */
  r = (z - T2[i].chi - T2[i].clo) * invc;
  rhi = asdouble (asuint64 (r) & -1ULL << 32);
  rlo = r - rhi;
  t1 = rhi * InvLn2hi;
  t2 = rlo * InvLn2hi + r * InvLn2lo;
#endif

  /* hi + lo = r/ln2 + log2(c) + k.  */
  t3 = kd + logc;
  hi = t3 + t1;
  lo = t3 - hi + t1 + t2;

  /* log2(r+1) = r/ln2 + r^2*poly(r).  */
  /* Evaluation is optimized assuming superscalar pipelined execution.  */
  r2 = r * r; /* rounding error: 0x1p-54/N^2.  */
  r4 = r2 * r2;
#if LOG2_POLY_ORDER == 7
  /* Worst-case error if |y| > 0x1p-4: 0.547 ULP (0.550 ULP without fma).
     ~ 0.5 + 2/N/ln2 + abs-poly-error*0x1p56 ULP (+ 0.003 ULP without fma).  */
  p = A[0] + r * A[1] + r2 * (A[2] + r * A[3]) + r4 * (A[4] + r * A[5]);
  y = lo + r2 * p + hi;
#endif
  return y;
}
#endif
