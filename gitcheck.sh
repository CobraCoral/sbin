#!/usr/bin/zsh
#set -x

source colors.zsh
function print_color() {
    fg_color=$1
    bg_color=$2
    TEXT=$3
    print -P -- "%{$FG[$fg_color]%}%{$BG[$bg_color]%}$TEXT%{$reset_color%}"
}

for d in $(find . -maxdepth 3 -name .git); do
    d=$(dirname $d)
    cd $d
    local_changes=$(git status --porcelain | wc -l)
    local_changes_long=$(git status --porcelain)
    unpushed_changes=$(git rev-list HEAD@{upstream}..HEAD | wc -l)
    unpushed_changes_long=$(git rev-list --left-right --pretty HEAD@{upstream}..HEAD)
    if [[ $local_changes -gt 0 || $unpushed_changes -gt 0 ]]; then
        print_color 009 232 "=== [$d] ==="
        if [[ $local_changes -gt 0 ]]; then
          print_color 081 232 "$local_changes_long"
        fi
        if [[ $unpushed_changes -gt 0 ]]; then
          print_color 148 232 "$unpushed_changes_long"
        fi
        print_color 148 232 ""
    fi
    cd -
done
