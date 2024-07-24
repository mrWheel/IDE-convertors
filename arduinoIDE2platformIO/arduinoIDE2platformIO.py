#------------------------------------------------------------
#
#   convert a ArduinoIDE project to a PlatformIO project
#
#   by Willem Aandewiel
#
#   Version 0.4 (24-07-2024)
#
#------------------------------------------------------------
import os
import sys
import shutil
import re
import argparse
import logging
import traceback
from datetime import datetime

global_extern_declarations = set()


#------------------------------------------------------------------------------------------------------
def setup_logging():
    """Set up logging configuration."""
    #logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')

#------------------------------------------------------------------------------------------------------
def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Convert Arduino project to PlatformIO structure.")
    parser.add_argument("--project_dir", default=os.getcwd(), help="Path to the project directory")
    parser.add_argument("--backup", action="store_true", help="Create a backup of original files")
    return parser.parse_args()

#------------------------------------------------------------------------------------------------------
def backup_project(project_folder):
    """Create a backup of the project folder."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_folder = f"{project_folder}_backup_{timestamp}"
    shutil.copytree(project_folder, backup_folder)
    logging.info(f"Project backup created at: {backup_folder}")

#------------------------------------------------------------------------------------------------------
def get_project_info(project_dir):
    """
    Get project folder, name, and PlatformIO-related paths.

    Returns:
        tuple: Contains project_folder, project_name, pio_folder, pio_src, pio_include
    """
    project_folder = os.path.abspath(project_dir)
    project_name = os.path.basename(project_folder)
    pio_folder = os.path.join(project_folder, "PlatformIO")
    pio_src = os.path.join(pio_folder, "src")
    pio_include = os.path.join(pio_folder, "include")
    return project_folder, project_name, pio_folder, pio_src, pio_include

#------------------------------------------------------------------------------------------------------
def recreate_pio_folders(pio_src, pio_include):
    """Remove and recreate PlatformIO src and include folders."""
    for folder in [pio_src, pio_include]:
        if os.path.exists(folder):
            shutil.rmtree(folder)
        os.makedirs(folder)
    logging.info("PlatformIO folders recreated")

#------------------------------------------------------------------------------------------------------
def create_platformio_ini(pio_folder):
    """Create a platformio.ini file if it doesn't exist."""
    platformio_ini_path = os.path.join(pio_folder, 'platformio.ini')
    if not os.path.exists(platformio_ini_path):
        platformio_ini_content = """
; PlatformIO Project Configuration File
;
;   Build options: build flags, source filter
;   Upload options: custom upload port, speed and extra flags
;   Library options: dependencies, extra library storages
;   Advanced options: extra scripting
;
; Please visit documentation for the other options and examples
; https://docs.platformio.org/page/projectconf.html

[platformio]
workspace_dir = .pio.nosync
default_envs = myBoard

[env:myBoard]
platform = <select platform with "PIO Home" -> Platforms>
board = <select board with "PIO Home" -> Boards>
framework = arduino
board_build.filesystem = <if appropriate>
monitor_speed = 115200
upload_speed = 115200
upload_port = <select port like "/dev/cu.usbserial-3224144">
build_flags =
\t-D DEBUG

lib_ldf_mode = deep+

lib_deps =
\t<select libraries with "PIO Home" -> Libraries

monitor_filters =
  esp8266_exception_decoder
"""
        with open(platformio_ini_path, 'w') as f:
            f.write(platformio_ini_content)
        logging.info(f"Created platformio.ini file at {platformio_ini_path}")
    else:
        logging.info(f"platformio.ini file already exists at {platformio_ini_path}")


#------------------------------------------------------------------------------------------------------
def remove_comments(content):
    """Remove C and C++ style comments from the content."""
    def replacer(match):
        s = match.group(0)
        if s.startswith('/'):
            return " "  # note: a space and not an empty string
        else:
            return s
    pattern = re.compile(
        r'//.*?$|/\*.*?\*/|\'(?:\\.|[^\\\'])*\'|"(?:\\.|[^\\"])*"',
        re.DOTALL | re.MULTILINE
    )
    return re.sub(pattern, replacer, content)

