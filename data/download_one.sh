#!/bin/sh

BASEDIR=`pwd`

if [ ! -d "$BASEDIR" ]; then
    mkdir "$BASEDIR"
fi

# fb15k
if [ ! -d "$BASEDIR/fb15k" ]; then
    echo Downloading fb15k
    cd $BASEDIR
    curl -O http://web.informatik.uni-mannheim.de/pi1/kge-datasets/fb15k.tar.gz
    tar xvf fb15k.tar.gz
    cd fb15k
    case "$(uname -s)" in
        CYGWIN*|MINGW32*|MSYS*)
            cmd.exe /c mklink train.txt freebase_mtr100_mte100-train.txt
            cmd.exe /c mklink valid.txt freebase_mtr100_mte100-valid.txt
            cmd.exe /c mklink test.txt freebase_mtr100_mte100-test.txt
            ;;
        *)
            ln -s freebase_mtr100_mte100-train.txt train.txt
            ln -s freebase_mtr100_mte100-valid.txt valid.txt
            ln -s freebase_mtr100_mte100-test.txt test.txt
            ;;
    esac
    cd ..
else
    echo fb15k already present
fi
if [ ! -f "$BASEDIR/fb15k/dataset.yaml" ]; then
    python preprocess/preprocess_default.py fb15k
else
    echo fb15k already prepared
fi
