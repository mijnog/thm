#!/bin/bash
/opt/metasploit-framework/embedded/framework/tools/exploit/pattern_create.rb -l $1 > pattern.dat
cat pattern.dat
