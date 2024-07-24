# ArduinoIDE to PlatformIO Converter

This Python script automates the process of converting an Arduino IDE project to a PlatformIO project structure. It's designed to simplify the transition from Arduino's traditional setup to PlatformIO's more organized and powerful environment.

## Features

- Converts Arduino (.ino) files to C++ (.cpp) files
- Creates appropriate header (.h) files for each source file
- Extracts and centralizes all #define statements into a single `allDefines.h` file
- Identifies and properly handles global variables
- Generates function prototypes in header files
- Preserves existing code structure and comments
- Copies the project's data folder (if it exists) to the PlatformIO structure
- Creates a basic `platformio.ini` file for PlatformIO configuration

## How It Works

1. **Project Structure Creation**: 
   - Creates a PlatformIO folder structure with `src` and `include` directories

2. **File Conversion**:
   - Converts `.ino` files to `.cpp` files
   - Creates corresponding `.h` files for each `.cpp` file

3. **Define Handling**:
   - Extracts all non-function-like #define statements
   - Places them in a centralized `allDefines.h` file
   - Comments out original #define statements in source files

4. **Global Variable Management**:
   - Identifies global variables
   - Adds appropriate `extern` declarations to header files

5. **Function Prototype Generation**:
   - Extracts function declarations
   - Adds them to the corresponding header files

6. **Main Project File Handling**:
   - Specially processes the main project file (originally .ino, converted to .cpp)
   - Ensures all necessary includes and declarations are present

7. **Data Folder Handling**:
   - Copies the `data` folder from the Arduino project to the PlatformIO structure (if it exists)

8. **PlatformIO Configuration**:
   - Generates a basic `platformio.ini` file with common settings

## Usage

1. Ensure you have Python installed on your system
2. Place the script in a directory accessible to your Arduino project
3. Run the script with the following command:
```
python arduinoIDE2platformIO.py --project_dir /path/to/your/arduino/project
```
  or `cd` to the directory where the Arduino.ino files are located and run the following command:
```
cd /path/to/your/arduino/project
python arduinoIDE2platformIO.py 
```
5. The script will create a new `PlatformIO` folder in your project directory with the converted project structure

## Notes

- Always backup your project before running this converter
- Review the generated files to ensure everything was converted correctly
- You may need to make minor adjustments to the code or PlatformIO configuration based on your specific project requirements

## Contributing

Contributions to improve the converter are welcome. Please feel free to submit issues or pull requests on the GitHub repository.

## License

[Specify your license here, e.g., MIT License, GPL, etc.]
