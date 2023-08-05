// Copyright 2018 Ulf Adams
//
// The contents of this file may be used under the terms of the Apache License,
// Version 2.0.
//
//    (See accompanying file LICENSE-Apache or copy at
//     http://www.apache.org/licenses/LICENSE-2.0)
//
// Alternatively, the contents of this file may be used under the terms of
// the Boost Software License, Version 1.0.
//    (See accompanying file LICENSE-Boost or copy at
//     https://www.boost.org/LICENSE_1_0.txt)
//
// Unless required by applicable law or agreed to in writing, this software
// is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
// KIND, either express or implied.

// Defines HAS_UINT128 and uint128_t if applicable.
#include <stdbool.h>
#include "ryu/common.h"
#include "ryu/d2s_intrinsics.h"

static const uint64_t DOUBLE_POW5_INV_SPLIT2[15][2] = {
  {                    1u, 2305843009213693952u },
  {  5955668970331000884u, 1784059615882449851u },
  {  8982663654677661702u, 1380349269358112757u },
  {  7286864317269821294u, 2135987035920910082u },
  {  7005857020398200553u, 1652639921975621497u },
  { 17965325103354776697u, 1278668206209430417u },
  {  8928596168509315048u, 1978643211784836272u },
  { 10075671573058298858u, 1530901034580419511u },
  {   597001226353042382u, 1184477304306571148u },
  {  1527430471115325346u, 1832889850782397517u },
  { 12533209867169019542u, 1418129833677084982u },
  {  5577825024675947042u, 2194449627517475473u },
  { 11006974540203867551u, 1697873161311732311u },
  { 10313493231639821582u, 1313665730009899186u },
  { 12701016819766672773u, 2032799256770390445u }
};
static const uint32_t POW5_INV_OFFSETS[21] = {
  0x54544554, 0x04055545, 0x10041000, 0x00400414, 0x40010000, 0x41155555,
  0x00000454, 0x00010044, 0x40000000, 0x44000041, 0x50454450, 0x55550054,
  0x51655554, 0x40004000, 0x01000001, 0x00010500, 0x51515411, 0x05555554,
  0x00000000, 0x00000000, 0x00000000
};

static const uint64_t DOUBLE_POW5_SPLIT2[13][2] = {
  {                    0u, 1152921504606846976u },
  {                    0u, 1490116119384765625u },
  {  1032610780636961552u, 1925929944387235853u },
  {  7910200175544436838u, 1244603055572228341u },
  { 16941905809032713930u, 1608611746708759036u },
  { 13024893955298202172u, 2079081953128979843u },
  {  6607496772837067824u, 1343575221513417750u },
  { 17332926989895652603u, 1736530273035216783u },
  { 13037379183483547984u, 2244412773384604712u },
  {  1605989338741628675u, 1450417759929778918u },
  {  9630225068416591280u, 1874621017369538693u },
  {   665883850346957067u, 1211445438634777304u },
  { 14931890668723713708u, 1565756531257009982u }
};
static const uint32_t POW5_OFFSETS[21] = {
  0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x40000000, 0x59695995,
  0x55545555, 0x56555515, 0x41150504, 0x40555410, 0x44555145, 0x44504540,
  0x45555550, 0x40004000, 0x96440440, 0x55565565, 0x54454045, 0x40154151,
  0x55559155, 0x51405555, 0x00000105
};

#define POW5_TABLE_SIZE 26
static const uint64_t DOUBLE_POW5_TABLE[POW5_TABLE_SIZE] = {
1ull, 5ull, 25ull, 125ull, 625ull, 3125ull, 15625ull, 78125ull, 390625ull,
1953125ull, 9765625ull, 48828125ull, 244140625ull, 1220703125ull, 6103515625ull,
30517578125ull, 152587890625ull, 762939453125ull, 3814697265625ull,
19073486328125ull, 95367431640625ull, 476837158203125ull,
2384185791015625ull, 11920928955078125ull, 59604644775390625ull,
298023223876953125ull //, 1490116119384765625ull
};

uint32_t __pow5Factor(uint64_t value) {
  const uint64_t m_inv_5 = 14757395258967641293u; // 5 * m_inv_5 = 1 (mod 2^64)
  const uint64_t n_div_5 = 3689348814741910323u;  // #{ n | n = 0 (mod 2^64) } = 2^64 / 5
  uint32_t count = 0;
  for (;;) {
    assert(value != 0);
    value *= m_inv_5;
    if (value > n_div_5)
      break;
    ++count;
  }
  return count;
}

#if defined(HAS_UINT128)

