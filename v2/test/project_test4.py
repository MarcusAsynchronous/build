#!/usr/bin/python

from BoostBuild import Tester
import os
from string import strip, find

t = Tester(translate_suffixes=0)


t.set_tree("project-test4")

t.run_build_system()

t.expect_addition("bin/$toolset/debug/a.obj")
t.expect_content("bin/$toolset/debug/a.obj",
"""$toolset/debug/include-everything
a.cpp
""")

t.expect_addition("bin/$toolset/debug/a.exe")
t.expect_content("bin/$toolset/debug/a.exe",
"$toolset/debug/include-everything\n" +
"bin/$toolset/debug/a.obj lib/bin/$toolset/debug/optimization-speed/b.obj\n"
)

t.expect_addition("lib/bin/$toolset/debug/optimization-speed/b.obj")
t.expect_content("lib/bin/$toolset/debug/optimization-speed/b.obj",
"""$toolset/debug/define-NDEBUG/include-everything/optimization-speed
lib/b.cpp
""")

t.expect_addition("bin/$toolset/debug/main-target-b.exe/b.exe")
t.expect_content("bin/$toolset/debug/main-target-b.exe/b.exe",
"$toolset/debug/define-MACROS/include-everything\n" +
"bin/$toolset/debug/a.obj\n"
)


t.copy("lib/Jamfile3", "lib/Jamfile")

t.run_build_system(status=None)
t.fail_test(find(t.stdout(),
"""warning: targets produced from b.obj are link incompatible
warning: with main target a.exe""") !=-0)

# We don't yet make targets depend on Jamfile, so need to start from scratch
# The following test is disabled, because of problems related to
# issue BB10

#t.set_tree("project-test4")
#t.copy("Jamfile2", "Jamfile")

#t.run_build_system()

#t.expect_addition("bin/$toolset/debug/a_gcc.obj")
#t.expect_content("bin/$toolset/debug/a_gcc.obj",
#"""$toolset/debug
#a_gcc.cpp
#""")

#t.expect_content("bin/$toolset/debug/a.exe",
#"$toolset/debug\n" +
#"bin/$toolset/debug/a.obj " +
#"lib/bin/$toolset/debug/optimization-speed/b.obj " +
#"bin/$toolset/debug/a_gcc.obj\n"
#)

# Test that if we specified composite property in target reference,
# everything works OK.

t.copy("lib/Jamfile1", "lib/Jamfile")
t.copy("Jamfile5", "Jamfile")

t.run_build_system()

t.expect_addition("lib/bin/$toolset/release/b.obj")

t.expect_content("bin/$toolset/debug/a.exe",
"$toolset/debug/include-everything\n" +
"bin/$toolset/debug/a.obj lib/bin/$toolset/release/b.obj\n"
)


t.cleanup()