#------------------------------------------------------------------------------------------------------
def remove_comments_preserve_strings(content):
    """Remove C and C++ style comments from the content while preserving string literals."""
    def replacer(match):
        s = match.group(0)
        if s.startswith('/'):
            return " "
        else:
            return s
    pattern = re.compile(
        r'//.*?$|/\*.*?\*/|("(?:\\.|[^"\\])*")|\'(?:\\.|[^\\\'])*\'',
        re.DOTALL | re.MULTILINE
    )
    return re.sub(pattern, replacer, content)

#------------------------------------------------------------------------------------------------------
def extract_and_comment_defines(pio_folder, pio_include):
    """
    Extract non-function-like #define statements from .h and .ino files,
    create allDefines.h, and comment original statements with info.
    """
    all_defines = []
    define_pattern = r'^\s*#define\s+(\w+)(?:\s+(.+))?$'

    logging.info(f"Searching for #define statements in {pio_folder}")

    for root, _, files in os.walk(pio_folder):
        for file in files:
            if file.endswith(('.h', '.ino', '.cpp')):
                file_path = os.path.join(root, file)
                logging.debug(f"Processing file: {file_path}")
                try:
                    with open(file_path, 'r') as f:
                        content = f.readlines()

                    new_content = []
                    for line in content:
                        match = re.match(define_pattern, line)
                        if match:
                            macro_name = match.group(1)
                            macro_value = match.group(2) if match.group(2) else ""

                            # Check if it's not a function-like macro and not a header guard
                            if not macro_value.strip().startswith('(') and not macro_name.endswith('_H'):
                                all_defines.append((macro_name, macro_value.strip()))
                                # Comment out the original #define with info
                                new_content.append(f"//-- moved to allDefines.h // {line}")
                                logging.debug(f"Added non-function-like #define: {macro_name}")
                            else:
                                new_content.append(line)
                        else:
                            new_content.append(line)

                    # Write the modified content back to the file
                    with open(file_path, 'w') as f:
                        f.writelines(new_content)
                    logging.debug(f"Updated {file} with commented out #defines")

                except Exception as e:
                    logging.error(f"Error processing file {file}: {str(e)}")

    # Create allDefines.h with non-function-like macros
    all_defines_path = os.path.join(pio_include, 'allDefines.h')
    logging.info(f"Creating allDefines.h with {len(all_defines)} macros")
    try:
        with open(all_defines_path, 'w') as f:
            f.write("#ifndef ALLDEFINES_H\n#define ALLDEFINES_H\n\n")
            for macro_name, macro_value in all_defines:
                if macro_value:
                    f.write(f"#define {macro_name} {macro_value}\n")
                else:
                    f.write(f"#define {macro_name}\n")
            f.write("\n#endif // ALLDEFINES_H\n")
        logging.info(f"Successfully created {all_defines_path}")
    except Exception as e:
        logging.error(f"Error creating allDefines.h: {str(e)}")

    logging.info(f"Extracted {len(all_defines)} non-function-like #define statements")


#------------------------------------------------------------------------------------------------------
def create_header_file(header_path, base_name):
    """Create a new header file with basic structure."""
    with open(header_path, 'w') as f:
        f.write(f"#ifndef {base_name.upper()}_H\n")
        f.write(f"#define {base_name.upper()}_H\n\n")
        f.write("#include <Arduino.h>\n")
        f.write("#include \"allDefines.h\"\n\n")
        f.write("//== Extern Variables ==")
        f.write("\n\n")
        f.write("//== Function Prototypes ==")
        f.write("\n\n")
        f.write(f"#endif // {base_name.upper()}_H\n")
    logging.info(f"Created new header file: {header_path}")

#------------------------------------------------------------------------------------------------------
def create_header_files(pio_src, pio_include, project_name):
    for file in os.listdir(pio_src):
        if file.endswith('.ino') and file != f"{project_name}.ino":
            base_name = os.path.splitext(file)[0]
            header_path = os.path.join(pio_include, f"{base_name}.h")
            process_header_file(header_path, base_name)

    logging.info("Processed regular header files")

