## Ardour Integration (macOS via MacPorts)

This document captures the exact state of our Ardour build attempt on macOS and provides step‑by‑step commands to reproduce and continue.

### Quick resume (current state)
- Platform: macOS (Apple Silicon arm64), MacPorts‑only PATH (no Homebrew), Xcode CLT present.
- Dependencies: Curated ports installed (toolchain, GTKmm3 stack, LV2 stack, audio libs, Boost 1.76 via MacPorts).
- Vamp SDK: Built and installed to `/opt/local` (`vamp-sdk.pc` and `vamp-hostsdk.pc`).
- Ardour source: Cloned; tag `8.9` checked out.
- Result: Build completed successfully using internal YTK.
- Key build inputs: SDKROOT pinned to macOS 14.x (e.g., `/Library/Developer/CommandLineTools/SDKs/MacOSX14.5.sdk`), `MACOSX_DEPLOYMENT_TARGET=11.0`, arm64, `--keepflags`, and alias/visibility defines.

To continue exactly where we left off, jump to "Continue here" below.

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

Additional libraries often required by Ardour (install up front to avoid configure loops):
```bash
sudo port -N install \
  fluidsynth hidapi libltc
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

### Build qm‑dsp (not in MacPorts)
```bash
mkdir -p "$HOME/Documents/Development/Audio"
cd "$HOME/Documents/Development/Audio"
git clone https://github.com/c4dm/qm-dsp.git
cd qm-dsp
make -f build/osx/Makefile.osx clean || true
make -f build/osx/Makefile.osx ARCHFLAGS="-mmacosx-version-min=11.0 -arch arm64" -j"$(sysctl -n hw.ncpu)"
# library will be at: $HOME/Documents/Development/Audio/qm-dsp/libqm-dsp.a
```

### Configure Ardour (CoreAudio, internal YTK)
Boost headers/libs live under `/opt/local/libexec/boost/1.76`. Use a clean environment, pin SDK and deployment target, keep flags, and add alias/visibility defines:
```bash
cd "$HOME/Documents/Development/Audio/ardour"
env -i \
  PATH="/opt/local/bin:/opt/local/sbin:/usr/bin:/bin:/usr/sbin:/sbin" \
  PKG_CONFIG_PATH="/opt/local/lib/pkgconfig:/opt/local/share/pkgconfig" \
  SDKROOT="/Library/Developer/CommandLineTools/SDKs/MacOSX14.5.sdk" \
  MACOSX_DEPLOYMENT_TARGET="11.0" \
  BOOST_ROOT="/opt/local/libexec/boost/1.76" \
  BOOST_INCLUDEDIR="/opt/local/libexec/boost/1.76/include" \
  BOOST_LIBRARYDIR="/opt/local/libexec/boost/1.76/lib" \
  CPPFLAGS="-I/opt/local/include -I/opt/local/libexec/boost/1.76/include" \
  LDFLAGS="-L/opt/local/lib -L/opt/local/libexec/boost/1.76/lib" \
  CFLAGS="-DNO_SYMBOL_RENAMING -DNO_SYMBOL_EXPORT -DDISABLE_VISIBILITY" \
  CXXFLAGS="-DNO_SYMBOL_RENAMING -DNO_SYMBOL_EXPORT -DDISABLE_VISIBILITY" \
  python3 ./waf configure --dist-target=apple --with-backends=coreaudio --arm64 --keepflags
```

At the time of writing, configure succeeds with:
- Boost (>= 1.68) via boost176
- GTKmm stack (glibmm, giomm, cairomm, pangomm, libpng, pango, cairo, gobject, gmodule)
- Audio libs (libsndfile, libsamplerate, rubberband 3.x, aubio >= 0.4, fftw3f)
- Metadata/IO (libarchive, libcurl, taglib, libusb)
- LV2 stack (lv2 1.18.4, lilv, serd, sord, sratom)
- Vamp (SDK + hostsdk) via source install
```

### Build
```bash
python3 ./waf -j"$(sysctl -n hw.ncpu)" --keepflags \
  CFLAGS="-DNO_SYMBOL_RENAMING -DNO_SYMBOL_EXPORT -DDISABLE_VISIBILITY" \
  CXXFLAGS="-DNO_SYMBOL_RENAMING -DNO_SYMBOL_EXPORT -DDISABLE_VISIBILITY"
```

Verification after configure:
- Summary shows: `Use YTK instead of GTK: True`.
- C/C++ compiler flags include the three defines above.
- Architecture: `Mac arm64 Architecture: True`.

Notes:
- `hidapi-hidraw` being "not found" is expected on macOS.
- If version parsing fails, check out a tag first, e.g., `git checkout 8.9`.
```

### Artifacts and launch
Artifacts will be placed under `build/`:
- GUI: `build/gtk2_ardour/ardour-8.9.0`
- Headless: `build/headless/hardour-8.9.0`

Run:
```bash
./build/gtk2_ardour/ardour-8.9.0
# or headless
./build/headless/hardour-8.9.0 --help
```

### Current focus / next step
- Integrate Ardour into the control plane: add OSC/Lua hooks to expose session state and route MIDI as we do today via IAC.

### Why Ardour
- Ardour provides OSC/Lua scripting, LV2, and robust state access not available in GarageBand. Source: `https://github.com/Ardour/ardour`.

### Integration plan back in this project
- Once Ardour launches, add a small OSC/LV2 bridge process to expose session state into the control plane, then route MIDI via IAC as we do today. This remains optional; core still works with GarageBand.

### Status snapshot
- MacPorts installed; curated dependencies present; Vamp SDK installed.
- Ardour: repo on tag `8.9`; configure shows YTK=True; SDKROOT pinned to 14.x; arm64 on; build finished successfully.


