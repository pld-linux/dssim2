# TODO: build without network (crates downloading)
Summary:	Tool to compute (dis)similarity between two or more images
Summary(pl.UTF-8):	Narzędzie do obliczania (nie)podobieństwa dwóch lub większej liczby obrazów
Name:		dssim2
Version:	2.9.4
Release:	1
License:	AGPL v3+ or commercial
Group:		Applications/Graphics
#Source0Download: https://github.com/pornel/dssim/releases
Source0:	https://github.com/pornel/dssim/archive/%{version}/dssim-%{version}.tar.gz
# Source0-md5:	54394c0c4e145434aec6c2f683b1e120
URL:		https://kornel.ski/dssim
BuildRequires:	cargo
BuildRequires:	rust
Obsoletes:	dssim < 2
ExclusiveArch:	%{x8664} %{ix86}
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
%setup -q -n dssim-%{version}

%build
cargo build -v --release

%install
rm -rf $RPM_BUILD_ROOT

cargo install --root $RPM_BUILD_ROOT%{_prefix}

%{__rm} $RPM_BUILD_ROOT%{_prefix}/.crates.toml

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.md
%attr(755,root,root) %{_bindir}/dssim
