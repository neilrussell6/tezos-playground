#! /bin/sh

set -e

command_docs="* help
  Display this help message."

LIGHTBLUE=74
LIME=106
RED=124
LIGHTRED=202

BOLD=1
DIM=2
ITALIC=3
UNDERLINED=4
NORMAL=5

RESET="\033[0m"

function _getBG() {
  echo "\033[48;5;${1}m"
}

function _getFG() {
    local mod="${!2:-$NORMAL}"
    echo "\033[${mod};38;5;${1}m"
}

function _print() {
	printf '%b%b%s %b' $1 $2 "${3}" $RESET
}

function print_success() {
	local color="${LIME}"
	local mod="${NORMAL}"
	_print $RESET $(_getFG $color $mod) "${1}"
}

function print_error() {
	local color="${LIGHTRED}"
	local mod="${NORMAL}"
	_print $RESET $(_getFG $color $mod) "${1}"
}

say () {
    {
        printf "[SmartPyBasic] "
        printf "$@"
        printf "\n"
    } >&2
}

download () {
    local uri="$1"
    local out="$2"
    say "Downloading $out ..."
    if [ -f "$out" ] ; then
        rm "$out"
    fi
    curl -s "$uri" -o "./$out"
    if [ -f "$out" ] ; then
        :
    else
        say "Download of '$uri' failed"
        exit 4
    fi
}

run_local_name="run"
install_path=$(dirname "$0")
command_docs="$command_docs


* $run_local_name <contract.py>
  Call a SmartPy script using the local installation.
  Example:
    $0 $run_local_name $install_path/scripts/demo.py"

run_local () {
    python3 $install_path/smartpybasic.py $1
}


test_local_name="test"
command_docs="$command_docs

* $test_local_name <contractBuilder.py> <output-directory>
  Test a contract."
