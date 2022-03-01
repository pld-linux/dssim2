Summary:	Tool to compute (dis)similarity between two or more images
Summary(pl.UTF-8):	Narzędzie do obliczania (nie)podobieństwa dwóch lub większej liczby obrazów
Name:		dssim2
Version:	3.2.0
Release:	1
License:	AGPL v3+ or commercial
Group:		Applications/Graphics
#Source0Download: https://github.com/pornel/dssim/releases
Source0:	https://github.com/pornel/dssim/archive/%{version}/dssim-%{version}.tar.gz
# Source0-md5:	64e777cdd859a9a556526a2ec69aef9b
# cd dssim-%{version}
# cargo vendor
# cd ..
# tar cJf dssim-vendor-%{version}.tar.xz dssim-%{version}/{vendor,Cargo.lock}
Source1:	dssim-vendor-%{version}.tar.xz
# Source1-md5:	96943aeffac9afe4f4ab4198d04f3e0b
URL:		https://kornel.ski/dssim
BuildRequires:	cargo
%ifarch %{ix86} %{x8664} x32
BuildRequires:	nasm
%endif
BuildRequires:	rpmbuild(macros) >= 2.004
BuildRequires:	rust
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Obsoletes:	dssim < 2
ExclusiveArch:	%{x8664} %{ix86} x32 aarch64 armv6hl armv7hl armv7hnl
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This tool computes (dis)similarity between two or more PNG images
using an algorithm approximating human vision.

Comparison is done using the SSIM algorithm at multiple weighed
resolutions.

%description -l pl.UTF-8
To narzędzie oblicza (nie)podobieństwo dwóch lub większej liczby
obrazów PNG przy użyciu algorytmu przybliżającego ludzkie widzenie.

Porównywanie jest wykonywane algorytmem SSIM z wieloma ważonymi
rozdzielczościami.

%prep
%setup -q -n dssim-%{version} -b1

# use our offline registry
export CARGO_HOME="$(pwd)/.cargo"

mkdir -p "$CARGO_HOME"
cat >.cargo/config <<EOF
[source.crates-io]
registry = 'https://github.com/rust-lang/crates.io-index'
replace-with = 'vendored-sources'

[source.vendored-sources]
directory = '$PWD/vendor'
EOF

%build
export CARGO_HOME="$(pwd)/.cargo"

%cargo_build --frozen

%install
rm -rf $RPM_BUILD_ROOT

export CARGO_HOME="$(pwd)/.cargo"

%cargo_install --frozen \
	--path . \
	--root $RPM_BUILD_ROOT%{_prefix}

%{__rm} $RPM_BUILD_ROOT%{_prefix}/.crates.toml
%{__rm} $RPM_BUILD_ROOT%{_prefix}/.crates2.json

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.md
%attr(755,root,root) %{_bindir}/dssim