#------------------------------------------------------------------------------------------------------
def fix_main_header_file(header_path, project_name):
    with open(header_path, 'r') as f:
        content = f.read()

    logging.info(f"1111\n{content}\n1111")
    # Remove existing header guards if present
    content = re.sub(r'#ifndef.*?_H\s*#define.*?_H', '', content, flags=re.DOTALL)
    content = re.sub(r'#endif.*?_H', '', content, flags=re.DOTALL)
    logging.info(f"2222\n{content}\n2222")

    # Ensure includes are at the top
    includes = re.findall(r'#include.*', content, re.MULTILINE)
    content_without_includes = re.sub(r'#include.*\n', '', content, flags=re.MULTILINE)

    # Reconstruct the file
    new_content = '\n'.join(includes) + '\n\n' if includes else ''
    new_content += content_without_includes.strip() + '\n'

    # Add header guards
    final_content = f"#ifndef {project_name.upper()}_H\n"
    final_content += f"#define {project_name.upper()}_H\n\n"
    final_content += new_content
    final_content += f"\n#endif // {project_name.upper()}_H\n"

    logging.info(f"3333\n{final_content}\n3333")

    with open(header_path, 'w') as f:
        f.write(final_content)

    logging.info(f"Fixed main header file: {header_path}")
    logging.info(f"CORRECT\n{final_content}\nCORRECT")

#------------------------------------------------------------------------------------------------------
def process_header_file(header_path, base_name, is_main_header=False):
    if os.path.exists(header_path):
        with open(header_path, 'r') as f:
            content = f.read()
    else:
        content = f"#ifndef {base_name.upper()}_H\n#define {base_name.upper()}_H\n\n#include <Arduino.h>\n#include \"allDefines.h\"\n\n#endif // {base_name.upper()}_H\n"

    if is_main_header:
        # For the main header, completely restructure the file
        includes = re.findall(r'#include.*', content, re.MULTILINE)
        externs = re.findall(r'extern.*?;', content, re.DOTALL)
        prototypes = re.findall(r'^\w+[\s\*]+\w+\s*\([^)]*\);', content, re.MULTILINE)

        new_content = f"#ifndef {base_name.upper()}_H\n#define {base_name.upper()}_H\n\n"
        new_content += '\n'.join(includes) + '\n\n'

        if externs:
            new_content += "//== Extern Variables ==\n" + '\n'.join(externs) + '\n\n'

        if prototypes:
            new_content += "//== Function Prototypes ==\n" + '\n'.join(prototypes) + '\n\n'

        new_content += f"#endif // {base_name.upper()}_H\n"

        with open(header_path, 'w') as f:
            f.write(new_content)
    else:
        # For other header files, just ensure the guards are present
        if "#ifndef" not in content:
            new_content = f"#ifndef {base_name.upper()}_H\n#define {base_name.upper()}_H\n\n"
            new_content += content
            if "#endif" not in content:
                new_content += f"\n#endif // {base_name.upper()}_H\n"

            with open(header_path, 'w') as f:
                f.write(new_content)

    logging.info(f"Processed header file: {header_path}")

#------------------------------------------------------------------------------------------------------
def copy_project_files(project_folder, pio_src, pio_include):
    """Copy .ino files to pio_src and .h files to pio_include."""
    for file in os.listdir(project_folder):
        if file.endswith('.ino'):
            shutil.copy2(os.path.join(project_folder, file), pio_src)
        elif file.endswith('.h'):
            shutil.copy2(os.path.join(project_folder, file), pio_include)
    logging.info("Copied project files to PlatformIO folders")


