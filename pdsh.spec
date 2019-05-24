#
# spec file for package pdsh
#
# Copyright (c) 2017 SUSE LINUX GmbH, Nuernberg, Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via http://bugs.opensuse.org/
#


#
#%if 0%{!?sle_version:1} || 0%{?sle_version} >= 120300 || (0%{!?is_opensuse:1} && 0%{?sle_version} >= 120200)
#%define have_munge 1
#%define have_slurm 1
#%endif
%define have_munge 0
%define have_slurm 0

Name:           pdsh
#BuildRequires:  dejagnu
BuildRequires:  openssh
BuildRequires:  readline-devel
%if 0%{?have_slurm}
BuildRequires:  slurm-devel
%endif
%if 0%{?have_munge}
BuildRequires:  munge-devel
%endif
BuildRequires:  pam-devel
%if (0%{?suse_version} >= 1315)
Recommends:     mrsh
%endif
%if 0%{?have_genders}
BuildRequires:  genders > 1.0
%endif
Url:            http://pdsh.googlecode.com/
Version:        2.33
Release:        39.1
Summary:        Parallel remote shell program
# git clone of https://code.google.com/p/pdsh/
License:        GPL-2.0+
Group:          Productivity/Clustering/Computing
Source:         https://github.com/chaos/%{name}/releases/download/%{name}-%{version}/%{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
# Prereq: 
# Set this to 1 to build with genders support and framework for
# running Elan jobs.
%define chaos 0

%description
Pdsh is a multithreaded remote shell client which executes commands on
multiple remote hosts in parallel.  Pdsh can use several different
remote shell services, including Kerberos IV and ssh.

%prep
%setup -q 

%build
export CFLAGS="%{optflags} -fno-strict-aliasing"
%configure \
	--with-readline \
	--with-machines=/etc/pdsh/machines \
	--with-ssh \
	--with-dshgroups \
	--with-netgroup \
        --with-rcmd-rank-list="ssh %{?have_munge:mrsh} krb4 qsh mqsh exec xcpu" \
        --with-pam \
        --with-exec \
        %{?have_genders:--with-genders} \
        %{?have_munge:--with-mrsh} \
        %{?have_slurm:--with-slurm} \
	--without-rsh \
	--disable-static
make