// Computes 5^i in the form required by Ryu, and stores it in the given pointer.
void __double_computePow5(const uint32_t i, uint64_t* const result) {
  const uint32_t base = i / POW5_TABLE_SIZE;
  const uint32_t base2 = base * POW5_TABLE_SIZE;
  const uint32_t offset = i - base2;
  const uint64_t* const mul = DOUBLE_POW5_SPLIT2[base];
  if (offset == 0) {
    result[0] = mul[0];
    result[1] = mul[1];
    return;
  }
  const uint64_t m = DOUBLE_POW5_TABLE[offset];
  const uint128_t b0 = ((uint128_t) m) * mul[0];
  const uint128_t b2 = ((uint128_t) m) * mul[1];
  const uint32_t delta = pow5bits(i) - pow5bits(base2);
  const uint128_t shiftedSum = (b0 >> delta) + (b2 << (64 - delta)) + ((POW5_OFFSETS[i / 16] >> ((i % 16) << 1)) & 3);
  result[0] = (uint64_t) shiftedSum;
  result[1] = (uint64_t) (shiftedSum >> 64);
}

// Computes 5^-i in the form required by Ryu, and stores it in the given pointer.
void __double_computeInvPow5(const uint32_t i, uint64_t* const result) {
  const uint32_t base = (i + POW5_TABLE_SIZE - 1) / POW5_TABLE_SIZE;
  const uint32_t base2 = base * POW5_TABLE_SIZE;
  const uint32_t offset = base2 - i;
  const uint64_t* const mul = DOUBLE_POW5_INV_SPLIT2[base]; // 1/5^base2
  if (offset == 0) {
    result[0] = mul[0];
    result[1] = mul[1];
    return;
  }
  const uint64_t m = DOUBLE_POW5_TABLE[offset]; // 5^offset
  const uint128_t b0 = ((uint128_t) m) * (mul[0] - 1);
  const uint128_t b2 = ((uint128_t) m) * mul[1]; // 1/5^base2 * 5^offset = 1/5^(base2-offset) = 1/5^i
  const uint32_t delta = pow5bits(base2) - pow5bits(i);
  const uint128_t shiftedSum =
    ((b0 >> delta) + (b2 << (64 - delta))) + 1 + ((POW5_INV_OFFSETS[i / 16] >> ((i % 16) << 1)) & 3);
  result[0] = (uint64_t) shiftedSum;
  result[1] = (uint64_t) (shiftedSum >> 64);
}

#else // defined(HAS_UINT128)

// Computes 5^i in the form required by Ryu, and stores it in the given pointer.
void __double_computePow5(const uint32_t i, uint64_t* const result) {
  const uint32_t base = i / POW5_TABLE_SIZE;
  const uint32_t base2 = base * POW5_TABLE_SIZE;
  const uint32_t offset = i - base2;
  const uint64_t* const mul = DOUBLE_POW5_SPLIT2[base];
  if (offset == 0) {
    result[0] = mul[0];
    result[1] = mul[1];
    return;
  }
  const uint64_t m = DOUBLE_POW5_TABLE[offset];
  uint64_t high1;
  const uint64_t low1 = umul128(m, mul[1], &high1);
  uint64_t high0;
  const uint64_t low0 = umul128(m, mul[0], &high0);
  const uint64_t sum = high0 + low1;
  if (sum < high0) {
    ++high1; // overflow into high1
  }
  // high1 | sum | low0
  const uint32_t delta = pow5bits(i) - pow5bits(base2);
  result[0] = shiftright128(low0, sum, delta) + ((POW5_OFFSETS[i / 16] >> ((i % 16) << 1)) & 3);
  result[1] = shiftright128(sum, high1, delta);
}

// Computes 5^-i in the form required by Ryu, and stores it in the given pointer.
void __double_computeInvPow5(const uint32_t i, uint64_t* const result) {
  const uint32_t base = (i + POW5_TABLE_SIZE - 1) / POW5_TABLE_SIZE;
  const uint32_t base2 = base * POW5_TABLE_SIZE;
  const uint32_t offset = base2 - i;
  const uint64_t* const mul = DOUBLE_POW5_INV_SPLIT2[base]; // 1/5^base2
  if (offset == 0) {
    result[0] = mul[0];
    result[1] = mul[1];
    return;
  }
  const uint64_t m = DOUBLE_POW5_TABLE[offset];
  uint64_t high1;
  const uint64_t low1 = umul128(m, mul[1], &high1);
  uint64_t high0;
  const uint64_t low0 = umul128(m, mul[0] - 1, &high0);
  const uint64_t sum = high0 + low1;
  if (sum < high0) {
    ++high1; // overflow into high1
  }
  // high1 | sum | low0
  const uint32_t delta = pow5bits(base2) - pow5bits(i);
  result[0] = shiftright128(low0, sum, delta) + 1 + ((POW5_INV_OFFSETS[i / 16] >> ((i % 16) << 1)) & 3);
  result[1] = shiftright128(sum, high1, delta);
}

#endif // defined(HAS_UINT128)