#------------------------------------------------------------------------------------------------------
def extract_global_vars(pio_src, pio_include, project_name):
    """
    Extract global variable definitions from .ino files and the main project header file.
    Only variables declared outside of all function blocks and not in function parameters are considered global.
    """
    global_vars = {}

    # Comprehensive list of object types, including String
    types = r'(?:uint8_t|int8_t|uint16_t|int16_t|uint32_t|int32_t|uint64_t|int64_t|char|int|float|double|bool|long|short|unsigned|signed|size_t|void|String)'

    var_pattern = rf'^\s*((?:static|volatile|const)?\s*{types}(?:\s*\*)*)\s+((?:\w+(?:\[.*?\])?(?:\s*=\s*[^,;]+)?\s*,\s*)*\w+(?:\[.*?\])?(?:\s*=\s*[^,;]+)?)\s*;'
    func_pattern = rf'^\s*(?:static|volatile|const)?\s*(?:{types})(?:\s*\*)*\s+(\w+)\s*\((.*?)\)'

    keywords = set(['if', 'else', 'for', 'while', 'do', 'switch', 'case', 'default',
                    'break', 'continue', 'return', 'goto', 'typedef', 'struct', 'enum',
                    'union', 'sizeof', 'volatile', 'register', 'extern', 'inline'])

    files_to_process = [f for f in os.listdir(pio_src) if f.endswith('.ino')]
    main_ino = f"{project_name}.ino"
    if main_ino not in files_to_process and os.path.exists(os.path.join(pio_src, main_ino)):
        files_to_process.append(main_ino)

    # Add the main project header file
    main_header = f"{project_name}.h"
    main_header_path = os.path.join(pio_include, main_header)
    if os.path.exists(main_header_path):
        files_to_process.append(main_header)

    for file in files_to_process:
        if file.endswith('.ino'):
            file_path = os.path.join(pio_src, file)
        else:  # It's the main header file
            file_path = main_header_path

        logging.info(f"Processing file for global variables: {file_path}")
        try:
            with open(file_path, 'r') as f:
                content = f.read()

            # Remove comments while preserving string literals
            content = remove_comments_preserve_strings(content)

            lines = content.split('\n')

            brace_level = 0
            in_function = False
            file_vars = []

            for line in lines:
                stripped_line = line.strip()

                # Check for function start
                if re.search(func_pattern, stripped_line) and not in_function:
                    in_function = True

                # Count braces
                brace_level += stripped_line.count('{') - stripped_line.count('}')

                # Check for function end
                if brace_level == 0:
                    in_function = False

                # Check for variable variables only at global scope
                if not in_function and brace_level == 0:
                    match = re.search(var_pattern, stripped_line)
                    if match:
                        var_type = match.group(1).strip()
                        var_declarations = match.group(2).split(',')
                        for var_decl in var_declarations:
                            var_name = var_decl.strip().split('=')[0].strip()  # Remove any initialization
                            base_name = var_name.split('[')[0].strip()
                            if base_name not in keywords:
                                file_vars.append((var_type, var_name))
                                logging.debug(f"Found global variable in {file}: {var_type} {var_name}")

            global_vars[file] = file_vars
            logging.info(f"Processed {file} successfully. Found {len(file_vars)} global variables.")

        except Exception as e:
            logging.error(f"Error processing file {file}: {str(e)}")
            logging.error(traceback.format_exc())

    logging.info("Extracted all global variables")
    return global_vars

#------------------------------------------------------------------------------------------------------
def create_extern_declaration(var_type, var_name):
    """Create an extern declaration for a global variable."""
    var_name = var_name.split('=')[0].strip()  # Remove any initialization

    if '[' in var_name:
        var_name = var_name.split('[')[0] + '[]'  # Keep array notation but remove size

    var_type = var_type.replace('static', '').strip()  # Remove 'static' if present

    return f"extern {var_type} {var_name};"

