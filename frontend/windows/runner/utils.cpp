#include "utils.h"

#include <flutter_windows.h>
#include <io.h>
#include <stdio.h>
#include <windows.h>

#include <iostream>
#include <vector>
#include <string>

void CreateAndAttachConsole() {
  if (::AllocConsole()) {
    FILE* unused;
    if (freopen_s(&unused, "CONOUT$", "w", stdout) == 0) {
      _dup2(_fileno(stdout), 1);
    }
    if (freopen_s(&unused, "CONOUT$", "w", stderr) == 0) {
      _dup2(_fileno(stdout), 2);
    }
    std::ios::sync_with_stdio();
    FlutterDesktopResyncOutputStreams();
  }
}

std::vector<std::string> GetCommandLineArguments() {
  // Convert the UTF-16 command line arguments to UTF-8 for the Engine to use.
  int argc;
  wchar_t** argv = ::CommandLineToArgvW(::GetCommandLineW(), &argc);
  if (argv == nullptr) {
    return std::vector<std::string>();
  }

  std::vector<std::string> command_line_arguments;

  // Skip the first argument as it's the binary name.
  for (int i = 1; i < argc; i++) {
    command_line_arguments.push_back(Utf8FromUtf16(argv[i]));
  }

  ::LocalFree(argv);

  return command_line_arguments;
}

std::string Utf8FromUtf16(const wchar_t* utf16_string) {
  if (utf16_string == nullptr) {
    return std::string();
  }

  // Use a safe length check with a max limit (adjustable as needed)
  size_t input_length = wcsnlen_s(utf16_string, 32767);
  if (input_length == 0 || input_length == 32767) {
    return std::string();  // Invalid or too long
  }

  int target_length = ::WideCharToMultiByte(
      CP_UTF8, WC_ERR_INVALID_CHARS, utf16_string,
      static_cast<int>(input_length), nullptr, 0, nullptr, nullptr);

  if (target_length <= 0) {
    return std::string();  // Conversion error
  }

  std::string utf8_string(target_length, 0);
  int converted_length = ::WideCharToMultiByte(
      CP_UTF8, WC_ERR_INVALID_CHARS, utf16_string,
      static_cast<int>(input_length), &utf8_string[0], target_length, nullptr, nullptr);

  if (converted_length == 0) {
    return std::string();  // Conversion error
  }

  return utf8_string;
}

