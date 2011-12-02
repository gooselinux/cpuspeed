Summary:        CPU frequency adjusting daemon
Name:           cpuspeed
Version:        1.5
Release:        15%{?dist}
Epoch:          1
Group:          System Environment/Base
License:        GPLv2+
URL:            http://carlthompson.net/Software/CPUSpeed
Source0:        http://carlthompson.net/downloads/cpuspeed/cpuspeed-%{version}.tar.bz2
Source1:        http://carlthompson.net/downloads/cpuspeed/license.txt
Source2:        cpuspeed.init
Source3:        cpuspeed.conf
Source4:        cpuspeed.8
Buildroot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires(post):  /sbin/chkconfig
Requires(preun): /sbin/chkconfig
Requires(preun): /sbin/service

BuildRequires:  automake util-linux groff gettext
ExclusiveArch:	%{ix86} x86_64 ppc ppc64 ia64 sparcv9 sparc64
Obsoletes:	kernel-utils

Patch1:         cpuspeed-1.5-Makefile.patch
Patch2:         cpuspeed-1.5-no-affected_cpus-fallback.patch

%description
cpuspeed is a daemon that dynamically changes the speed
of your processor(s) depending upon its current workload
if it is capable (needs Intel Speedstep, AMD PowerNow!,
or similar support).

This package also supports enabling cpu frequency scaling
via in-kernel governors on Intel Centrino and AMD
Athlon64/Opteron platforms.

%prep
%setup -q
cp %{SOURCE1} .
%patch1 -p1 -b .make
%patch2 -p1 -b .ac

%build
rm -rf $RPM_BUILD_ROOT

RPM_OPT_FLAGS=$(echo $RPM_OPT_FLAGS | sed -e 's/-fexceptions/-fno-exceptions/g')
make CFLAGS="$RPM_OPT_FLAGS -fpie -pie" LDFLAGS="-Wl,-z,relro,-z,now"

%install
mkdir -p $RPM_BUILD_ROOT%{_sbindir}
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man8/

make DESTDIR=$RPM_BUILD_ROOT install
install -m755 %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d/cpuspeed
install -m644 %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/cpuspeed
install -m644 %{SOURCE4} $RPM_BUILD_ROOT%{_mandir}/man8/cpuspeed.8

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && [ -d $RPM_BUILD_ROOT ] && rm -rf $RPM_BUILD_ROOT;