#------------------------------------------------------------------------------------------------------
def update_header_with_externs(header_path, global_vars, used_vars, current_file):
    """Update header file with extern variables for used global variables."""
    global global_extern_declarations

    logging.debug(f"Updating header {header_path} with externs")
    logging.debug(f"Global vars: {global_vars}")
    logging.debug(f"Used vars: {used_vars}")

    with open(header_path, 'r+') as f:
        content = f.read()
        insert_pos = content.find("//== Extern Variables ==")
        #logging.info(f"insert_pos [{insert_pos}]")
        if insert_pos == -1:
            logging.warning(f"Could not find Extern Variables marker in {header_path}")
            return
        insert_pos += len("//== Extern Variables ==\n")

        new_extern_declarations = set()

        all_globals = [var for file, vars in global_vars.items() if file != current_file for var in vars]
        logging.debug(f"All globals: {all_globals}")

        for var_type, var_name in all_globals:
            base_name = var_name.split('[')[0].split('=')[0].strip()
            logging.debug(f"Checking var: {base_name}")
            if base_name in used_vars:
                extern_decl = create_extern_declaration(var_type, var_name)
                logging.debug(f"Created extern declaration: {extern_decl}")
                if extern_decl not in global_extern_declarations:
                    new_extern_declarations.add(extern_decl)
                    global_extern_declarations.add(extern_decl)

        if new_extern_declarations:
            new_content = (content[:insert_pos] +
                           '\n'.join(sorted(new_extern_declarations)) + '\n\n' +
                           content[insert_pos:])
            f.seek(0)
            f.write(new_content)
            f.truncate()
            logging.info(f"Added {len(new_extern_declarations)} extern variables to {header_path}")
        else:
            logging.info(f"No new extern variables added to {header_path}")

#------------------------------------------------------------------------------------------------------
def extract_prototypes(content):
    """Extract function prototypes from the given content."""
    # Remove comments
    content = remove_comments(content)

    # Comprehensive list of object types, including String
    types = r'(?:uint8_t|int8_t|uint16_t|int16_t|uint32_t|int32_t|uint64_t|int64_t|char|int|float|double|bool|long|short|unsigned|signed|size_t|void|String)'

    func_def_pattern = rf'\b(?:static|volatile|const)?\s*({types})(?:\s*\*)?\s+(\w+)\s*\([^)]*\)\s*{{'

    func_defs = re.finditer(func_def_pattern, content, re.MULTILINE)

    prototypes = []
    for match in func_defs:
        full_match = match.group(0)
        return_type = match.group(1)
        func_name = match.group(2)
        prototype = full_match[:-1].strip() + ";"
        prototypes.append(prototype)
        logging.debug(f"Found function: {return_type} {func_name}")

    return prototypes


#------------------------------------------------------------------------------------------------------
def update_header_with_prototypes(header_path, prototypes):
    """Update header file with function prototypes."""
    with open(header_path, 'r+') as f:
        content = f.read()
        insert_pos = content.find("//== Function Prototypes ==") + len("//== Function Prototypes ==\n")
        new_prototypes = []
        for proto in prototypes:
            if proto not in content:
                new_prototypes.append(proto)
                logging.debug(f"Adding Prototype to {header_path}: {proto}")

        if new_prototypes:
            new_content = (content[:insert_pos] +
                           '\n'.join(new_prototypes) + '\n\n' +
                           content[insert_pos:])
            f.seek(0)
            f.write(new_content)
            f.truncate()
    logging.info(f"Updated header {header_path} with {len(new_prototypes)} new Function Prototypes")

#------------------------------------------------------------------------------------------------------
def process_ino_files(pio_src, pio_include, project_name, global_vars):
    global global_extern_declarations
    global_extern_declarations = set()  # Reset global extern declarations

    logging.debug(f"Global vars at start of process_ino_files: {global_vars}")

    main_ino = f"{project_name}.ino"
    main_ino_path = os.path.join(pio_src, main_ino)

    files_to_process = [f for f in os.listdir(pio_src) if f.endswith('.ino')]
    if main_ino not in files_to_process and os.path.exists(main_ino_path):
        files_to_process.append(main_ino)

    for file in files_to_process:
        base_name = os.path.splitext(file)[0]
        header_path = os.path.join(pio_include, f"{base_name}.h")
        source_path = os.path.join(pio_src, file)

        logging.info(f"Processing file: {source_path}, header_path {header_path}")

        # Create the header file if it doesn't exist
        #--aaw- if not os.path.exists(header_path):
        create_header_file(header_path, base_name)

        with open(source_path, 'r') as f:
            content = f.read()

        content_no_comments = remove_comments_preserve_strings(content)

        used_vars = set(re.findall(r'\b(\w+)\b', content_no_comments))
        logging.debug(f"Used vars in {file}: {used_vars}")

        update_header_with_externs(header_path, global_vars, used_vars, file)

        prototypes = extract_prototypes(content_no_comments)
        logging.info(f"Found {len(prototypes)} prototypes in {file}")

        update_header_with_prototypes(header_path, prototypes)

        if file != main_ino:
            with open(source_path, 'r+') as f:
                content = f.read()
                f.seek(0, 0)
                f.write(f'#include "{base_name}.h"\n' + content)

            os.rename(source_path, os.path.join(pio_src, f"{base_name}.cpp"))
        else:
            # For the main project file, just rename it to .cpp
            os.rename(source_path, os.path.join(pio_src, f"{project_name}.cpp"))

    logging.info("Processed .ino files: renamed, updated headers, and converted to .cpp")

