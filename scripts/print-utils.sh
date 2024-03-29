#!/bin/bash

LIGHTER_GREY=246
LIGHT_GREY=244
GREY=243
DARK_GREY=237
DARKER_GREY=235
BLACK=233

BLUE=4
GOLD=214
LIGHTBLUE=74
LIME=106
RED=124
LIGHTRED=202
PINK=219
WHITE=255
PURPLE=99

DETAULT_THEME=$LIME

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
	printf '%b%b %s %b' $1 $2 "${3}" $RESET
}

function h1() {
	local color="${!2:-$DETAULT_THEME}"
	_print $(_getBG $color) $(_getFG $BLACK BOLD) "${1}"
}

function h2() {
	local color="${!2:-$DETAULT_THEME}"
	_print $(_getBG $BLACK) $(_getFG $color) "${1}"
}

function h3() {
	_print $(_getBG $BLACK) $(_getFG $LIGHTER_GREY BOLD) "${1}"
}

function warn() {
	local color="${GOLD}"
	_print $(_getBG $BLACK) $(_getFG $color BOLD) "${1}"
}

function error() {
	local color="${LIGHTRED}"
	_print $(_getBG $BLACK) $(_getFG $color BOLD) "${1}"
}

function print() {
	local color="${!2:-$DETAULT_THEME}"
	local mod="${3:-NORMAL}"
	_print $RESET $(_getFG $color $mod) "${1}"
}

function printList() {
	local color="${3:-$DETAULT_THEME}"
	local mod="${4:-NORMAL}"
    IFS="${2:-;}" read -ra xs <<< "${1//\n/}"
    for i in "${!xs[@]}"; do
        echo $(print " - ${xs[$i]//\"/}" $color $mod);
    done
}

function printDefListItem() {
	local color1="${!3:-$DETAULT_THEME}"
	local color2="${!4:-$DETAULT_THEME}"
    local pad="${5:-20}"
    printf "%b%b %-${pad}s %b%b %s %b\n" $(_getBG) $(_getFG $color1) \
    "${1}" $RESET $(_getFG $color2) "${2}" $RESET
}

function printDefList() {
	local color1="${3:-DETAULT_THEME}"
	local color2="${4:-DETAULT_THEME}"
    IFS="${2:-;}" read -ra xs <<< "${1//\n/}"
    for i in "${!xs[@]}"; do
        IFS=":" read -ra x <<< "${xs[$i]//\"/}"
        printDefListItem "${x[0]}" "${x[1]}" $color1 $color2 $5
    done
}

"$@"
