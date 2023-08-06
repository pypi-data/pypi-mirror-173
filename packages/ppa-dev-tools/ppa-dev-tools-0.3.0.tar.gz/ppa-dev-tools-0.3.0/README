Ppa Dev Tools
=============

ppa is a command line client for managing PPAs in Launchpad.

This primarily focuses on functionality needed by owners of PPAs, to
assist in their creation, deletion, and configuration.  A key
functionality is to poll and wait until the package(s) in the PPA have
completed building; this permits blocking on the builds to delay other
actions such as requesting users on a bug report to test the PPA, or
submitting a merge proposal for the update to be considered for
inclusion in the distro.

You can view a team's registered PPAs using 'ppa list'.


Usage
-----

Register a new PPA

```
$ ppa create my-ppa
PPA 'my-ppa' created for the following architectures:

   i386, amd64, armel, armhf, ppc64el, s390x, arm64, powerpc

The PPA can be viewed at:

   https://launchpad.net/~my-name/+archive/ubuntu/my-ppa

You can upload packages to this PPA using:

   dput ppa:my-name/my-ppa <source.changes>
```

Upload a package to the PPA

```
$ dput ppa:my-name/my-ppa some-package.changes
```

Wait until all packages in the PPA have finished building

```
$ ppa wait ppa:my-name/my-ppa
```

Set the public description for a PPA from a file

```
$ cat some-package/README | ppa desc ppa:my-name/my-ppa
```

Trigger autopkgtests for the package, and check results

```
$ ppa tests ppa:my-name/my-ppa
```

Delete the PPA

```
$ ppa destroy ppa:my-name/my-ppa
```

Auto-linked Autopkgtest Trigger URLS
------------------------------------

By default, `ppa tests` will display autopkgtest triggers as hyperlinked
text.  The hyperlinking feature is supported on many newer terminal
programs but as it's a relatively recent VTE function it may not yet be
available in the terminal you use.  The following terminal programs are
believed to support it:

  - iTerm2 3.1
  - DomTerm 1.0.2
  - hTerm 1.76
  - Terminology 1.3?
  - Gnome Terminal 3.26 (VTE 0.50)
  - Guake 3.2.1 (VTE 0.50)
  - TOXTerm 3.5.1 (VTE 0.50)
  - Tilix 3.26 (VTE 0.50)
  - Terminator 2.0

This is not a comprehensive list, and likely will lengthen swiftly.
Meanwhile, if you have a non-supporting browser, the --show-urls option
can be passed to `ppa tests` to make it display the raw URLs that can be
manually cut and pasted into your web browser.