#------------------------------------------------------------------------------------------------------
def update_project_header(pio_include, project_name):
    """Update project header file with includes for all created headers."""
    project_header_path = os.path.join(pio_include, f"{project_name}.h")
    with open(project_header_path, 'r+') as f:
        content = f.read()
        f.seek(0, 0)
        for file in os.listdir(pio_include):
            if file.endswith('.h') and file != f"{project_name}.h":
                include_statement = f'#include "{file}"\n'
                if include_statement not in content:
                    f.write(include_statement)
        f.write(content)
    logging.info(f"Updated project header {project_name}.h with includes")

#------------------------------------------------------------------------------------------------------
def print_global_vars(global_vars):
    """Print the dictionary of global variables."""
    print("Global Variables:")
    for file, vars in global_vars.items():
        print(f"In file {file}:")
        for var_type, var_name in vars:
            print(f"  {var_type} {var_name}")


#------------------------------------------------------------------------------------------------------
def parse_arguments():
    parser = argparse.ArgumentParser(description="Convert Arduino project to PlatformIO structure.")
    parser.add_argument("--project_dir", default=os.getcwd(), help="Path to the project directory")
    parser.add_argument("--backup", action="store_true", help="Create a backup of original files")
    parser.add_argument("--debug", action="store_true", help="Enable debug logging")
    return parser.parse_args()


#------------------------------------------------------------------------------------------------------
def setup_logging(debug=False):
    level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(levelname)s - %(filename)s:%(lineno)d - %(message)s'
    )

#------------------------------------------------------------------------------------------------------
def main():
    setup_logging()
    args = parse_arguments()

    if args.backup:
        backup_project(args.project_dir)

    try:
        project_folder, project_name, pio_folder, pio_src, pio_include = get_project_info(args.project_dir)

        logging.info(f"Project folder: {project_folder}")
        logging.info(f"PlatformIO folder: {pio_folder}")
        logging.info(f"PlatformIO src folder: {pio_src}")
        logging.info(f"PlatformIO include folder: {pio_include}\n")

        if not os.path.exists(pio_folder):
            logging.error(f"PlatformIO folder does not exist: {pio_folder}")
            return

        recreate_pio_folders(pio_src, pio_include)
        copy_project_files(project_folder, pio_src, pio_include)
        create_platformio_ini(pio_folder)
        extract_and_comment_defines(pio_folder, pio_include)
        create_header_files(pio_src, pio_include, project_name)
        global_vars = extract_global_vars(pio_src, pio_include, project_name)
        logging.debug(f"Extracted global vars: {global_vars}")
        print_global_vars(global_vars)
        process_ino_files(pio_src, pio_include, project_name, global_vars)

        # Process the main project header file last
        update_project_header(pio_include, project_name)
        main_header_path = os.path.join(pio_include, f"{project_name}.h")
        fix_main_header_file(main_header_path, project_name)

        logging.info("Arduino to PlatformIO conversion completed successfully")

    except Exception as e:
        logging.error(f"An error occurred during conversion: {str(e)}")
        logging.error(traceback.format_exc())
        print(f"An error occurred. Please check the log for details.")


#======================================================================================================
if __name__ == "__main__":
    main()
  
