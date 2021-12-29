#pragma once

#define static_fail(msg) []<bool flag = false>(){static_assert(flag, msg);}()

#include <fstream>
#include <string>
#include <regex>
#include <utility>

#include "run.h"
#include "ostream.h"
#include "parsing.h"
#include "circular_buffer.h"
#include "containers.h"

#if defined(DEBUG)
#   define dbg(X) do{X;}while(false)
#   define is_dbg() (1)
#else
#   define dbg(X)  do{}while(false)
#   define is_dbg() (0)
#endif


typedef long long ll;
typedef unsigned long long ull;
typedef __int128_t lll;
typedef __uint128_t ulll;