test_local () {
    local contracts=${@:1:$#-1}
    local target_dir_base="${@: -1}"
    if [ "$target_dir_base" = "" ] ; then
        say "$test_local_name: Wrong command line"
        usage
        exit 8
    fi
    mkdir -p "$target_dir_base/"
    for contract in $contracts
    do
        IFS='/' read -ra contract_parts <<< "${contract}"
        local target_dir="${target_dir_base}/${contract_parts[${#contract_parts[@]}-2]}/${contract_parts[${#contract_parts[@]}-1]}"
        local basecontract="$(basename $contract)"
        local scenariofile="$target_dir/$basecontract.sc"
        local pyadaptedfile="$target_dir/${basecontract}_gen.py"
        ensure_locally_installed "$install_path"
        mkdir -p "$target_dir/"
        rm -f $scenariofile $pyadaptedfile $target_dir/test.output $target_dir/testContractCode*
        PYTHONPATH=$PWD python3 "$install_path/smartpybasic.py" \
                  "$contract" \
                  --test \
                  --scenario "$scenariofile" \
                  --pyadaptedfile "$pyadaptedfile"
        node "$install_path/smartmlbasic.js" \
             --scenario "$scenariofile" \
             --outputDir "$target_dir" > $target_dir/test.output

        local result=$(cat $target_dir/test.output | tail -1 | tr -d ' ')
        if [[ "${result}" == "OK" ]]
            then
                print_success " - ${contract} - PASS"; echo ""
            else
                print_error " - ${contract} - FAIL"; echo ""
                print_error "$(cat $target_dir/test.output | tail -4)"; echo ""
        fi
    done
}

compile_local_name="compile"
command_docs="$command_docs

* $compile_local_name <contractBuilder.py> <class-call> <output-directory>
  Compile a contract to michelson."
compile_local () {
    local contract="$1"
    local class_call="$2"
    local target_dir="$3"
    if [ "$target_dir" = "" ] ; then
        say "$compile_local_name: Wrong command line"
        usage
        exit 8
    fi
    local basecontract="$(basename $contract)"
    local sexprfile="$target_dir/$basecontract.smlse"
    local pyadaptedfile="$target_dir/${basecontract}_gen.py"
    ensure_locally_installed "$install_path"
    mkdir -p "$target_dir/"
    rm -f $sexprfile $pyadaptedfile $target_dir/*.tz
    PYTHONPATH="$install_path/" python3 "$install_path/smartpybasic.py" \
              "$contract" \
              --class_call "$class_call" \
              --sexprfile "$sexprfile" \
              --pyadaptedfile "$pyadaptedfile"
    node "$install_path/smartmlbasic.js" \
         --compile "$sexprfile" \
         --outputDir "$target_dir"
    say "$compile_local_name: Done see $target_dir/"
}

minimal_install_name="local-install"
command_docs="$command_docs

* $minimal_install_name <path>
  Install a local (minimal) distribution of SmartPy for command line usage."
minimal_install () {
    if [ "$1" = "" ] ; then
        say "$minimal_install_name: Missing install path argument."
        say "Use '$minimal_install_name ~' to install ~/SmartPyBasic."
        exit 2
    fi
    local path="$1/SmartPyBasic"
    mkdir -p "$path" || {
        say "$minimal_install_name: Wrong path, argument"
        exit 5
    }
    say "Installing minimal distribution in '$path'"
    (
        cd "$path"
        mkdir -p scripts
        download https://SmartPy.io/SmartPyBasic/smartpy.py      smartpy.py
        download https://SmartPy.io/SmartPyBasic/smartpyio.py    smartpyio.py
        download https://SmartPy.io/SmartPyBasic/smartpybasic.py smartpybasic.py
        download https://SmartPy.io/SmartPyBasic/browser.py      browser.py
        download https://SmartPy.io/SmartPyBasic/smartmljs.bc.js smartmljs.bc.js
        download https://SmartPy.io/SmartPyBasic/SmartPy.sh      SmartPy.sh
        download https://SmartPy.io/SmartPyBasic/smartmlbasic.js smartmlbasic.js
        download https://SmartPy.io/SmartPyBasic/demo.py         scripts/demo.py
        chmod +x SmartPy.sh
        say "Installation successful! in "`pwd`
        ls -ltr `pwd`/SmartPy.sh
    ) || {
        say "$minimal_install_name: Installation failed."
        exit 4
    }
}

minimal_install_name_dev="local-install-dev"
command_docs="$command_docs

* $minimal_install_name_dev <path>
  Install a local (minimal) distribution of SmartPy for command line usage."
minimal_install_dev () {
    if [ "$1" = "" ] ; then
        say "$minimal_install_name_dev: Missing install path argument."
        say "Use '$minimal_install_name_dev ~' to install ~/SmartPyBasicDev."
        exit 2
    fi
    local path="$1/SmartPyBasic"
    mkdir -p "$path" || {
        say "$minimal_install_name_dev: Wrong path, argument"
        exit 5
    }
    say "Installing minimal distribution in '$path'"
    (
        cd "$path"
        mkdir -p scripts
        download https://SmartPy.io/SmartPyBasicDev/smartpy.py      smartpy.py
        download https://SmartPy.io/SmartPyBasicDev/smartpyio.py    smartpyio.py
        download https://SmartPy.io/SmartPyBasicDev/smartpybasic.py smartpybasic.py
        download https://SmartPy.io/SmartPyBasicDev/browser.py      browser.py
        download https://SmartPy.io/SmartPyBasicDev/smartmljs.bc.js smartmljs.bc.js
        download https://SmartPy.io/SmartPyBasicDev/SmartPy.sh      SmartPy.sh
        download https://SmartPy.io/SmartPyBasicDev/smartmlbasic.js smartmlbasic.js
        download https://SmartPy.io/SmartPyBasicDev/demo.py         scripts/demo.py
        chmod +x SmartPy.sh
        say "Installation successful! in "`pwd`
        ls -ltr `pwd`/SmartPy.sh
    ) || {
        say "$minimal_install_name_dev: Installation failed."
        exit 4
    }
}

minimal_install_name_test="local-install-test"
command_docs="$command_docs

* $minimal_install_name_test <path>
  Install a local (minimal) distribution of SmartPy for command line usage."
minimal_install_test () {
    if [ "$1" = "" ] ; then
        say "$minimal_install_name_test: Missing install path argument."
        say "Use '$minimal_install_name_test ~' to install ~/SmartPyBasicTest."
        exit 2
    fi
    local path="$1/SmartPyBasic"
    mkdir -p "$path" || {
        say "$minimal_install_name_test: Wrong path, argument"
        exit 5
    }
    say "Installing minimal distribution in '$path'"
    (
        cd "$path"
        mkdir -p scripts
        download https://SmartPy.io/SmartPyBasicTest/smartpy.py              smartpy.py
        download https://SmartPy.io/SmartPyBasicTest/smartpyio.py            smartpyio.py
        download https://SmartPy.io/SmartPyBasicTest/smartpybasic.py         smartpybasic.py
        download https://SmartPy.io/SmartPyBasicTest/browser.py              browser.py
        download https://SmartPy.io/SmartPyBasicTest/smartmljs.bc.js         smartmljs.bc.js
        download https://SmartPy.io/SmartPyBasicTest/SmartPy.sh              SmartPy.sh
        download https://SmartPy.io/SmartPyBasicTest/smartmlbasic.js         smartmlbasic.js
        download https://SmartPy.io/SmartPyBasicTest/demo.py                 scripts/demo.py
        download https://SmartPy.io/SmartPyBasicTest/reference.html          reference.html
        download https://SmartPy.io/SmartPyBasicTest/asciidoctor.css         asciidoctor.css
        download https://SmartPy.io/SmartPyBasicTest/coderay-asciidoctor.css coderay-asciidoctor.css
        chmod +x SmartPy.sh
        say "Installation successful! in "`pwd`
        ls -ltr `pwd`/SmartPy.sh
    ) || {
        say "$minimal_install_name_test: Installation failed."
        exit 4
    }
}

ensure_locally_installed () {
    local path="$1"
    if [ -f "$path/smartmlbasic.js" ] ; then
        :
    else
        say "There does not seem to be a local installation at '$path', please use the '$minimal_install_name' command"
        # At some point we could also ask the user if they want to
        # install here and then call minimal.
        exit 2
    fi
}


usage () {
    cat >&2 <<EOF

[SmartPyBasic]

Introduction: https://medium.com/@SmartPy_io/f5bd8772b74a

Install directory: $install_path

Usage: $0 <command> <arguments>

Where <command> can be:
$command_docs

EOF
}

case "$1" in
    "" | "help" | "--help" | "-h" )
        usage ;;
    "$minimal_install_name" )
        minimal_install "$2" ;;
    "$minimal_install_name_dev" )
        minimal_install_dev "$2" ;;
    "$minimal_install_name_test" )
        minimal_install_test "$2" ;;
    "$compile_local_name" )
        shift
        compile_local "$@" ;;
    "local-compile" )
        shift
        compile_local "$@" ;;
    "$test_local_name" )
        shift
        test_local "$@" ;;
    "local-test" )
        shift
        test_local "$@" ;;
    "$run_local_name" )
        shift
        run_local "$@" ;;
    * )
        say "Unknown command '$1'"
        usage
        exit 1 ;;
esac