%install
%make_install
rm -f %buildroot/%_libdir/pdsh/*.la

%files
%defattr(-,root,root)
%doc README DISCLAIMER.* README.* NEWS COPYING TODO
%attr(755, root, root) /usr/bin/pdsh
%attr(755, root, root) /usr/bin/pdcp 
/usr/bin/dshbak
/usr/bin/rpdcp
%{_mandir}/man1/pdsh.1.gz
%{_mandir}/man1/pdcp.1.gz
%{_mandir}/man1/dshbak.1.gz
%{_mandir}/man1/rpdcp.1.gz
%_libdir/pdsh

%changelog
* Thu May 23 2019 eich@suse.com
- Recommends only works on SLES
- Disable munge and slurm options
* Mon Oct  9 2017 eich@suse.com
- Removed deprecated %%leap_version from spec file.
* Sat Oct  7 2017 jengelh@inai.de
- Remove --with-pic which is a no-op due to --disable-static.
- Replace old RPM constructs.
* Fri Oct  6 2017 eich@suse.com
- Update to 2.33:
  * Fix segfault and build issues on Mac OSX (#95)
  * Always pass RTLD_GLOBAL to dlopen(3) of modules. Fixes missing symbol
    errors from modules using libraries that also use dlopen() (e.g.
    nodeupdown, slurm)
  From 2.32:
  * Autotools update
  * Switch to dlopen(3)/dlsym(3) instead of using libltdl
  * Drop qshell, mqshell, rmsquery, nodeattr and sdr modules.
  * Fix issue 70: dshbak: handle hostname of "0"
  * Allow PDSH_CONNECT_TIMEOUT and PDSH_COMMAND_TIMEOUT environment
    variables (Erik Jacobson)
  * Fix some old URLs in documentation (Al Chu)
  * Avoid exporting POSIXLY_CORRECT to child processes (Dorian Krause)
  * Fix mcmd start offset bug in max bytes calculation (Egbert Eich)
- Removed:
  mcmd-Account-for-start-offset-when-providing-max-bytes-to-read.patch:
  Obsoleted by update.
* Fri Mar 10 2017 eich@suse.com
- Fix %%if clause in spec file.
* Thu Feb 16 2017 eich@suse.com
- mcmd-Account-for-start-offset-when-providing-max-bytes-to-read.patch
  Fix a write past the end of a buffer.
* Wed Feb 15 2017 eich@suse.com
- Add 'Recommends: mrsh':
  pdsh should be run using the mrsh protocol but can get by using
  ssh as well, thus adding as a recommended dependency.
* Mon Nov 21 2016 eich@suse.com
- Disable support for slurm and mrsh until it is in Factory.
* Tue Nov  8 2016 eich@suse.com
- Add support for: pam, exec, mrsh and slurm
  genders will follow later. We don't have support for this lib, yet.
* Sat Oct 22 2016 eich@suse.com
- Replace tarball with official tarball of 2.31. (Content identical).
  (Add download rpm).
- Add _service for download_files.
- Remove .la files from installation.
* Wed Oct 19 2016 eich@suse.com
- Importing to SLE-12-SP2 for FATE#321714.
* Mon Aug 10 2015 jkeil@suse.de
- Don't include the rsh module, because rsh is outdated, deprecated and upstream
  is dead.  Removing the dependency makes it possible to drop the rsh package.
* Thu Jan 30 2014 tabraham@suse.com
- update to version 2.31 (2013-11-07)
  - - updated to git tag pdsh-2.31 (rev:e1c8e71dd6a2)
  - - Fix issue 56: slurm: Allow mixed use of -P, -w and -j options.
  - - Fix issue 59: pdsh very slow when using a few thousand hosts and genders.
  - - testsuite: Expanded tests for genders module (Pythagoras Watson)
- Changes from pdsh-2.30 (2013-03-02)
  - - Fix issue 55: genders -X option removes more hosts than expected.
    (This was a generic fix for hostname matching, so it probably
    affected -x and other options as well.)
  - - testsuite: Add test for issue 55.
* Wed Oct  2 2013 david.bahi@emc.com
- update to version 2.29 (2013-02-12)
  - - Fix issue 42: --with-dshgroup sets DSHGROUP_PATH to "yes"
  - - Fix issue 53: Add -P option to target SLURM partitions (Michael Fenn)
  - - Fix issue 54: pdsh prints empty lines with -S
  - - pdcp: Add more levels of directory recursion (Pythagoras Watson)
* Mon Dec  3 2012 tabraham@suse.com
- update to version 2.28
  - - Fix issue 39: ssh forces use of -l<user> option
  - - Fix issue 40: -l%%u added to ssh args only if remote and local
    usernames differ
- update to version 2.27
  - - Fix issue 17: Allow dshgroup files to include other files
  - - Fix issue 33: dshbak breaks up host lists at zeropad boundaries,
    (e.g. 01-09,10-11, 010-099,100-101, etc.)
  - - Fix issue 34: dshgroup path override broken in ./configure
  - - Fix issue 36: pdsh truncates output lines at 8K
  - - dshgroup: Allow dshgroup search path to be overridden by DSHGROUP_PATH,
    a colon-separated list of directories to search. $HOME/.dsh/group
    is still always prepended to this path.
  - - Allow wcoll files (-w ^file and WCOLL=file) to include other files
    with a "#include FILE" syntax. If included files have no path, then
    a search path of the dirname of the included file ("." for stdin)
    is used. -- Fix issue 17: Allow dshgroup files to include other files
  - - Fix issue 33: dshbak breaks up host lists at zeropad boundaries,
    (e.g. 01-09,10-11, 010-099,100-101, etc.)
  - - Fix issue 34: dshgroup path override broken in ./configure
  - - Fix issue 36: pdsh truncates output lines at 8K
  - - dshgroup: Allow dshgroup search path to be overridden by DSHGROUP_PATH,
    a colon-separated list of directories to search. $HOME/.dsh/group
    is still always prepended to this path.
  - - Allow wcoll files (-w ^file and WCOLL=file) to include other files
    with a "#include FILE" syntax. If included files have no path, then
    a search path of the dirname of the included file ("." for stdin)
    is used.
  - - Fix some minor memory leaks and locking bugs reported by Coverity.
* Wed Nov  2 2011 cfarrell@suse.com
- license update: GPL-2.0+
  SDPX format (http://www.spdx.org/licenses)
* Tue Nov  1 2011 tabraham@novell.com
- update to version 2.26
  - - Fix issue 14: interactive mode broken with ssh
  - - Fix issue 19: missing commas in dshbak(1) header output
  - - Fix issue 20: compilation error in genders.c with non-GCC compilers
  - - Fix issue 23: compilation failure with --enable-static-modules
  - - Fix issue 24: don't arbitrarily limit usernames to 16 characters
  - - Fix issue 25: PDSH_SSH_ARGS should not require %%u and %%h
  - - Fix issue 26: document use of %%u and %%h in PDSH_SSH_ARGS
  - - Fix interactive mode with rcmd/exec.
  - - genders: do not look for genders_query(3) support at runtime,
    as this causes too many problems on some systems. Instead,
    use autoconf to include or exclude genders_query support from
    the genders module. (fixes Issue 1)
- update to version 2.25
  - - Fix pdcp breakage with ssh (bug introduced in pdsh-2.24).
    (Resolves issue 12: pdcp executes file instead of copying.)
  - - testsuite: Skip tests dependent on PDSH_MODULE_DIR when testsuite
    run as root (Resolves issue 13: testsuite broken when run as root)
  - - testsuite: Skip dshbak -d test to non-writable directory when
    directory permissions do not seem to apply (e.g. privileged user)
    (Possibly resolves issue 11: tests fail on Mac OSX under fink)
  - - testsuite: add simple ssh teststestsuite: add simple ssh tests
- update to version 2.24
  - - Resolve issue 7: Allow PDSH_REMOTE_PDCP_PATH to set default path
    to remote pdcp program (pdcp -e).
  - - Resolve issue 9: Fix use of PDSH_SSH_ARGS_APPEND.
  - - Resolve issue 10: dshbak: Support writing output to file-per-host.
    Adds new -d DIR and -f options to dshbak.
  - - genders: Allow relative paths to genders files with -F and
    PDSH_GENDERS_FILE.
  - - genders: Don't print an error if genders file is missing, unless
    a genders optin (-F, -a, -g, -i, -X) is explicitly used.
  - - genders: Allow -g to be used with other node selection options as
    a filter. For example: pdsh -w host[0-1024] -g attr1 ...
  - - ssh: Better preservation of remote command args in ssh module.
    Previous versions of pdsh would alwas collapse all args into
    a single argument passed to ssh: "cmd arg1 arg2 ..." With this
    fix the argv list will more closely match the form passed to pdsh
  - - Refactored large portions of dshbak, improve usage output,
    and update manpage
  - - Expanded testsuite.
- update to version 2.23
  - - Fix issue 4: List available but conflicting modules in -V and -L output
  - - Fix issue 5: dshbak -c doesn't properly coalesce hosts with different
    zero-padding in the numeric suffix.
  - - Added torque module for setting list of target hosts based on Torque/PBS
    jobs (Issue 2).
  - - Enhance syntax of -w and -x to allow preceeding arguments with:
    `-' - Exclude hosts instead of include with -w ( -w foo[1-9],-foo8)
    `^' - insert/exclude list of hosts from a file (^/path/to/file)
  `/' - filter hosts based on regex (/host.*0$/)
  - - Introduce new pdsh testsuite with many new tests. See tests/README
    for more information
* Thu Nov 18 2010 hvogel@novell.com
- update to version 2.22
  - - Sort modules by name before initialization so that modules
    initialize in a reproducible order.
  - - New option -M name,... forces load of misc modules by
    name, thus allowing users to select between conflicting
    modules.
  - - Fix parsing of hostlist expressions with multiple brackets
  - - Fix for coredump when no rcmd module is loaded.
  - - Fix duplicate error output from ssh module.
  - - Add -e option to pdcp to explicitly specify remote execution
    path.
* Wed May 12 2010 puzel@novell.com
- build with support for dshgroup and netgroup (bnc#477720)
* Fri Apr 11 2008 crrodriguez@suse.de
- fix build with glibc 28, ARG_MAX no longer defined
- update to version 2.16
- Rewrite of the ssh module using the same framework as the existing
  "exec" module.
- Ability to specify an ssh connect timeout.
- Small improvements for the dshbak script.
- Other minor fixes to the pdsh interface.
- See the NEWS file distributed with pdsh for further information.
* Thu Apr  3 2008 hvogel@suse.de
- update to 2.14
  * some build fixes
  * Enable "exec" rcmd module by default
  * Ignore blank and comment lines in WCOLL file
  * Add new "pipecmd" API for executing arbitrary commands
  * Add "-N" option to disable hostname
  * Block SIGCHLD in pdsh threads
  * Undocumented -K option to explicitly keep
    domain names in output labels
* Mon Apr 30 2007 ro@suse.de
- added rpdcp to filelist (binary and manpage)
* Wed Apr 25 2007 mskibbe@suse.de
- update to version 2.12 which includes:
  o pdsh-2.10.patch
  o fix build warnings
  o fix bugs
* Thu Aug 31 2006 mskibbe@suse.de
- update to version 2.10 which
  o allow rcmd modules to set rcmd-specific options
  o Add test for "," in host range. Increase version number
  o Add COPYING to docs. Remove -n from %%setup
  o Add support for command history in interactive mode when using
    readline (History file is placed in ~/.pdsh/history)
  o Change mini shell script so -S hack will work
* Thu Jul 13 2006 mskibbe@suse.de
- update to version 2.9 which
  o Remove unneeded .la and .a files in packages
  o Use io session file instead of stdout and stdin session files
  o Remove code which only loaded pdsh modules via *.la files
  o Add xcpu module support
  o Do not install pdsh/pdcp setuid root by default anymore
  o Update documentation
* Wed Jan 25 2006 mls@suse.de
- converted neededforbuild to BuildRequires
* Tue Jan 17 2006 hvogel@suse.de
- disable make check for now
* Fri Jan 13 2006 hvogel@suse.de
- update to version 2.8
* Wed Jun  8 2005 meissner@suse.de
- use RPM_OPT_FLAGS -fno-strict-aliasing
* Tue Jun  7 2005 hvogel@suse.de
- update to version 2.3
* Thu Feb 26 2004 hmacht@suse.de
- building as non-root
* Sun Jun 15 2003 nashif@suse.de
- Initial release (1.7-6)
