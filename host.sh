#!/bin/sh
#set -x
# File: host.sh
#
# Return system ID on stdout (all on one line) as:
#
# cpu:<cpu name> os:<os name> path:<path component> version:<n> \
# revision:<n> export:<n> dist:<name> dist_version:<n> dist_revision:<n>
#
# e.g., "cpu:I386 os:LINUX path:i386-linux version:2.4 \
#        revision:18 export:linux-x86 dist:RedHat dist_version:7 dist_revision:3\n"
#
# some valid cpu names are: sun3 sun4 alpha mips hp800 hp700 i386
# some valid OS names are: sunos solaris osf1 ultrix hp-ux linux
#
# Note: dist:<name>, dist_version:<n>, and dist_revision:<n>
# are generated only for known Linux systems.
#
# Update log
#
# Nov 28 2006 JVD: Set "dist_revision" to the RHEL "Update" number.
# Mar  3 2006 JVD: Use i386-darwin instead of x86-darwin.
# Feb  1 2005 RMM: Mac OS X: Corrected Darwin to seek i386 vice x86 in uname.
# Aug 12 2005 JVD: Mac OS X: Added Darwin-x86.
# May  4 2005 JVD: Mac OS X: use sw_vers to figure out the OS version.
# Dec 27 2004 JVD: Mac OS X Darwin-Power: Added mapping from Darwin version to Mac OS X version.
# Oct  1 2004 JVD: Distinguish between SLES and SuSE distribution names.
#		   Distinguish between RedHatFC and RedHat distribution names.
#		   Make darwin-power the export path for MAC OS X.
# Dec  1 2003 JVD: Added Power (ppc and ppc64) on Linux.
# Nov 12 2003 JVD: Added RedHatEL distribution name.
# Sep 18 2003 JVD: Added Linux distribution name for SuSE.
# Aug  7 2003 RWG: Add Mac OSX support
# Jul 11 2003 JVD: Added AMD x86_64 on Linux.
# Jun 26 2003 RWG: Add the Linux distribution name, version, and revision.
#                  Add support for RedHat initially. For some build decisions,
#                  the distribution version is more useful than the kernel
#                  version.
# Jun 17 2003 RTF: Added HPUX IA64.
# Jan 23 2003 RWG: Add a bit of extra code to distinguish between a
#                  stock RH 7.2 and RH 7.2 with the recommended updates
#                  to a 2.4-18 kernel (e.g. my home machine).
# Dec  7 2002 JVD: Set the export field to linux-ia64 instead of ia64-linux.
#		   This makes it consistent with the other Linux platform 
#                  export fields.
# Jul 12 2001 JVD: Recognize 32-bit "IRIX" machines.
# Jun 26 2001 JVD: Permit [BDESTVX] as verion type letter on Tru64.
# Aug 31 2000 JVD: Add the export: tagged value to spitout the platform tags
#		used by totalview historically.
#
#----------------------------------------------------------------------------
# $Id: host.sh,v 1.40 2007/01/19 18:38:08 jdelsign Exp $

# pull indicators out of uname

system=`uname -s`
machine=`uname -m`
version=`uname -v`
revision=`uname -r`

dist_name=""
dist_version=""
dist_revision=""

v=0
r=0

# Prepend system with an X, in case uname wasn't found

case X${system} in
  XOSF1)     os="OSF1"; 
   case X${machine} in
    Xmips)    p="mips"      ;;
    X9000/7*) p="hp700-osf"  ;;
    Xalpha)   p="alpha"
	      v=`expr $revision : "[BDESTVX]\([0-9]\)"`
	      r=`expr $revision : "[BDESTVX][0-9]\.\([0-9]*\)"`
	      ;;
    *)        p="osfx"      ;;
   esac
  ;;

  XSunOS)
    case X$revision in
      X5*)
        case X$machine in
	  Xi86pc) os="SOLARIS"; p="sun5-x86" ;;
	  *)	 os="SOLARIS"; p="sun5" ;;
	esac
	;;
      *)
	case X$machine in
	  Xsun3) os="SUNOS";   p="sun3" ;;
	  *)   	 os="SUNOS";   p="sun4" ;;
	esac
	;;
    esac 

    v=`expr $revision : "\([0-9]\)"`         # SunOS=4, Solaris=5
    r=`expr $revision : "[0-9]\.\([0-9]*\)"`
    ;;

  XHP-UX)    
    os="HPUX"
    v=`expr $revision : "B\.\([0-9][0-9]\)"`
    r=`expr $revision : "B\.[0-9][0-9]\.\([0-9]*\)"`

    case X$machine in
      X9000/3*) p="hp800" ;;
      X9000/4*) p="hp800" ;;
      X9000/8*) p="hp800" ;;
      X9000/7*) p="hp800" ;;
      Xia64)    p="ia64-hpux" ;;
      *)        p="hpux11-xxx" ;;
    esac
    ;;

  XAIX)
    os="AIX"
    p="rs6000"
    machine="RS6000" 
    v=${version}
    r=${revision}
    ;;

  XULTRIX)   os="ULTRIX";  p="vax"     ;;

  XLynxOS)
   os="LYNXOS"
