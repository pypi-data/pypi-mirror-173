/*
 * Copyright (c) 1994 Cygnus Support.
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms are permitted
 * provided that the above copyright notice and this paragraph are
 * duplicated in all such forms and that any documentation,
 * and/or other materials related to such
 * distribution and use acknowledge that the software was developed
 * at Cygnus Support, Inc.  Cygnus Support, Inc. may not be used to
 * endorse or promote products derived from this software without
 * specific prior written permission.
 * THIS SOFTWARE IS PROVIDED ``AS IS'' AND WITHOUT ANY EXPRESS OR
 * IMPLIED WARRANTIES, INCLUDING, WITHOUT LIMITATION, THE IMPLIED
 * WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.
 */
#include "test.h"
 one_line_type tanf_vec[] = {
{40, 0,123,__LINE__, 0xc00493c4, 0x60000000, 0xbff33333, 0x33333333},	/* -2.57215=f(-1.2)*/
{37, 0,123,__LINE__, 0xc003fbb2, 0xe0000000, 0xbff30a3d, 0x70a3d70a},	/* -2.4979=f(-1.19)*/
{36, 0,123,__LINE__, 0xc0036b0a, 0x60000000, 0xbff2e147, 0xae147ae1},	/* -2.42727=f(-1.18)*/
{42, 0,123,__LINE__, 0xc002e13d, 0xa0000000, 0xbff2b851, 0xeb851eb8},	/* -2.35998=f(-1.17)*/
{36, 0,123,__LINE__, 0xc0025dcb, 0x80000000, 0xbff28f5c, 0x28f5c28f},	/* -2.2958=f(-1.16)*/
{36, 0,123,__LINE__, 0xc001e03f, 0xe0000000, 0xbff26666, 0x66666666},	/* -2.2345=f(-1.15)*/
{38, 0,123,__LINE__, 0xc0016831, 0x20000000, 0xbff23d70, 0xa3d70a3d},	/* -2.17587=f(-1.14)*/
{36, 0,123,__LINE__, 0xc000f53f, 0x80000000, 0xbff2147a, 0xe147ae14},	/* -2.11975=f(-1.13)*/
{36, 0,123,__LINE__, 0xc0008713, 0x80000000, 0xbff1eb85, 0x1eb851eb},	/* -2.06596=f(-1.12)*/
{40, 0,123,__LINE__, 0xc0001d5d, 0x60000000, 0xbff1c28f, 0x5c28f5c2},	/* -2.01434=f(-1.11)*/
{36, 0,123,__LINE__, 0xbfff6fa7, 0xe0000000, 0xbff19999, 0x99999999},	/* -1.96476=f(-1.1)*/
{38, 0,123,__LINE__, 0xbffeac68, 0xa0000000, 0xbff170a3, 0xd70a3d70},	/* -1.91709=f(-1.09)*/
{34, 0,123,__LINE__, 0xbffdf081, 0xc0000000, 0xbff147ae, 0x147ae147},	/* -1.87122=f(-1.08)*/
{34, 0,123,__LINE__, 0xbffd3b82, 0x20000000, 0xbff11eb8, 0x51eb851e},	/* -1.82703=f(-1.07)*/
{35, 0,123,__LINE__, 0xbffc8d00, 0xc0000000, 0xbff0f5c2, 0x8f5c28f5},	/* -1.78442=f(-1.06)*/
{34, 0,123,__LINE__, 0xbffbe49e, 0x60000000, 0xbff0cccc, 0xcccccccc},	/* -1.74332=f(-1.05)*/
{36, 0,123,__LINE__, 0xbffb4201, 0x40000000, 0xbff0a3d7, 0x0a3d70a3},	/* -1.70361=f(-1.04)*/
{35, 0,123,__LINE__, 0xbffaa4d6, 0xc0000000, 0xbff07ae1, 0x47ae147a},	/* -1.66524=f(-1.03)*/
{35, 0,123,__LINE__, 0xbffa0cd2, 0x60000000, 0xbff051eb, 0x851eb851},	/* -1.62813=f(-1.02)*/
{36, 0,123,__LINE__, 0xbff979ad, 0x00000000, 0xbff028f5, 0xc28f5c28},	/* -1.59221=f(-1.01)*/
{36, 0,123,__LINE__, 0xbff8eb24, 0x60000000, 0xbfefffff, 0xfffffffe},	/* -1.55741=f(-1)*/
{35, 0,123,__LINE__, 0xbff860fa, 0xe0000000, 0xbfefae14, 0x7ae147ac},	/* -1.52368=f(-0.99)*/
{37, 0,123,__LINE__, 0xbff7daf7, 0x20000000, 0xbfef5c28, 0xf5c28f5a},	/* -1.49096=f(-0.98)*/
{38, 0,123,__LINE__, 0xbff758e3, 0x60000000, 0xbfef0a3d, 0x70a3d708},	/* -1.4592=f(-0.97)*/
{35, 0,123,__LINE__, 0xbff6da8d, 0x60000000, 0xbfeeb851, 0xeb851eb6},	/* -1.42836=f(-0.96)*/
{35, 0,123,__LINE__, 0xbff65fc6, 0x60000000, 0xbfee6666, 0x66666664},	/* -1.39838=f(-0.95)*/
{35, 0,123,__LINE__, 0xbff5e862, 0x60000000, 0xbfee147a, 0xe147ae12},	/* -1.36923=f(-0.94)*/
{36, 0,123,__LINE__, 0xbff57438, 0x20000000, 0xbfedc28f, 0x5c28f5c0},	/* -1.34087=f(-0.93)*/
{38, 0,123,__LINE__, 0xbff50320, 0xe0000000, 0xbfed70a3, 0xd70a3d6e},	/* -1.31326=f(-0.92)*/
{38, 0,123,__LINE__, 0xbff494f8, 0x20000000, 0xbfed1eb8, 0x51eb851c},	/* -1.28637=f(-0.91)*/
{35, 0,123,__LINE__, 0xbff4299b, 0xa0000000, 0xbfeccccc, 0xccccccca},	/* -1.26016=f(-0.9)*/
{38, 0,123,__LINE__, 0xbff3c0eb, 0x60000000, 0xbfec7ae1, 0x47ae1478},	/* -1.2346=f(-0.89)*/
{36, 0,123,__LINE__, 0xbff35ac8, 0xc0000000, 0xbfec28f5, 0xc28f5c26},	/* -1.20966=f(-0.88)*/
{35, 0,123,__LINE__, 0xbff2f717, 0x40000000, 0xbfebd70a, 0x3d70a3d4},	/* -1.18532=f(-0.87)*/
{35, 0,123,__LINE__, 0xbff295bb, 0xa0000000, 0xbfeb851e, 0xb851eb82},	/* -1.16156=f(-0.86)*/
{35, 0,123,__LINE__, 0xbff2369c, 0x60000000, 0xbfeb3333, 0x33333330},	/* -1.13833=f(-0.85)*/
{36, 0,123,__LINE__, 0xbff1d9a1, 0x40000000, 0xbfeae147, 0xae147ade},	/* -1.11563=f(-0.84)*/
{35, 0,123,__LINE__, 0xbff17eb3, 0x80000000, 0xbfea8f5c, 0x28f5c28c},	/* -1.09343=f(-0.83)*/
{36, 0,123,__LINE__, 0xbff125bd, 0x40000000, 0xbfea3d70, 0xa3d70a3a},	/* -1.07171=f(-0.82)*/
{35, 0,123,__LINE__, 0xbff0ceaa, 0x00000000, 0xbfe9eb85, 0x1eb851e8},	/* -1.05046=f(-0.81)*/
{35, 0,123,__LINE__, 0xbff07966, 0x40000000, 0xbfe99999, 0x99999996},	/* -1.02964=f(-0.8)*/
{35, 0,123,__LINE__, 0xbff025df, 0x80000000, 0xbfe947ae, 0x147ae144},	/* -1.00925=f(-0.79)*/
{36, 0,123,__LINE__, 0xbfefa807, 0xc0000000, 0xbfe8f5c2, 0x8f5c28f2},	/* -0.989262=f(-0.78)*/
{34, 0,123,__LINE__, 0xbfef0785, 0xc0000000, 0xbfe8a3d7, 0x0a3d70a0},	/* -0.969668=f(-0.77)*/
{37, 0,123,__LINE__, 0xbfee6a19, 0x20000000, 0xbfe851eb, 0x851eb84e},	/* -0.950451=f(-0.76)*/
{36, 0,123,__LINE__, 0xbfedcfa3, 0x60000000, 0xbfe7ffff, 0xfffffffc},	/* -0.931596=f(-0.75)*/
{38, 0,123,__LINE__, 0xbfed3807, 0xa0000000, 0xbfe7ae14, 0x7ae147aa},	/* -0.91309=f(-0.74)*/
{37, 0,123,__LINE__, 0xbfeca32a, 0x20000000, 0xbfe75c28, 0xf5c28f58},	/* -0.894918=f(-0.73)*/
{35, 0,123,__LINE__, 0xbfec10f0, 0xc0000000, 0xbfe70a3d, 0x70a3d706},	/* -0.877068=f(-0.72)*/
{36, 0,123,__LINE__, 0xbfeb8142, 0x20000000, 0xbfe6b851, 0xeb851eb4},	/* -0.859529=f(-0.71)*/
{36, 0,123,__LINE__, 0xbfeaf406, 0xc0000000, 0xbfe66666, 0x66666662},	/* -0.842288=f(-0.7)*/
{36, 0,123,__LINE__, 0xbfea6927, 0x40000000, 0xbfe6147a, 0xe147ae10},	/* -0.825336=f(-0.69)*/
{35, 0,123,__LINE__, 0xbfe9e08d, 0xe0000000, 0xbfe5c28f, 0x5c28f5be},	/* -0.808661=f(-0.68)*/
{38, 0,123,__LINE__, 0xbfe95a25, 0x80000000, 0xbfe570a3, 0xd70a3d6c},	/* -0.792254=f(-0.67)*/
{35, 0,123,__LINE__, 0xbfe8d5da, 0x20000000, 0xbfe51eb8, 0x51eb851a},	/* -0.776105=f(-0.66)*/
{40, 0,123,__LINE__, 0xbfe85398, 0x20000000, 0xbfe4cccc, 0xccccccc8},	/* -0.760204=f(-0.65)*/
{35, 0,123,__LINE__, 0xbfe7d34d, 0x80000000, 0xbfe47ae1, 0x47ae1476},	/* -0.744544=f(-0.64)*/
{35, 0,123,__LINE__, 0xbfe754e8, 0x60000000, 0xbfe428f5, 0xc28f5c24},	/* -0.729115=f(-0.63)*/
{35, 0,123,__LINE__, 0xbfe6d857, 0xc0000000, 0xbfe3d70a, 0x3d70a3d2},	/* -0.713909=f(-0.62)*/
{35, 0,123,__LINE__, 0xbfe65d8b, 0x20000000, 0xbfe3851e, 0xb851eb80},	/* -0.698919=f(-0.61)*/
{36, 0,123,__LINE__, 0xbfe5e473, 0x00000000, 0xbfe33333, 0x3333332e},	/* -0.684137=f(-0.6)*/
{35, 0,123,__LINE__, 0xbfe56cff, 0xe0000000, 0xbfe2e147, 0xae147adc},	/* -0.669556=f(-0.59)*/
{36, 0,123,__LINE__, 0xbfe4f723, 0xc0000000, 0xbfe28f5c, 0x28f5c28a},	/* -0.655168=f(-0.58)*/
{37, 0,123,__LINE__, 0xbfe482d0, 0x80000000, 0xbfe23d70, 0xa3d70a38},	/* -0.640969=f(-0.57)*/
{37, 0,123,__LINE__, 0xbfe40ff8, 0x80000000, 0xbfe1eb85, 0x1eb851e6},	/* -0.62695=f(-0.56)*/
{38, 0,123,__LINE__, 0xbfe39e8e, 0xe0000000, 0xbfe19999, 0x99999994},	/* -0.613105=f(-0.55)*/
{36, 0,123,__LINE__, 0xbfe32e87, 0x20000000, 0xbfe147ae, 0x147ae142},	/* -0.59943=f(-0.54)*/
{39, 0,123,__LINE__, 0xbfe2bfd5, 0x00000000, 0xbfe0f5c2, 0x8f5c28f0},	/* -0.585917=f(-0.53)*/
{35, 0,123,__LINE__, 0xbfe2526d, 0x20000000, 0xbfe0a3d7, 0x0a3d709e},	/* -0.572562=f(-0.52)*/
{35, 0,123,__LINE__, 0xbfe1e644, 0x40000000, 0xbfe051eb, 0x851eb84c},	/* -0.559359=f(-0.51)*/
{36, 0,123,__LINE__, 0xbfe17b4f, 0x60000000, 0xbfdfffff, 0xfffffff4},	/* -0.546302=f(-0.5)*/
{40, 0,123,__LINE__, 0xbfe11184, 0x00000000, 0xbfdf5c28, 0xf5c28f50},	/* -0.533388=f(-0.49)*/
{36, 0,123,__LINE__, 0xbfe0a8d8, 0x00000000, 0xbfdeb851, 0xeb851eac},	/* -0.520611=f(-0.48)*/
{36, 0,123,__LINE__, 0xbfe04141, 0xc0000000, 0xbfde147a, 0xe147ae08},	/* -0.507966=f(-0.47)*/
{36, 0,123,__LINE__, 0xbfdfb56e, 0xc0000000, 0xbfdd70a3, 0xd70a3d64},	/* -0.495449=f(-0.46)*/
{35, 0,123,__LINE__, 0xbfdeea5f, 0xc0000000, 0xbfdccccc, 0xccccccc0},	/* -0.483055=f(-0.45)*/
{36, 0,123,__LINE__, 0xbfde2144, 0xa0000000, 0xbfdc28f5, 0xc28f5c1c},	/* -0.470781=f(-0.44)*/
{38, 0,123,__LINE__, 0xbfdd5a0c, 0x00000000, 0xbfdb851e, 0xb851eb78},	/* -0.458621=f(-0.43)*/
{36, 0,123,__LINE__, 0xbfdc94a5, 0x00000000, 0xbfdae147, 0xae147ad4},	/* -0.446573=f(-0.42)*/
{45, 0,123,__LINE__, 0xbfdbd0ff, 0x60000000, 0xbfda3d70, 0xa3d70a30},	/* -0.434631=f(-0.41)*/
{35, 0,123,__LINE__, 0xbfdb0f0b, 0x60000000, 0xbfd99999, 0x9999998c},	/* -0.422793=f(-0.4)*/
{43, 0,123,__LINE__, 0xbfda4eb9, 0x40000000, 0xbfd8f5c2, 0x8f5c28e8},	/* -0.411055=f(-0.39)*/
{35, 0,123,__LINE__, 0xbfd98ffa, 0x60000000, 0xbfd851eb, 0x851eb844},	/* -0.399413=f(-0.38)*/
{37, 0,123,__LINE__, 0xbfd8d2c0, 0x00000000, 0xbfd7ae14, 0x7ae147a0},	/* -0.387863=f(-0.37)*/
{37, 0,123,__LINE__, 0xbfd816fc, 0x00000000, 0xbfd70a3d, 0x70a3d6fc},	/* -0.376403=f(-0.36)*/
{38, 0,123,__LINE__, 0xbfd75ca0, 0x80000000, 0xbfd66666, 0x66666658},	/* -0.365029=f(-0.35)*/
{36, 0,123,__LINE__, 0xbfd6a3a0, 0x00000000, 0xbfd5c28f, 0x5c28f5b4},	/* -0.353737=f(-0.34)*/
{39, 0,123,__LINE__, 0xbfd5ebed, 0x80000000, 0xbfd51eb8, 0x51eb8510},	/* -0.342525=f(-0.33)*/
{37, 0,123,__LINE__, 0xbfd5357b, 0xe0000000, 0xbfd47ae1, 0x47ae146c},	/* -0.331389=f(-0.32)*/
{35, 0,123,__LINE__, 0xbfd4803f, 0x00000000, 0xbfd3d70a, 0x3d70a3c8},	/* -0.320328=f(-0.31)*/
{37, 0,123,__LINE__, 0xbfd3cc2a, 0x60000000, 0xbfd33333, 0x33333324},	/* -0.309336=f(-0.3)*/
{41, 0,123,__LINE__, 0xbfd31931, 0xe0000000, 0xbfd28f5c, 0x28f5c280},	/* -0.298413=f(-0.29)*/
{36, 0,123,__LINE__, 0xbfd2674a, 0x40000000, 0xbfd1eb85, 0x1eb851dc},	/* -0.287554=f(-0.28)*/
{38, 0,123,__LINE__, 0xbfd1b667, 0xc0000000, 0xbfd147ae, 0x147ae138},	/* -0.276758=f(-0.27)*/
{38, 0,123,__LINE__, 0xbfd1067f, 0x20000000, 0xbfd0a3d7, 0x0a3d7094},	/* -0.266022=f(-0.26)*/
{38, 0,123,__LINE__, 0xbfd05785, 0xa0000000, 0xbfcfffff, 0xffffffe0},	/* -0.255342=f(-0.25)*/
{36, 0,123,__LINE__, 0xbfcf52e0, 0x80000000, 0xbfceb851, 0xeb851e98},	/* -0.244717=f(-0.24)*/
{39, 0,123,__LINE__, 0xbfcdf868, 0xe0000000, 0xbfcd70a3, 0xd70a3d50},	/* -0.234143=f(-0.23)*/
{36, 0,123,__LINE__, 0xbfcc9f8f, 0xa0000000, 0xbfcc28f5, 0xc28f5c08},	/* -0.223619=f(-0.22)*/
{39, 0,123,__LINE__, 0xbfcb4840, 0x60000000, 0xbfcae147, 0xae147ac0},	/* -0.213142=f(-0.21)*/
{35, 0,123,__LINE__, 0xbfc9f267, 0x00000000, 0xbfc99999, 0x99999978},	/* -0.20271=f(-0.2)*/
{36, 0,123,__LINE__, 0xbfc89def, 0xc0000000, 0xbfc851eb, 0x851eb830},	/* -0.19232=f(-0.19)*/
{39, 0,123,__LINE__, 0xbfc74ac7, 0x20000000, 0xbfc70a3d, 0x70a3d6e8},	/* -0.18197=f(-0.18)*/
{36, 0,123,__LINE__, 0xbfc5f8d9, 0xc0000000, 0xbfc5c28f, 0x5c28f5a0},	/* -0.171657=f(-0.17)*/
{39, 0,123,__LINE__, 0xbfc4a815, 0x00000000, 0xbfc47ae1, 0x47ae1458},	/* -0.161379=f(-0.16)*/
{37, 0,123,__LINE__, 0xbfc35866, 0x20000000, 0xbfc33333, 0x33333310},	/* -0.151135=f(-0.15)*/
{36, 0,123,__LINE__, 0xbfc209ba, 0x80000000, 0xbfc1eb85, 0x1eb851c8},	/* -0.140922=f(-0.14)*/
{38, 0,123,__LINE__, 0xbfc0bc00, 0x20000000, 0xbfc0a3d7, 0x0a3d7080},	/* -0.130737=f(-0.13)*/
{35, 0,123,__LINE__, 0xbfbede49, 0x80000000, 0xbfbeb851, 0xeb851e71},	/* -0.120579=f(-0.12)*/
{34, 0,123,__LINE__, 0xbfbc462d, 0x80000000, 0xbfbc28f5, 0xc28f5be2},	/* -0.110446=f(-0.11)*/
{36, 0,123,__LINE__, 0xbfb9af88, 0x80000000, 0xbfb99999, 0x99999953},	/* -0.100335=f(-0.1)*/
{37, 0,123,__LINE__, 0xbfb71a37, 0xa0000000, 0xbfb70a3d, 0x70a3d6c4},	/* -0.0902438=f(-0.09)*/
{41, 0,123,__LINE__, 0xbfb48617, 0xe0000000, 0xbfb47ae1, 0x47ae1435},	/* -0.0801711=f(-0.08)*/
{36, 0,123,__LINE__, 0xbfb1f307, 0x20000000, 0xbfb1eb85, 0x1eb851a6},	/* -0.0701146=f(-0.07)*/
{37, 0,123,__LINE__, 0xbfaec1c5, 0x40000000, 0xbfaeb851, 0xeb851e2d},	/* -0.0600721=f(-0.06)*/
{36, 0,123,__LINE__, 0xbfa99f11, 0x20000000, 0xbfa99999, 0x9999990e},	/* -0.0500417=f(-0.05)*/
{35, 0,123,__LINE__, 0xbfa47dad, 0x80000000, 0xbfa47ae1, 0x47ae13ef},	/* -0.0400213=f(-0.04)*/
{37, 0,123,__LINE__, 0xbf9ebaae, 0x20000000, 0xbf9eb851, 0xeb851da0},	/* -0.030009=f(-0.03)*/
{36, 0,123,__LINE__, 0xbf947b94, 0x40000000, 0xbf947ae1, 0x47ae1362},	/* -0.0200027=f(-0.02)*/
{37, 0,123,__LINE__, 0xbf847b0e, 0x00000000, 0xbf847ae1, 0x47ae1249},	/* -0.0100003=f(-0.01)*/
{64, 0,123,__LINE__, 0x3cd19000, 0x00000000, 0x3cd19000, 0x00000000},	/* 9.74915e-16=f(9.74915e-16)*/
{37, 0,123,__LINE__, 0x3f847b0e, 0x00000000, 0x3f847ae1, 0x47ae16ad},	/* 0.0100003=f(0.01)*/
{36, 0,123,__LINE__, 0x3f947b94, 0x40000000, 0x3f947ae1, 0x47ae1594},	/* 0.0200027=f(0.02)*/
{37, 0,123,__LINE__, 0x3f9ebaae, 0x20000000, 0x3f9eb851, 0xeb851fd2},	/* 0.030009=f(0.03)*/
{35, 0,123,__LINE__, 0x3fa47dad, 0x80000000, 0x3fa47ae1, 0x47ae1508},	/* 0.0400213=f(0.04)*/
{36, 0,123,__LINE__, 0x3fa99f11, 0x20000000, 0x3fa99999, 0x99999a27},	/* 0.0500417=f(0.05)*/
{37, 0,123,__LINE__, 0x3faec1c5, 0x40000000, 0x3faeb851, 0xeb851f46},	/* 0.0600721=f(0.06)*/
{36, 0,123,__LINE__, 0x3fb1f307, 0x20000000, 0x3fb1eb85, 0x1eb85232},	/* 0.0701146=f(0.07)*/
{41, 0,123,__LINE__, 0x3fb48617, 0xe0000000, 0x3fb47ae1, 0x47ae14c1},	/* 0.0801711=f(0.08)*/
{37, 0,123,__LINE__, 0x3fb71a37, 0xa0000000, 0x3fb70a3d, 0x70a3d750},	/* 0.0902438=f(0.09)*/
{36, 0,123,__LINE__, 0x3fb9af88, 0x80000000, 0x3fb99999, 0x999999df},	/* 0.100335=f(0.1)*/
{34, 0,123,__LINE__, 0x3fbc462d, 0x80000000, 0x3fbc28f5, 0xc28f5c6e},	/* 0.110446=f(0.11)*/
{35, 0,123,__LINE__, 0x3fbede49, 0x80000000, 0x3fbeb851, 0xeb851efd},	/* 0.120579=f(0.12)*/
{38, 0,123,__LINE__, 0x3fc0bc00, 0x20000000, 0x3fc0a3d7, 0x0a3d70c6},	/* 0.130737=f(0.13)*/
{36, 0,123,__LINE__, 0x3fc209ba, 0x80000000, 0x3fc1eb85, 0x1eb8520e},	/* 0.140922=f(0.14)*/
{37, 0,123,__LINE__, 0x3fc35866, 0x20000000, 0x3fc33333, 0x33333356},	/* 0.151135=f(0.15)*/
{39, 0,123,__LINE__, 0x3fc4a815, 0x00000000, 0x3fc47ae1, 0x47ae149e},	/* 0.161379=f(0.16)*/
{36, 0,123,__LINE__, 0x3fc5f8d9, 0xc0000000, 0x3fc5c28f, 0x5c28f5e6},	/* 0.171657=f(0.17)*/
{39, 0,123,__LINE__, 0x3fc74ac7, 0x20000000, 0x3fc70a3d, 0x70a3d72e},	/* 0.18197=f(0.18)*/
{36, 0,123,__LINE__, 0x3fc89def, 0xc0000000, 0x3fc851eb, 0x851eb876},	/* 0.19232=f(0.19)*/
{35, 0,123,__LINE__, 0x3fc9f267, 0x00000000, 0x3fc99999, 0x999999be},	/* 0.20271=f(0.2)*/
{39, 0,123,__LINE__, 0x3fcb4840, 0x60000000, 0x3fcae147, 0xae147b06},	/* 0.213142=f(0.21)*/
{36, 0,123,__LINE__, 0x3fcc9f8f, 0xa0000000, 0x3fcc28f5, 0xc28f5c4e},	/* 0.223619=f(0.22)*/
{39, 0,123,__LINE__, 0x3fcdf868, 0xe0000000, 0x3fcd70a3, 0xd70a3d96},	/* 0.234143=f(0.23)*/
{36, 0,123,__LINE__, 0x3fcf52e0, 0x80000000, 0x3fceb851, 0xeb851ede},	/* 0.244717=f(0.24)*/
{38, 0,123,__LINE__, 0x3fd05785, 0xa0000000, 0x3fd00000, 0x00000013},	/* 0.255342=f(0.25)*/
{38, 0,123,__LINE__, 0x3fd1067f, 0x20000000, 0x3fd0a3d7, 0x0a3d70b7},	/* 0.266022=f(0.26)*/
{38, 0,123,__LINE__, 0x3fd1b667, 0xc0000000, 0x3fd147ae, 0x147ae15b},	/* 0.276758=f(0.27)*/
{36, 0,123,__LINE__, 0x3fd2674a, 0x40000000, 0x3fd1eb85, 0x1eb851ff},	/* 0.287554=f(0.28)*/
{41, 0,123,__LINE__, 0x3fd31931, 0xe0000000, 0x3fd28f5c, 0x28f5c2a3},	/* 0.298413=f(0.29)*/
{37, 0,123,__LINE__, 0x3fd3cc2a, 0x60000000, 0x3fd33333, 0x33333347},	/* 0.309336=f(0.3)*/
{35, 0,123,__LINE__, 0x3fd4803f, 0x00000000, 0x3fd3d70a, 0x3d70a3eb},	/* 0.320328=f(0.31)*/
{37, 0,123,__LINE__, 0x3fd5357b, 0xe0000000, 0x3fd47ae1, 0x47ae148f},	/* 0.331389=f(0.32)*/
{39, 0,123,__LINE__, 0x3fd5ebed, 0x80000000, 0x3fd51eb8, 0x51eb8533},	/* 0.342525=f(0.33)*/
{36, 0,123,__LINE__, 0x3fd6a3a0, 0x00000000, 0x3fd5c28f, 0x5c28f5d7},	/* 0.353737=f(0.34)*/
{38, 0,123,__LINE__, 0x3fd75ca0, 0x80000000, 0x3fd66666, 0x6666667b},	/* 0.365029=f(0.35)*/
{37, 0,123,__LINE__, 0x3fd816fc, 0x00000000, 0x3fd70a3d, 0x70a3d71f},	/* 0.376403=f(0.36)*/
{37, 0,123,__LINE__, 0x3fd8d2c0, 0x00000000, 0x3fd7ae14, 0x7ae147c3},	/* 0.387863=f(0.37)*/
{35, 0,123,__LINE__, 0x3fd98ffa, 0x60000000, 0x3fd851eb, 0x851eb867},	/* 0.399413=f(0.38)*/
{43, 0,123,__LINE__, 0x3fda4eb9, 0x40000000, 0x3fd8f5c2, 0x8f5c290b},	/* 0.411055=f(0.39)*/
{35, 0,123,__LINE__, 0x3fdb0f0b, 0x60000000, 0x3fd99999, 0x999999af},	/* 0.422793=f(0.4)*/
{45, 0,123,__LINE__, 0x3fdbd0ff, 0x60000000, 0x3fda3d70, 0xa3d70a53},	/* 0.434631=f(0.41)*/
{36, 0,123,__LINE__, 0x3fdc94a5, 0x00000000, 0x3fdae147, 0xae147af7},	/* 0.446573=f(0.42)*/
{38, 0,123,__LINE__, 0x3fdd5a0c, 0x00000000, 0x3fdb851e, 0xb851eb9b},	/* 0.458621=f(0.43)*/
{36, 0,123,__LINE__, 0x3fde2144, 0xa0000000, 0x3fdc28f5, 0xc28f5c3f},	/* 0.470781=f(0.44)*/
{35, 0,123,__LINE__, 0x3fdeea5f, 0xc0000000, 0x3fdccccc, 0xcccccce3},	/* 0.483055=f(0.45)*/
{36, 0,123,__LINE__, 0x3fdfb56e, 0xc0000000, 0x3fdd70a3, 0xd70a3d87},	/* 0.495449=f(0.46)*/
{36, 0,123,__LINE__, 0x3fe04141, 0xc0000000, 0x3fde147a, 0xe147ae2b},	/* 0.507966=f(0.47)*/
{36, 0,123,__LINE__, 0x3fe0a8d8, 0x00000000, 0x3fdeb851, 0xeb851ecf},	/* 0.520611=f(0.48)*/
{40, 0,123,__LINE__, 0x3fe11184, 0x00000000, 0x3fdf5c28, 0xf5c28f73},	/* 0.533388=f(0.49)*/
{36, 0,123,__LINE__, 0x3fe17b4f, 0x60000000, 0x3fe00000, 0x0000000b},	/* 0.546302=f(0.5)*/
{35, 0,123,__LINE__, 0x3fe1e644, 0x40000000, 0x3fe051eb, 0x851eb85d},	/* 0.559359=f(0.51)*/
{35, 0,123,__LINE__, 0x3fe2526d, 0x20000000, 0x3fe0a3d7, 0x0a3d70af},	/* 0.572562=f(0.52)*/
{39, 0,123,__LINE__, 0x3fe2bfd5, 0x00000000, 0x3fe0f5c2, 0x8f5c2901},	/* 0.585917=f(0.53)*/
{36, 0,123,__LINE__, 0x3fe32e87, 0x20000000, 0x3fe147ae, 0x147ae153},	/* 0.59943=f(0.54)*/
{38, 0,123,__LINE__, 0x3fe39e8e, 0xe0000000, 0x3fe19999, 0x999999a5},	/* 0.613105=f(0.55)*/
{37, 0,123,__LINE__, 0x3fe40ff8, 0x80000000, 0x3fe1eb85, 0x1eb851f7},	/* 0.62695=f(0.56)*/
{37, 0,123,__LINE__, 0x3fe482d0, 0x80000000, 0x3fe23d70, 0xa3d70a49},	/* 0.640969=f(0.57)*/
{36, 0,123,__LINE__, 0x3fe4f723, 0xc0000000, 0x3fe28f5c, 0x28f5c29b},	/* 0.655168=f(0.58)*/
{35, 0,123,__LINE__, 0x3fe56cff, 0xe0000000, 0x3fe2e147, 0xae147aed},	/* 0.669556=f(0.59)*/
{36, 0,123,__LINE__, 0x3fe5e473, 0x00000000, 0x3fe33333, 0x3333333f},	/* 0.684137=f(0.6)*/
{35, 0,123,__LINE__, 0x3fe65d8b, 0x20000000, 0x3fe3851e, 0xb851eb91},	/* 0.698919=f(0.61)*/
{35, 0,123,__LINE__, 0x3fe6d857, 0xc0000000, 0x3fe3d70a, 0x3d70a3e3},	/* 0.713909=f(0.62)*/
{35, 0,123,__LINE__, 0x3fe754e8, 0x60000000, 0x3fe428f5, 0xc28f5c35},	/* 0.729115=f(0.63)*/
{35, 0,123,__LINE__, 0x3fe7d34d, 0x80000000, 0x3fe47ae1, 0x47ae1487},	/* 0.744544=f(0.64)*/
{40, 0,123,__LINE__, 0x3fe85398, 0x20000000, 0x3fe4cccc, 0xccccccd9},	/* 0.760204=f(0.65)*/
{35, 0,123,__LINE__, 0x3fe8d5da, 0x20000000, 0x3fe51eb8, 0x51eb852b},	/* 0.776105=f(0.66)*/
{38, 0,123,__LINE__, 0x3fe95a25, 0x80000000, 0x3fe570a3, 0xd70a3d7d},	/* 0.792254=f(0.67)*/
{35, 0,123,__LINE__, 0x3fe9e08d, 0xe0000000, 0x3fe5c28f, 0x5c28f5cf},	/* 0.808661=f(0.68)*/
{36, 0,123,__LINE__, 0x3fea6927, 0x40000000, 0x3fe6147a, 0xe147ae21},	/* 0.825336=f(0.69)*/
{36, 0,123,__LINE__, 0x3feaf406, 0xc0000000, 0x3fe66666, 0x66666673},	/* 0.842288=f(0.7)*/
{36, 0,123,__LINE__, 0x3feb8142, 0x20000000, 0x3fe6b851, 0xeb851ec5},	/* 0.859529=f(0.71)*/
{35, 0,123,__LINE__, 0x3fec10f0, 0xc0000000, 0x3fe70a3d, 0x70a3d717},	/* 0.877068=f(0.72)*/
{37, 0,123,__LINE__, 0x3feca32a, 0x20000000, 0x3fe75c28, 0xf5c28f69},	/* 0.894918=f(0.73)*/
{38, 0,123,__LINE__, 0x3fed3807, 0xa0000000, 0x3fe7ae14, 0x7ae147bb},	/* 0.91309=f(0.74)*/
{36, 0,123,__LINE__, 0x3fedcfa3, 0x60000000, 0x3fe80000, 0x0000000d},	/* 0.931596=f(0.75)*/
{37, 0,123,__LINE__, 0x3fee6a19, 0x20000000, 0x3fe851eb, 0x851eb85f},	/* 0.950451=f(0.76)*/
{34, 0,123,__LINE__, 0x3fef0785, 0xc0000000, 0x3fe8a3d7, 0x0a3d70b1},	/* 0.969668=f(0.77)*/
{36, 0,123,__LINE__, 0x3fefa807, 0xc0000000, 0x3fe8f5c2, 0x8f5c2903},	/* 0.989262=f(0.78)*/
{35, 0,123,__LINE__, 0x3ff025df, 0x80000000, 0x3fe947ae, 0x147ae155},	/* 1.00925=f(0.79)*/
{35, 0,123,__LINE__, 0x3ff07966, 0x40000000, 0x3fe99999, 0x999999a7},	/* 1.02964=f(0.8)*/
{35, 0,123,__LINE__, 0x3ff0ceaa, 0x00000000, 0x3fe9eb85, 0x1eb851f9},	/* 1.05046=f(0.81)*/
{36, 0,123,__LINE__, 0x3ff125bd, 0x40000000, 0x3fea3d70, 0xa3d70a4b},	/* 1.07171=f(0.82)*/
{35, 0,123,__LINE__, 0x3ff17eb3, 0x80000000, 0x3fea8f5c, 0x28f5c29d},	/* 1.09343=f(0.83)*/
{36, 0,123,__LINE__, 0x3ff1d9a1, 0x40000000, 0x3feae147, 0xae147aef},	/* 1.11563=f(0.84)*/
{35, 0,123,__LINE__, 0x3ff2369c, 0x60000000, 0x3feb3333, 0x33333341},	/* 1.13833=f(0.85)*/
{35, 0,123,__LINE__, 0x3ff295bb, 0xa0000000, 0x3feb851e, 0xb851eb93},	/* 1.16156=f(0.86)*/
{35, 0,123,__LINE__, 0x3ff2f717, 0x40000000, 0x3febd70a, 0x3d70a3e5},	/* 1.18532=f(0.87)*/
{36, 0,123,__LINE__, 0x3ff35ac8, 0xc0000000, 0x3fec28f5, 0xc28f5c37},	/* 1.20966=f(0.88)*/
{38, 0,123,__LINE__, 0x3ff3c0eb, 0x60000000, 0x3fec7ae1, 0x47ae1489},	/* 1.2346=f(0.89)*/
{35, 0,123,__LINE__, 0x3ff4299b, 0xa0000000, 0x3feccccc, 0xccccccdb},	/* 1.26016=f(0.9)*/
{38, 0,123,__LINE__, 0x3ff494f8, 0x20000000, 0x3fed1eb8, 0x51eb852d},	/* 1.28637=f(0.91)*/
{38, 0,123,__LINE__, 0x3ff50320, 0xe0000000, 0x3fed70a3, 0xd70a3d7f},	/* 1.31326=f(0.92)*/
{36, 0,123,__LINE__, 0x3ff57438, 0x20000000, 0x3fedc28f, 0x5c28f5d1},	/* 1.34087=f(0.93)*/
{35, 0,123,__LINE__, 0x3ff5e862, 0x60000000, 0x3fee147a, 0xe147ae23},	/* 1.36923=f(0.94)*/
{35, 0,123,__LINE__, 0x3ff65fc6, 0x60000000, 0x3fee6666, 0x66666675},	/* 1.39838=f(0.95)*/
{35, 0,123,__LINE__, 0x3ff6da8d, 0x60000000, 0x3feeb851, 0xeb851ec7},	/* 1.42836=f(0.96)*/
{38, 0,123,__LINE__, 0x3ff758e3, 0x60000000, 0x3fef0a3d, 0x70a3d719},	/* 1.4592=f(0.97)*/
{37, 0,123,__LINE__, 0x3ff7daf7, 0x20000000, 0x3fef5c28, 0xf5c28f6b},	/* 1.49096=f(0.98)*/
{35, 0,123,__LINE__, 0x3ff860fa, 0xe0000000, 0x3fefae14, 0x7ae147bd},	/* 1.52368=f(0.99)*/
{36, 0,123,__LINE__, 0x3ff8eb24, 0x60000000, 0x3ff00000, 0x00000007},	/* 1.55741=f(1)*/
{36, 0,123,__LINE__, 0x3ff979ad, 0x00000000, 0x3ff028f5, 0xc28f5c30},	/* 1.59221=f(1.01)*/
{35, 0,123,__LINE__, 0x3ffa0cd2, 0x60000000, 0x3ff051eb, 0x851eb859},	/* 1.62813=f(1.02)*/
{35, 0,123,__LINE__, 0x3ffaa4d6, 0xc0000000, 0x3ff07ae1, 0x47ae1482},	/* 1.66524=f(1.03)*/
{36, 0,123,__LINE__, 0x3ffb4201, 0x40000000, 0x3ff0a3d7, 0x0a3d70ab},	/* 1.70361=f(1.04)*/
{34, 0,123,__LINE__, 0x3ffbe49e, 0x60000000, 0x3ff0cccc, 0xccccccd4},	/* 1.74332=f(1.05)*/
{35, 0,123,__LINE__, 0x3ffc8d00, 0xc0000000, 0x3ff0f5c2, 0x8f5c28fd},	/* 1.78442=f(1.06)*/
{34, 0,123,__LINE__, 0x3ffd3b82, 0x20000000, 0x3ff11eb8, 0x51eb8526},	/* 1.82703=f(1.07)*/
{34, 0,123,__LINE__, 0x3ffdf081, 0xc0000000, 0x3ff147ae, 0x147ae14f},	/* 1.87122=f(1.08)*/
{38, 0,123,__LINE__, 0x3ffeac68, 0xa0000000, 0x3ff170a3, 0xd70a3d78},	/* 1.91709=f(1.09)*/
{36, 0,123,__LINE__, 0x3fff6fa7, 0xe0000000, 0x3ff19999, 0x999999a1},	/* 1.96476=f(1.1)*/
{40, 0,123,__LINE__, 0x40001d5d, 0x60000000, 0x3ff1c28f, 0x5c28f5ca},	/* 2.01434=f(1.11)*/
{36, 0,123,__LINE__, 0x40008713, 0x80000000, 0x3ff1eb85, 0x1eb851f3},	/* 2.06596=f(1.12)*/
{36, 0,123,__LINE__, 0x4000f53f, 0x80000000, 0x3ff2147a, 0xe147ae1c},	/* 2.11975=f(1.13)*/
{38, 0,123,__LINE__, 0x40016831, 0x20000000, 0x3ff23d70, 0xa3d70a45},	/* 2.17587=f(1.14)*/
{36, 0,123,__LINE__, 0x4001e03f, 0xe0000000, 0x3ff26666, 0x6666666e},	/* 2.2345=f(1.15)*/
{36, 0,123,__LINE__, 0x40025dcb, 0x80000000, 0x3ff28f5c, 0x28f5c297},	/* 2.2958=f(1.16)*/
{42, 0,123,__LINE__, 0x4002e13d, 0xa0000000, 0x3ff2b851, 0xeb851ec0},	/* 2.35998=f(1.17)*/
{36, 0,123,__LINE__, 0x40036b0a, 0x60000000, 0x3ff2e147, 0xae147ae9},	/* 2.42727=f(1.18)*/
{37, 0,123,__LINE__, 0x4003fbb2, 0xe0000000, 0x3ff30a3d, 0x70a3d712},	/* 2.4979=f(1.19)*/
{64, 0,123,__LINE__, 0xbe8777a5, 0xc0000000, 0xc01921fb, 0x54442d18},	/* -1.74846e-07=f(-6.28319)*/
{37, 0,123,__LINE__, 0x4193fe4d, 0xa0000000, 0xc012d97c, 0x7f3321d2},	/* 8.38583e+07=f(-4.71239)*/
{64, 0,123,__LINE__, 0xbe7777a5, 0xc0000000, 0xc00921fb, 0x54442d18},	/* -8.74228e-08=f(-3.14159)*/
{36, 0,123,__LINE__, 0x4175d149, 0x60000000, 0xbff921fb, 0x54442d18},	/* 2.28773e+07=f(-1.5708)*/
{64, 0,123,__LINE__, 0x00000000, 0x00000000, 0x00000000, 0x00000000},	/* 0=f(0)*/
{36, 0,123,__LINE__, 0xc175d149, 0x60000000, 0x3ff921fb, 0x54442d18},	/* -2.28773e+07=f(1.5708)*/
{64, 0,123,__LINE__, 0x3e7777a5, 0xc0000000, 0x400921fb, 0x54442d18},	/* 8.74228e-08=f(3.14159)*/
{37, 0,123,__LINE__, 0xc193fe4d, 0xa0000000, 0x4012d97c, 0x7f3321d2},	/* -8.38583e+07=f(4.71239)*/
{37, 0,123,__LINE__, 0x40199f0f, 0x20000000, 0xc03e0000, 0x00000000},	/* 6.40533=f(-30)*/
{35, 0,123,__LINE__, 0xbf9a497f, 0x20000000, 0xc03c4ccc, 0xcccccccd},	/* -0.025671=f(-28.3)*/
{37, 0,123,__LINE__, 0xc0233f66, 0xa0000000, 0xc03a9999, 0x9999999a},	/* -9.62383=f(-26.6)*/
{36, 0,123,__LINE__, 0x3fce573b, 0xa0000000, 0xc038e666, 0x66666667},	/* 0.237037=f(-24.9)*/
{37, 0,123,__LINE__, 0xc005210f, 0x20000000, 0xc0373333, 0x33333334},	/* -2.64114=f(-23.2)*/
{35, 0,123,__LINE__, 0x3fe11d9c, 0x00000000, 0xc0358000, 0x00000001},	/* 0.534864=f(-21.5)*/
{41, 0,123,__LINE__, 0xbff66525, 0x20000000, 0xc033cccc, 0xccccccce},	/* -1.39969=f(-19.8)*/
{36, 0,123,__LINE__, 0x3fedc8d7, 0x00000000, 0xc0321999, 0x9999999b},	/* 0.930767=f(-18.1)*/
{41, 0,123,__LINE__, 0xbfea853e, 0xe0000000, 0xc0306666, 0x66666668},	/* -0.828765=f(-16.4)*/
{36, 0,123,__LINE__, 0x3ff95c48, 0x40000000, 0xc02d6666, 0x6666666a},	/* 1.58503=f(-14.7)*/
{36, 0,123,__LINE__, 0xbfdda223, 0x60000000, 0xc02a0000, 0x00000004},	/* -0.463021=f(-13)*/
{36, 0,123,__LINE__, 0x4009764c, 0xe0000000, 0xc0269999, 0x9999999e},	/* 3.18276=f(-11.3)*/
{36, 0,123,__LINE__, 0xbfc6a92e, 0x60000000, 0xc0233333, 0x33333338},	/* -0.177038=f(-9.6)*/
{40, 0,123,__LINE__, 0x4035b70e, 0xa0000000, 0xc01f9999, 0x999999a3},	/* 21.7151=f(-7.9)*/
{35, 0,123,__LINE__, 0x3fb55841, 0x20000000, 0xc018cccc, 0xccccccd6},	/* 0.0833779=f(-6.2)*/
{40, 0,123,__LINE__, 0xc0128ca0, 0xc0000000, 0xc0120000, 0x00000009},	/* -4.63733=f(-4.5)*/
{37, 0,123,__LINE__, 0x3fd6c100, 0x60000000, 0xc0066666, 0x66666678},	/* 0.35553=f(-2.8)*/
{36, 0,123,__LINE__, 0xbfff6fa7, 0xe0000000, 0xbff19999, 0x999999bd},	/* -1.96476=f(-1.1)*/
{36, 0,123,__LINE__, 0x3fe5e473, 0x00000000, 0x3fe33333, 0x333332ec},	/* 0.684137=f(0.6)*/
{35, 0,123,__LINE__, 0xbff1e84c, 0xa0000000, 0x40026666, 0x66666654},	/* -1.11921=f(2.3)*/
{36, 0,123,__LINE__, 0x3ff2866f, 0xa0000000, 0x400fffff, 0xffffffee},	/* 1.15782=f(4)*/
{36, 0,123,__LINE__, 0xbfe51c83, 0xe0000000, 0x4016cccc, 0xccccccc4},	/* -0.659731=f(5.7)*/
{36, 0,123,__LINE__, 0x400064ef, 0x60000000, 0x401d9999, 0x99999991},	/* 2.04928=f(7.4)*/
{36, 0,123,__LINE__, 0xbfd58c7e, 0xa0000000, 0x40223333, 0x3333332f},	/* -0.3367=f(9.1)*/
{38, 0,123,__LINE__, 0x401430f0, 0xc0000000, 0x40259999, 0x99999995},	/* 5.04779=f(10.8)*/
{35, 0,123,__LINE__, 0xbfb10410, 0x00000000, 0x4028ffff, 0xfffffffb},	/* -0.0664682=f(12.5)*/
{34, 0,123,__LINE__, 0xc02fc9e0, 0x00000000, 0x402c6666, 0x66666661},	/* -15.8943=f(14.2)*/
{36, 0,123,__LINE__, 0x3fc8e328, 0xa0000000, 0x402fcccc, 0xccccccc7},	/* 0.194432=f(15.9)*/
{36, 0,123,__LINE__, 0xc0080a74, 0xc0000000, 0x40319999, 0x99999997},	/* -3.00511=f(17.6)*/
{36, 0,123,__LINE__, 0x3fdef355, 0xa0000000, 0x40334ccc, 0xccccccca},	/* 0.483602=f(19.3)*/
{35, 0,123,__LINE__, 0xbff870a2, 0x40000000, 0x4034ffff, 0xfffffffd},	/* -1.5275=f(21)*/
{36, 0,123,__LINE__, 0x3feb70ec, 0xe0000000, 0x4036b333, 0x33333330},	/* 0.857535=f(22.7)*/
{35, 0,123,__LINE__, 0xbfeccbb5, 0xe0000000, 0x40386666, 0x66666663},	/* -0.899867=f(24.4)*/
{34, 0,123,__LINE__, 0x3ff735e5, 0xa0000000, 0x403a1999, 0x99999996},	/* 1.45066=f(26.1)*/
{37, 0,123,__LINE__, 0xbfe06e07, 0x00000000, 0x403bcccc, 0xccccccc9},	/* -0.513431=f(27.8)*/
{37, 0,123,__LINE__, 0x4006407d, 0xa0000000, 0x403d7fff, 0xfffffffc},	/* 2.78149=f(29.5)*/
{0},};
void test_tanf(int m)   {run_vector_1(m,tanf_vec,(char *)(tanf),"tanf","ff");   }	
