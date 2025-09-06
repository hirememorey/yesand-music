## Ardour Integration (macOS via MacPorts)

This document captures the exact state of our Ardour build attempt on macOS and provides step‑by‑step commands to reproduce and continue.

### Goal
- Build Ardour from source on macOS and integrate it as the DAW target for live MIDI from this project (alternative to GarageBand), with deep state access via LV2/OSC/scriptable APIs.

### Prerequisites
- macOS 15.6.1 (Sequoia) tested.
- Xcode Command Line Tools installed:
  ```bash
  xcode-select -p
  ```

### Install MacPorts (from source)
If you already have MacPorts, skip to Dependencies.
```bash
curl -fsSLO https://distfiles.macports.org/MacPorts/MacPorts-2.9.3.tar.bz2
tar xjf MacPorts-2.9.3.tar.bz2
cd MacPorts-2.9.3
./configure --prefix=/opt/local --with-applications-dir=/Applications/MacPorts --with-install-user="$USER" --with-install-group="staff"
make -j"$(sysctl -n hw.ncpu)"
sudo make install
echo 'export PATH="/opt/local/bin:/opt/local/sbin:$PATH"' >> ~/.zshrc
export PATH="/opt/local/bin:/opt/local/sbin:$PATH"
sudo port -v selfupdate
```

### Install build toolchain and libraries
```bash
sudo port -N install \
  pkgconfig git wget cmake ninja python311 py311-pip

# GTKmm stack and core libs
sudo port -N install \
  gtkmm3 glibmm pangomm cairomm libsigcxx2 \
  libsndfile libogg libvorbis curl libarchive libsamplerate \
  liblo fftw-3-single libusb taglib lv2 lilv serd sord sratom \
  rubberband aubio

# Boost (MacPorts keeps headers/libs under a versioned prefix)
sudo port -N install boost176
```

### Clone Ardour
```bash
mkdir -p "$HOME/Documents/Development/Audio"
cd "$HOME/Documents/Development/Audio"
git clone https://github.com/Ardour/ardour.git
cd ardour

# Fetch tags to enable waf version detection
git fetch --unshallow --tags || git fetch --tags --depth=1000
```

### Install Vamp Plugin SDK (not provided by MacPorts)
```bash
cd /tmp
git clone https://github.com/vamp-plugins/vamp-plugin-sdk.git
cmake -S vamp-plugin-sdk -B vamp-plugin-sdk/build -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=/opt/local
cmake --build vamp-plugin-sdk/build -j"$(sysctl -n hw.ncpu)"
sudo cmake --install vamp-plugin-sdk/build
# verify
env PKG_CONFIG_PATH="/opt/local/lib/pkgconfig:/opt/local/share/pkgconfig" pkg-config --modversion vamp-sdk
```

### Configure Ardour (CoreAudio)
Boost headers/libs live under `/opt/local/libexec/boost/1.76`. Point waf to them, and to MacPorts pkg-config paths:
```bash
cd "$HOME/Documents/Development/Audio/ardour"
env \
  BOOST_ROOT="/opt/local/libexec/boost/1.76" \
  BOOST_INCLUDEDIR="/opt/local/libexec/boost/1.76/include" \
  BOOST_LIBRARYDIR="/opt/local/libexec/boost/1.76/lib" \
  PKG_CONFIG_PATH="/opt/local/lib/pkgconfig:/opt/local/share/pkgconfig" \
  CPPFLAGS="-I/opt/local/include -I/opt/local/libexec/boost/1.76/include" \
  LDFLAGS="-L/opt/local/lib -L/opt/local/libexec/boost/1.76/lib" \
  ./waf configure --dist-target=apple --with-backends=coreaudio --noconfirm
```

At the time of writing, configure succeeds with:
- Boost (>= 1.68) via boost176
- GTKmm stack (glibmm, giomm, cairomm, pangomm, libpng, pango, cairo, gobject, gmodule)
- Audio libs (libsndfile, libsamplerate, rubberband 3.x, aubio >= 0.4, fftw3f)
- Metadata/IO (libarchive, libcurl, taglib, libusb)
- LV2 stack (lv2 1.18.4, lilv, serd, sord, sratom)
- Vamp (SDK + hostsdk) via source install

### Build
```bash
./waf -j"$(sysctl -n hw.ncpu)"
```

### Current blocker (macOS-specific)
The build fails within Ardour's internal `libs/tk/ydk` due to GCC symbol alias attributes not supported by Darwin/clang, e.g.:
```
.../libs/tk/ydk/gdkaliasdef.c:XXXX: error: aliases are not supported on darwin
```

#### Next steps to try
- Prefer external system GTK stack entirely (avoid internal `ydk`):
  ```bash
  ./waf distclean
  env BOOST_ROOT=... PKG_CONFIG_PATH=... ./waf configure --dist-target=apple --with-backends=coreaudio --use-external-libs --noconfirm
  ./waf -j"$(sysctl -n hw.ncpu)"
  ```
- If alias errors persist, patch out `#include "gdkaliasdef.c"` on macOS in `libs/tk/ydk/*` (guard with `#ifndef __APPLE__`), or adjust compiler flags to disable alias sections for Darwin. Keep the edit scoped to the `ydk` layer.
- Alternatively, build Ardour on Linux (or use the official macOS binary) while continuing integration via IAC/CoreMIDI on macOS.

### Why Ardour
- Ardour provides OSC/Lua scripting, LV2, and robust state access not available in GarageBand. Source: `https://github.com/Ardour/ardour`.

### Integration plan back in this project
- Once Ardour launches, add a small OSC/LV2 bridge process to expose session state into the control plane, then route MIDI via IAC as we do today. This remains optional; core still works with GarageBand.

### Status snapshot
- MacPorts installed, toolchain and dependencies present.
- Ardour configure: success (CoreAudio target).
- Ardour build: blocked by `gdkaliasdef.c` Darwin alias errors in `libs/tk/ydk`.