#   case X$revision in
#	X2.2.*)     os="LYNXOS-2.2";;
#	X2.3.*)     os="LYNXOS-2.3";;
#	*)          os="LYNXOS";;
#   esac;
   case X${machine} in
    Xi386)    p="i386-lynx"  ;;
    XuSPARC1) p="sparc-lynx" ;;
    Xm68040)  p="m68k-lynx"  ;;
    XPowerPC) p="ppc-lynx"   ;;
    *)        p="x-lynx"     ;;
   esac
  ;;

  Xdgux)
    os="DGUX";
    machine=`uname -p`;
    case X${machine} in
      XPentium) p="i386-dgux";;
      *)        p="m88k-dgux";;
    esac
    ;;

  XUNIX_SV)
   os="UNIXWARE";
   case X${machine} in
     Xi386) p="i386-unixware" ;;
     *)     p="xxx-unixware" ;;
   esac
   ;;

  X*WIN32*)
    if [ "$NUTC" = "NUTC" ]; then 
        os="NUTC"
        p="nutc"
    else
        os="WIN32"
        p="win32"
    fi
    ;;

  XWindows_NT)    # uname under MKS
    if [ "$NUTC" = "NUTC" ]; then 
        os="NUTC"
        p="nutc"
    else
        os="WIN32"
        p="win32"
    fi
    ;;

  X*CYGWIN*)
    os="WIN32"
    p="win32"
    ;;

  XIRIX64 | XIRIX)
    machine=mips64;
    case X${revision} in
      X6*)   os="IRIX6"; p="mips64-irix6" ;;
      *)     os="UNKNOWN"; p="unknown" ;;
    esac
    v=`expr $revision : "\([0-9]\)"`
    r=`expr $revision : "[0-9]\.\([0-9]*\)"`
    ;;

  XLinux)
    case X$machine in
      Xi*86)    p="i386-linux" ;;
      Xalpha)   p="alpha-linux" ;;
      Xia64)    p="ia64-linux" ;;
      Xx86_64)  p="x86-64-linux" ;;
      Xppc)     p="power-linux" ;;
      Xppc64)   p="power-linux" ;;
      *)        p="xxx-linux" ;;
    esac
    os="LINUX"
    v=`expr $revision : "\([0-9]\.[0-9]\)"`      # kernel version (e.g. 2.0)
    r=`expr $revision : "[0-9]\.[0-9]\.\([0-9]*\)"`

    # for RedHat Linux, extract the distribution name and version

    if [ -f /etc/redhat-release ] ; then
      vers=`cat /etc/redhat-release`

      if [ `expr "$vers" : "Red Hat Enterprise Linux [AEW]S release "` != 0 ]; then
	dist_name="RedHatEL"
	vers=`expr "$vers" : "Red Hat Enterprise Linux [AEW]S release \([0-9]\+\(\(\.[0-9]\+\)\|\( (.* Update [0-9]\+)\)\)\?\)"`
      elif [ `expr "$vers" : "Fedora Core release "` != 0 ]; then
	dist_name="RedHatFC"
	vers=`expr "$vers" : "Fedora Core release \([0-9]\+\(\.[0-9]\+\)\?\)"`
      elif [ `expr "$vers" : "Red Hat Linux release "` != 0 ]; then
	dist_name="RedHat"
	vers=`expr "$vers" : "Red Hat Linux release \([0-9]\+\(\.[0-9]\+\)\?\)"`
      else
	dist_name="RedHatUNKNOWN"
	vers="0.0"
      fi

      dist_version=`expr "$vers" : "\([0-9]\+\)"`
      if [ `expr "$vers" : "[0-9]\+ (.* Update [0-9]\+)"` -gt 0 ]; then
	dist_revision=`expr "$vers" : "[0-9]\+ (.* Update \([0-9]\+\))"`
      else
	dist_revision=`expr "$vers" : "[0-9]\+\.\([0-9]\+\)"`
      fi
      if [ -z "$dist_revision" ] ; then
        dist_revision="0"
      fi

      # The recommended patches update the RH  7.2 kernel to 2.14.18.
      # Some test predicates confuse this with RH 7.3. Tack -rh72 to r to
      # distinguish this special case

       if [ "$r" = "18" -a "$vers" = "7.2" ]; then
        r="$r-rh72"
      fi
    elif [ -f /etc/SuSE-release ] ; then
      if egrep -q '(Enterprise Server)|(SLES)' /etc/SuSE-release; then
	dist_name="SLES"
      else
	dist_name="SuSE"
      fi

      vers=`awk '/^VERSION/ { print $3 }' /etc/SuSE-release`

      dist_version=`expr "$vers" : "\([0-9]\+\)"`
      dist_revision=`expr "$vers" : "[0-9]\+\.\([0-9]\+\)"`
      if [ -z "$dist_revision" ] ; then
        dist_revision="0"
      fi
    elif [ -f /etc/lsb-release ] ; then
        dist_name="Ubuntu"
        if [ -f /etc/os-release ] ; then
            codename=$(cat /etc/os-release | awk '/^VERSION=/' | xargs -I '{}' expr '{}' : 'VERSION=[0-9]\+\.[0-9]\+ \+\(.*\)')
            dist_name="$dist_name-$codename"
        fi
        vers=$(lsb_release -a 2>/dev/null | awk '/^Release/' | awk '{ print $NF }')
        dist_version=`expr "$vers" : "\([0-9]\+\)"`
        dist_revision=`expr "$vers" : "[0-9]\+\.\([0-9]\+\)"`
        if [ -z "$dist_revision" ] ; then
          dist_revision="0"
        fi
    fi
    ;;

  XDarwin)
    os="DARWIN"
    case X${machine} in
     "XPower Macintosh") p="power-darwin" ;;
     "Xi386")            p="i386-darwin" ;;
      *)                 p="xxx-darwin"   ;;
    esac
    v=`expr $revision : "\([0-9]\)"`
    r=`expr $revision : "[0-9]\.\([0-9]*\)"`
    dist_name="MacOSX"
    dist_vers=`sw_vers -productVersion`
    dist_version=`expr "$dist_vers" : "\([0-9]\{1,\}\)"`
    dist_revision=`expr "$dist_vers" : "[0-9]\{1,\}\.\([0-9]\{1,\}\)"`
    ;;

  *)         os="UNKNOWN"; p="unknown" ;;
