#!/bin/bash
script="start-chain.sh"
#Declare the number of mandatory args
margs=2

consensus="pow"

full_path=$(realpath $0)
root=$(dirname $full_path)
echo $root

# Common functions - BEGIN
function example {
    echo -e "example: $script -p my_password -cs 3 -c pow -o2 VAL"
}

function usage {
    echo -e "usage: $script MANDATORY [OPTION]\n"
}

function help {
  usage
    echo -e "MANDATORY:"
    echo -e "  -p, --password  your_password  -- Your sudo password. Mininet requires root."
    echo -e "  -cs, --chain-size  number  -- The number of nodes in the desired chain.\n"
    echo -e "OPTION:"
    echo -e "  -c, --consensus poa/pow --  The consensus type for the chain poa or pow (pow is default)"
    echo -e "  -o1, --optional2   VAL  The desc of the optional1 String  parameter"
    echo -e "  -h,  --help             Prints this help\n"
  example
}

# Ensures that the number of passed args are at least equals
# to the declared number of mandatory args.
# It also handles the special case of the -h or --help arg.
function margs_precheck {
	if [ $2 ] && [ $1 -lt $margs ]; then
		if [ $2 == "--help" ] || [ $2 == "-h" ]; then
			help
			exit
		else
	    	usage
			example
	    	exit 1 # error
		fi
	fi
}

# Ensures that all the mandatory args are not empty
function margs_check {
	if [ $# -lt $margs ]; then
	    help
	    exit 1 # error
	fi
}
# Common functions - END

# Custom functions - BEGIN
# Put here your custom functions
# Custom functions - END

# Main
margs_precheck $# $1

marg0=
size=1
consensus="pow"
oarg1="default"

# Args while-loop
while [ "$1" != "" ];
do
   case $1 in
   -p  | --password )  shift 
				password=$1
                		  ;;
   -cs  | --chain-size )  shift 
				size=$1
			          ;;
   -c  | --consensus  )  shift 
				consensus=$1
                                  ;;
   -o1  | --optional1  )  shift 
				oarg1=$1
                          	  ;;
   -h   | --help )        help
                          exit
                          ;;
   *)                     
                          echo "$script: illegal option $1"
                          usage
						  example
						  exit 1 # error
                          ;;
    esac
    shift
done

# Pass here your mandatory args for check
margs_check $password $size

echo $consensus

# Your stuff goes here
echo $password | sudo -S python3 go-ethereum/containernet/ethereum-python-scripts/ethereum_net.py $size $consensus $root
