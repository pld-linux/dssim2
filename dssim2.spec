#
# Conditional build:
%bcond_without	aom	# AVIF support via AOM
%bcond_without	webp	# WEBP support

Summary:	Tool to compute (dis)similarity between two or more images
Summary(pl.UTF-8):	Narzędzie do obliczania (nie)podobieństwa dwóch lub większej liczby obrazów
Name:		dssim2
Version:	3.2.3
Release:	1
License:	AGPL v3+ or commercial
Group:		Applications/Graphics
#Source0Download: https://github.com/pornel/dssim/releases
Source0:	https://github.com/pornel/dssim/archive/%{version}/dssim-%{version}.tar.gz
# Source0-md5:	4226a24d7728b77cfb490b03831d7f07
# cd dssim-%{version}
# cargo vendor
# cd ..
# tar cJf dssim-vendor-%{version}.tar.xz dssim-%{version}/{vendor,Cargo.lock}
Source1:	dssim-vendor-%{version}.tar.xz
# Source1-md5:	02c25d610a0644876e4588daa6a42b85
URL:		https://kornel.ski/dssim
%{?with_aom:BuildRequires:	aom-devel >= 3.3.0}
BuildRequires:	cargo
BuildRequires:	lcms2-devel >= 2.13.1
%{?with_webp:BuildRequires:	libwebp-devel}
%ifarch %{ix86} %{x8664} x32
BuildRequires:	nasm
%endif
BuildRequires:	rpmbuild(macros) >= 2.004
BuildRequires:	rust
BuildRequires:	sed >= 4.0
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
%{?with_aom:Requires:	aom >= 3.3.0}
Requires:	lcms2 >= 2.13.1
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

# shared aom (also fixes x32 build, builtin aom linking fails)
%{__sed} -i -e 's/cargo:rustc-link-lib=static=aom/cargo:rustc-link-lib=aom/' vendor/libaom-sys/build.rs
%{__sed} -i -e 's/"build.rs":"e20f251c0f9cbe97b298d4575259f9583633fb9526c61c52cc9abe5a94769284"/"build.rs":"b9ce3f79373bed7310a8da968620b3d97f907fd54e266a7f38f5f4090a007ea9"/' vendor/libaom-sys/.cargo-checksum.json

# shared lcms2
%{__sed} -i -e '/^load_image = / s/, features = \["lcms2-static"\]//' Cargo.toml

%build
export CARGO_HOME="$(pwd)/.cargo"
export LIB_AOM_INCLUDE_PATH=%{_includedir}
export LIB_AOM_PKG_CONFIG_PATH=%{_pkgconfigdir}
export LIB_AOM_STATIC_LIB_PATH=%{_libdir}

%cargo_build --frozen \
	--features "%{?with_aom:avif} %{?with_webp:webp}"

%install
rm -rf $RPM_BUILD_ROOT

export CARGO_HOME="$(pwd)/.cargo"
export LIB_AOM_INCLUDE_PATH=%{_includedir}
export LIB_AOM_PKG_CONFIG_PATH=%{_pkgconfigdir}
export LIB_AOM_STATIC_LIB_PATH=%{_libdir}

%cargo_install --frozen \
	--features "%{?with_aom:avif} %{?with_webp:webp}" \
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