esac

# figure out machine type
case X${machine} in
    Xalpha)   cpu="ALPHA"   ;;
    Xmips)    cpu="MIPS"    ;;
    Xmips64)  cpu="MIPS64"  ;;
    XRISC)    cpu="MIPS"    ;;	# mips ultrix
    Xsun3)    cpu="SUN3"    ;;
    Xsun4*)   cpu="SUN4"    ;;
    Xsun386)  cpu="SUN386"  ;;
    XVAX)     cpu="VAX"     ;;
    X9000/3*) cpu="HP300"   ;;
    X9000/4*) cpu="HP300"   ;;
    X9000/8*) cpu="HP800"   ;;
    X9000/7*) cpu="HP800"   ;;
    Xi386)    cpu="I386"    ;;
    XuSPARC1) cpu="SPARC"   ;;
    Xm68040)  cpu="M68K"    ;;
    XAViiON)  cpu="M88K"    ;;  # by Data General
    XPentium) cpu="I386"    ;;
    XRS6000)  cpu="RS6000"  ;;
    XPowerPC) cpu="PPC"     ;;
   "XPower Macintosh") cpu="POWER" ;;
    Xppc)     cpu="POWER"   ;;
    Xppc64)   cpu="POWER"   ;;
    Xi*86)    cpu="I386"    ;;
    X586)     cpu="I386"    ;;
    Xi86pc)   cpu="I386"    ;;
    Xx86)     cpu="I386"    ;;
    Xia64)    cpu="IA64"    ;;
    Xx86_64)  cpu="X86_64"  ;;
    *)        cpu="UNKNOWN" ;;
esac

# Map the path to the values TV's has used historically
case X${p} in
    Xi386-linux)	exp=linux-x86	;;
    Xalpha-linux)	exp=linux-alpha	;;
    Xia64-linux)	exp=linux-ia64	;;
    Xpower-linux)	exp=linux-power	;;
    Xia64-hpux) 	exp=hpux11-ia64	;;
    Xx86-64-linux)	exp=linux-x86-64;;
    Xmips64-irix6)	exp=irix6-mips	;;
    Xhp800)		exp=hpux11-hppa	;;
    Xpower-darwin)	exp=darwin-power;;
    Xi386-darwin)	exp=darwin-x86;;
    *)			exp="$p"	;;
esac

# Label the distribution info if any is available

if [ -n "$dist_name" ] ; then
  dist_name="dist:$dist_name"
fi

if [ -n "$dist_version" ] ; then
  dist_version="dist_version:$dist_version"
fi

if [ -n "$dist_revision" ] ; then
  dist_revision="dist_revision:$dist_revision"
fi

# tell the caller

echo cpu:$cpu os:$os path:$p version:$v revision:$r export:$exp \
    $dist_name $dist_version $dist_revision
