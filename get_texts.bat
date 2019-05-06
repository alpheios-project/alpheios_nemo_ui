:: A version of get_texts.sh for Windows 10 build is 17063 or later (where it has cURL installed)
:: Use wsl version of cURL for earlier Windows 10 builds
mkdir texts
curl -L https://github.com/PerseusDL/canonical-latinLit/archive/master.zip > ./texts/canonical-latinLit.zip
curl -L https://github.com/PerseusDL/canonical-greekLit/archive/master.zip > ./texts/canonical-greekLit.zip
curl -L https://github.com/alpheios-project/cts-texts-latinLit/archive/master.zip > ./texts/alpheios-latinLit.zip
curl -L https://github.com/alpheios-project/cts-texts-greekLit/archive/master.zip > ./texts/alpheios-greekLit.zip
curl -L https://github.com/alpheios-project/cts-texts-arabicLit/archive/master.zip > ./texts/alpheios-arabicLit.zip
:: Extract downloaded text using WSL version of unzip
wsl unzip -q "texts/*.zip" -d texts

:: As an alternative, files can be extracted using 7-Zip (https://www.7-zip.org/)
:: 7-Zip executable must be added to your PATH
::cd texts
::7z x *.zip
::cd ..
