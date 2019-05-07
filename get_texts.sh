#!/bin/sh
mkdir texts
curl -L https://github.com/alpheios-project/canonical-latinLit/archive/master.zip > ./texts/canonical-latinLit.zip
curl -L https://github.com/PerseusDL/canonical-greekLit/archive/master.zip > ./texts/canonical-greekLit.zip
curl -L https://github.com/alpheios-project/cts-texts-latinLit/archive/master.zip > ./texts/alpheios-latinLit.zip
curl -L https://github.com/alpheios-project/cts-texts-greekLit/archive/master.zip > ./texts/alpheios-greekLit.zip
curl -L https://github.com/alpheios-project/cts-texts-arabicLit/archive/master.zip > ./texts/alpheios-arabicLit.zip
unzip -q "texts/*.zip" -d texts 

