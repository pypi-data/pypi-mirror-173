/*
 * Copyright (c) 1990, 2007 The Regents of the University of California.
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms are permitted
 * provided that the above copyright notice and this paragraph are
 * duplicated in all such forms and that any documentation,
 * and/or other materials related to such
 * distribution and use acknowledge that the software was developed
 * by the University of California, Berkeley.  The name of the
 * University may not be used to endorse or promote products derived
 * from this software without specific prior written permission.
 * THIS SOFTWARE IS PROVIDED ``AS IS'' AND WITHOUT ANY EXPRESS OR
 * IMPLIED WARRANTIES, INCLUDING, WITHOUT LIMITATION, THE IMPLIED
 * WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.
 */
/* doc in sprintf.c */
/* This code created by modifying sprintf.c so copyright inherited. */

#define _DEFAULT_SOURCE
#include <_ansi.h>
#include <stdio.h>
#include <stdarg.h>
#include <limits.h>
#include <errno.h>
#include "local.h"

#undef snprintf

int
snprintf (char *__restrict str,
       size_t size,
       const char *__restrict fmt, ...)
{
  int ret;
  va_list ap;
  FILE f;

  if (size > INT_MAX)
    {
      _REENT_ERRNO(ptr) = EOVERFLOW;
      return EOF;
    }
  f._flags = __SWR | __SSTR;
  f._bf._base = f._p = (unsigned char *) str;
  f._bf._size = f._w = (size > 0 ? size - 1 : 0);
  f._file = -1;  /* No file. */
  va_start (ap, fmt);
  ret = svfprintf ( &f, fmt, ap);
  va_end (ap);
  if (ret < EOF)
    _REENT_ERRNO(ptr) = EOVERFLOW;
  if (size > 0)
    *f._p = 0;
  return (ret);
}

#ifdef _NANO_FORMATTED_IO
int __nonnull((1, 3)) _NOTHROW
sniprintf (char *, size_t, const char *, ...)
       _ATTRIBUTE ((__alias__("snprintf")));
#endif
