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
#else
#   define dbg(X)  do{}while(false)
#endif


