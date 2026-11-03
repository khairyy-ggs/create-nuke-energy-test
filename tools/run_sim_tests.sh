#!/bin/sh
# Compiles and runs the pure-Java sim checks (no Gradle, no Minecraft). Works with a JRE that ships jdk.compiler.
rm -rf /tmp/sf-out && java -m jdk.compiler/com.sun.tools.javac.Main -d /tmp/sf-out src/main/java/dev/staggfield/sim/*.java src/test/java/dev/staggfield/sim/*.java && java -cp /tmp/sf-out dev.staggfield.sim.SimCheck
