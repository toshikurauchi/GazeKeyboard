# Qt Keyboard Visualizer (with EyeTribe remote eye tracker)

This application shows the keyboard image with the current gaze position over it.

## Requirements

To run this visualizer you will need to install the EyeTribe SDK and boost library (there are prebuilt binaries for Windows).

## Environment setup

Set following environment variables: `BOOST_DIR` and `BOOST_LIB`. `BOOST_DIR` should point to the root directory containing the boost installation (using the prebuild binaries for Windows the default location would look something like `C:\local\boost_1_57_0`). `BOOST_LIB` should point to the directory containing the library files (again, on Windows the default location will be something like `C:\local\boost_1_57_0\lib32-msvc-10.0`.
