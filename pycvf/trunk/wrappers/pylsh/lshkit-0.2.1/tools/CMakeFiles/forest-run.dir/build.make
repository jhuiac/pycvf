# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 2.6

#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canoncical targets will work.
.SUFFIXES:

# Remove some rules from gmake that .SUFFIXES does not remove.
SUFFIXES =

.SUFFIXES: .hpux_make_needs_suffix_list

# Produce verbose output by default.
VERBOSE = 1

# Suppress display of executed commands.
$(VERBOSE).SILENT:

# A target that is always out of date.
cmake_force:
.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /usr/bin/cmake

# The command to remove a file.
RM = /usr/bin/cmake -E remove -f

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /home/tranx/pycvfext/wrappers/pylsh/lshkit-0.2.1

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/tranx/pycvfext/wrappers/pylsh/lshkit-0.2.1

# Include any dependencies generated for this target.
include tools/CMakeFiles/forest-run.dir/depend.make

# Include the progress variables for this target.
include tools/CMakeFiles/forest-run.dir/progress.make

# Include the compile flags for this target's objects.
include tools/CMakeFiles/forest-run.dir/flags.make

tools/CMakeFiles/forest-run.dir/forest-run.cpp.o: tools/CMakeFiles/forest-run.dir/flags.make
tools/CMakeFiles/forest-run.dir/forest-run.cpp.o: tools/forest-run.cpp
	$(CMAKE_COMMAND) -E cmake_progress_report /home/tranx/pycvfext/wrappers/pylsh/lshkit-0.2.1/CMakeFiles $(CMAKE_PROGRESS_1)
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Building CXX object tools/CMakeFiles/forest-run.dir/forest-run.cpp.o"
	cd /home/tranx/pycvfext/wrappers/pylsh/lshkit-0.2.1/tools && /usr/bin/c++   $(CXX_DEFINES) $(CXX_FLAGS) -o CMakeFiles/forest-run.dir/forest-run.cpp.o -c /home/tranx/pycvfext/wrappers/pylsh/lshkit-0.2.1/tools/forest-run.cpp

tools/CMakeFiles/forest-run.dir/forest-run.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/forest-run.dir/forest-run.cpp.i"
	cd /home/tranx/pycvfext/wrappers/pylsh/lshkit-0.2.1/tools && /usr/bin/c++  $(CXX_DEFINES) $(CXX_FLAGS) -E /home/tranx/pycvfext/wrappers/pylsh/lshkit-0.2.1/tools/forest-run.cpp > CMakeFiles/forest-run.dir/forest-run.cpp.i

tools/CMakeFiles/forest-run.dir/forest-run.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/forest-run.dir/forest-run.cpp.s"
	cd /home/tranx/pycvfext/wrappers/pylsh/lshkit-0.2.1/tools && /usr/bin/c++  $(CXX_DEFINES) $(CXX_FLAGS) -S /home/tranx/pycvfext/wrappers/pylsh/lshkit-0.2.1/tools/forest-run.cpp -o CMakeFiles/forest-run.dir/forest-run.cpp.s

tools/CMakeFiles/forest-run.dir/forest-run.cpp.o.requires:
.PHONY : tools/CMakeFiles/forest-run.dir/forest-run.cpp.o.requires

tools/CMakeFiles/forest-run.dir/forest-run.cpp.o.provides: tools/CMakeFiles/forest-run.dir/forest-run.cpp.o.requires
	$(MAKE) -f tools/CMakeFiles/forest-run.dir/build.make tools/CMakeFiles/forest-run.dir/forest-run.cpp.o.provides.build
.PHONY : tools/CMakeFiles/forest-run.dir/forest-run.cpp.o.provides

tools/CMakeFiles/forest-run.dir/forest-run.cpp.o.provides.build: tools/CMakeFiles/forest-run.dir/forest-run.cpp.o
.PHONY : tools/CMakeFiles/forest-run.dir/forest-run.cpp.o.provides.build

# Object files for target forest-run
forest__run_OBJECTS = \
"CMakeFiles/forest-run.dir/forest-run.cpp.o"

# External object files for target forest-run
forest__run_EXTERNAL_OBJECTS =

bin/forest-run: tools/CMakeFiles/forest-run.dir/forest-run.cpp.o
bin/forest-run: lib/liblshkit.a
bin/forest-run: /usr/lib/libboost_program_options-mt.a
bin/forest-run: tools/CMakeFiles/forest-run.dir/build.make
bin/forest-run: tools/CMakeFiles/forest-run.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --red --bold "Linking CXX executable ../bin/forest-run"
	cd /home/tranx/pycvfext/wrappers/pylsh/lshkit-0.2.1/tools && $(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/forest-run.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
tools/CMakeFiles/forest-run.dir/build: bin/forest-run
.PHONY : tools/CMakeFiles/forest-run.dir/build

tools/CMakeFiles/forest-run.dir/requires: tools/CMakeFiles/forest-run.dir/forest-run.cpp.o.requires
.PHONY : tools/CMakeFiles/forest-run.dir/requires

tools/CMakeFiles/forest-run.dir/clean:
	cd /home/tranx/pycvfext/wrappers/pylsh/lshkit-0.2.1/tools && $(CMAKE_COMMAND) -P CMakeFiles/forest-run.dir/cmake_clean.cmake
.PHONY : tools/CMakeFiles/forest-run.dir/clean

tools/CMakeFiles/forest-run.dir/depend:
	cd /home/tranx/pycvfext/wrappers/pylsh/lshkit-0.2.1 && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/tranx/pycvfext/wrappers/pylsh/lshkit-0.2.1 /home/tranx/pycvfext/wrappers/pylsh/lshkit-0.2.1/tools /home/tranx/pycvfext/wrappers/pylsh/lshkit-0.2.1 /home/tranx/pycvfext/wrappers/pylsh/lshkit-0.2.1/tools /home/tranx/pycvfext/wrappers/pylsh/lshkit-0.2.1/tools/CMakeFiles/forest-run.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : tools/CMakeFiles/forest-run.dir/depend

