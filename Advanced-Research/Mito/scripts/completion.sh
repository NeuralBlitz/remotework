#!/bin/bash
# Mito CLI Completion Script

_mito() {
    local cur prev opts
    COMPREPLY=()
    cur="${COMP_WORDS[COMP_CWORD]}"
    prev="${COMP_WORDS[COMP_CWORD-1]}"
    
    opts="-v --version -l --list -h --help"
    commands="llama ocr textgen classify sentiment speech translate embed summarize qa tts detect segment rag agent chat server"
    
    if [[ ${COMP_CWORD} -eq 1 ]] ; then
        COMPREPLY=( $(compgen -W "${opts} ${commands}" -- ${cur}) )
        return 0
    fi
    
    case "${prev}" in
        llama)
            COMPREPLY=( $(compgen -f -- ${cur}) )
            return 0
            ;;
        ocr|classify|detect|segment)
            COMPREPLY=( $(compgen -f -- ${cur}) )
            return 0
            ;;
        textgen|summarize|translate|sentiment|embed)
            return 0
            ;;
        qa)
            return 0
            ;;
        chat)
            COMPREPLY=( $(compgen -f -- ${cur}) )
            return 0
            ;;
        server)
            opts="--host --port --help"
            COMPREPLY=( $(compgen -W "${opts}" -- ${cur}) )
            return 0
            ;;
        *)
            ;;
    esac
    
    COMPREPLY=( $(compgen -W "${commands}" -- ${cur}) )
}

complete -F _mito mito