%files
%defattr(-,root,root,-)
%doc license.txt CHANGES CONTRIBUTORS EXAMPLES FEATURES README USAGE
%{_sbindir}/cpuspeed
%{_sysconfdir}/rc.d/init.d/cpuspeed
%{_mandir}/man8/*
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/sysconfig/cpuspeed

%preun
if [ "$1" = "0" ] ; then
  /sbin/service cpuspeed stop >/dev/null 2>&1 || :
  /sbin/chkconfig --del cpuspeed
fi

%post
/sbin/chkconfig --add cpuspeed

%triggerpostun -- kernel-utils
/sbin/chkconfig --add cpuspeed
exit 0

%changelog
* Tue Jul 20 2010 Matthew Garrett <mjg@redhat.com> 1:1.5-15
- Init scipt: Add support for loading the pcc-cpufreq driver
- Resolves: rhbz#609659

* Wed Jun 30 2010 Petr Sabata <psabata@redhat.com> - 1:1.5-14
- Init script: added the reload function
- Init script: the service now stops when using p4-clockmod driver
- Resolves: rhbz#607223

* Fri Nov 13 2009 Jarod Wilson <jarod@redhat.com> 1.5-13
- Move startup prio so we start after syslog, so any notices during
  system startup actually get logged

* Tue Aug 04 2009 Adam Jackson <ajax@redhat.com> 1.5-12
- Move buildroot dir creation to %%install

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.5-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Jun 26 2009 Jarod Wilson <jarod@redhat.com> 1.5-10
- Fix #505837 for real this time, even tested on an actual
  p4-clockmod system, seems to DTRT

* Mon Jun 22 2009 Jarod Wilson <jarod@redhat.com> 1.5-9
- Un-pooch fix for #505837 (caused #507216 and didn't work right
  to begin with...)

* Wed Jun 17 2009 Jarod Wilson <jarod@redhat.com> 1.5-8
- Let p4-clockmod users override defaults and set a governor,
  even if its generally a Bad Idea... (#505837)

* Wed Jun 10 2009 Jarod Wilson <jarod@redhat.com> 1.5-7
- Fix up lsb compliance a bit (#246895)
- Correct a few more exit codes (rhel5 bz, #495049)

* Tue Mar 17 2009 Jarod Wilson <jarod@redhat.com> 1.5-6
- Fix up prior fix-up so that status and stop actually do the right thing
  on NON-p4-clockmod systems

* Fri Mar 06 2009 Jarod Wilson <jarod@redhat.com> 1.5-5
- Fix up p4-clockmod support so start/stop/status actually report
  something sane to the user

* Mon Mar 02 2009 Jarod Wilson <jarod@redhat.com> 1.5-4
- Fix up ExclusiveArch, now that 32-bit x86 is built i586 for F11

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Nov 03 2008 Jarod Wilson <jarod@redhat.com> 1.5-2
- Revive p4-clockmod support, for passive cooling only, when
  all else fails on Intel boxes

* Wed Oct 08 2008 Jarod Wilson <jarod@redhat.com> 1.5-1
- Update to v1.5 release

* Fri Sep 26 2008 Jarod Wilson <jarod@redhat.com> 1.2.1-9
- backport proper multicore support for userspace governor
  (cpuspeed daemon) case from v1.5 cpuspeed snapshot

* Tue Jul 15 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.2.1-8
- fix license tag

* Sun May 11 2008 Dennis Gilmore <dennis@ausil.us> 1.2.1-7
- add sparcv9 sparc64 to list of arches

* Wed Mar 12 2008 Jarod Wilson <jwilson@redhat.com> 1.2.1-6
- Minor formatting and redirection fixups

* Thu Feb 14 2008 Jarod Wilson <jwilson@redhat.com> 1.2.1-5
- Support for powernow-k8 as a kernel module

* Tue Feb 12 2008 Jarod Wilson <jwilson@redhat.com> 1.2.1-4
- Fix up for gcc 4.3
- Work around multi-core step detection problems (#392781)

* Wed Aug 29 2007 Jarod Wilson <jwilson@redhat.com> 1.2.1-3
- Bump and rebuild, due to busted ppc32

* Sat Jul 07 2007 Jarod Wilson <jwilson@redhat.com> 1.2.1-2
- Account for the cpuidle feature in rawhide kernels,
  slated for release in kernel 2.6.23 (#247352)

* Mon Jun 11 2007 Jarod Wilson <jwilson@redhat.com>
- Add e_powersaver (new Via C3 cpufreq driver) to list
  of those which should use ondemand governor by default

* Thu Apr 26 2007 Jarod Wilson <jwilson@redhat.com>
- Add a bit to the config file documentation
- Use variable for program name
- Fix up exit codes (#237942)

* Mon Mar 12 2007 Jarod Wilson <jwilson@redhat.com>
- Try loading acpi-cpufreq even on machines that don't
  report est flag (#231783, #216702)
- Tighten up formatting in initscript

* Wed Feb 21 2007 Jarod Wilson <jwilson@redhat.com>
- Default to ondemand governor w/acpi-cpufreq driver
- Minor initscript output cleanup

* Sun Feb 04 2007 Jarod Wilson <jwilson@redhat.com>
- Fix up compile flags and misc other fixes for
  core/extras merge review (#225658)

* Thu Jan 11 2007 Jarod Wilson <jwilson@redhat.com>
- Fix error-suppression for systems that report support
  for est, but have it disabled in the bios (#220200)

* Thu Jan 11 2007 Jarod Wilson <jwilson@redhat.com>
- Fix up documentation in config file (#219926)
- Fall back cleanly to userspace governor on
  non-centrino/powernow-k8/p4-clockmod systems
- Update description to reflect support for
  kernel-space freq scaling

* Wed Jan 10 2007 Jarod Wilson <jwilson@redhat.com>
- Fix governor validation check
- Use ondemand by default on p4-clockmod systems

* Wed Jan 10 2007 Jarod Wilson <jwilson@redhat.com>
- Minor fix for cpuspeed daemon stop function

* Tue Jan 09 2007 Jarod Wilson <jwilson@redhat.com>
- Turn on ia64 builds (#216702)
- Fix status on xen kernels

* Tue Jan 09 2007 Jarod Wilson <jwilson@redhat.com>
- Move config file to /etc/sysconfig/cpuspeed, more
  appropriate for initscript configs (#152305)
- Manify 'cpuspeed --help' along with other details (#172655)
- Tweak cpuspeed default thresholds (#147565)

* Mon Jan 08 2007 Jarod Wilson <jwilson@redhat.com>
- Let non-centrino/powernow-k8 systems also use other
  validated governors (#219926)
- Fix cpuspeed daemon options settings (#221829)

* Fri Jan 05 2007 Jarod Wilson <jwilson@redhat.com>
- Fix status and condrestart for centrino/powernow-k8 (#219926)
- Give feedback when loading/unloading a cpufreq governor
- Rework config file and initscript to make it much easier
  for end-users to adjust frequency scaling setup (#151761)
- Log start/stop events with useful info
- Don't start on xen kernels (freq scaling not supported)

* Thu Dec 14 2006 Jarod Wilson <jwilson@redhat.com>
- Set lock file for centrino/powernow-k8 so status
  indicates we do have scaling working
- Fix up centrino/powernow-k8 stop function (#213999)

* Wed Nov 29 2006 Jarod Wilson <jwilson@redhat.com>
- Fix busted config file sourcing

* Mon Nov 27 2006 Jarod Wilson <jwilson@redhat.com>
- Spec tweaks to bring in line with Fedora packaging guidelines
- Add docs to package
- Mark config file as noreplace
- Be sure to stop service before uninstall

* Tue Nov 21 2006 Dave Jones <davej@redhat.com>
- Merge one more patch from Michal Jaegermann <michal@harddata.com> (#216816)

* Mon Nov 20 2006 Dave Jones <davej@redhat.com>
- Merge patch from Michal Jaegermann <michal@harddata.com>
  that solves the acpi-cpufreq problem in an improved
  way and fixes several other nits.

* Sat Oct 28 2006 Dave Jones <davej@redhat.com>
- Only load acpi-cpufreq on speedstep capable machines.
- Unload acpi-cpufreq if BIOS tables didn't exist or
  other acpi-cpufreq failures occured.

* Sat Jul 29 2006 Dave Jones <davej@redhat.com>
- Don't try to load acpi-cpufreq on non-ACPI machines. (#196446)

* Wed Jul 26 2006 Dave Jones <davej@redhat.com>
- Fix up retval & /var/lock/subsys/cpuspeed handling in initscript.

* Thu Jul 20 2006 Jim Paradis <jparadis@redhat.com>
- Enable on-demand governor usage for powernow-k8 as well as centrino

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1:1.2.1-1.35%{dist}.1
- rebuild

* Sat Jul  1 2006 Dave Jones <davej@redhat.com>
- Fix sched_mc_power_savings warning on centrino laptops.

* Wed Jun  7 2006 Dave Jones <davej@redhat.com>
- Remove a bunch of no-longer needed gunk from the initscript.
- Use on-demand governor on centrino/core based systems for now,
  as it seems to have a better effect.

* Thu Feb 23 2006 Dave Jones <davej@redhat.com>
- Fix broken init script. (Alexandre Oliva) [#182691]
  Taking ugly shell script to the next level.

* Tue Feb 21 2006 Dave Jones <davej@redhat.com>
- Missed another occurance of the same problem I fixed yesterday.

* Mon Feb 20 2006 Dave Jones <davej@redhat.com>
- Some ACPI BIOSes start counting CPUs at 0, some at 1. *sigh*  (#181673)

* Sat Feb 11 2006 Dave Jones <davej@redhat.com>
- rebuild.

* Thu Feb 09 2006 Dave Jones <davej@redhat.com>
- rebuild.

* Fri Dec 16 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt for new gcj

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Mon Nov 14 2005 Dave Jones <davej@redhat.com>
- Don't try and load acpi-cpufreq if we have no throttling states.

* Thu Sep 29 2005 Dave Jones <davej@redhat.com>
- On shutdown, restore speed to maximum before daemon exit.

* Fri Sep 23 2005 Dave Jones <davej@redhat.com>
- Use ACPI as a fallback driver if possible, if one didn't get loaded. (#160788)

* Mon May  9 2005 Dave Jones <davej@redhat.com>
- Fix debuginfo generation.

* Wed Apr  6 2005 Dave Jones <davej@redhat.com>
- Don't count nice time as idle time. (#132383)

* Tue Mar  1 2005 Dave Jones <davej@redhat.com>
- Rebuild for gcc4.

* Tue Feb  8 2005 Dave Jones <davej@redhat.com>
- Rebuild with -D_FORTIFY_SOURCE=2

* Fri Feb  4 2005 Dave Jones <davej@redhat.com>
- Enable builds for PPC (#147089)

* Tue Jan 11 2005 Dave Jones <davej@redhat.com>
- Add missing Obsoletes: kernel-utils

* Mon Jan 10 2005 Dave Jones <davej@redhat.com>
- Update to upstream 1.2.1 release.

* Sat Dec 18 2004 Dave Jones <davej@redhat.com>
- Initial packaging, split out from kernel-utils.

