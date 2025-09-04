#!/usr/bin/env python3
"""
Test script for the Multiplatform Code Generator Python version.
"""

import asyncio
import tempfile
import shutil
from pathlib import Path

from src.multiplatform_code_generator.parsers.cpp_parser import CppInterfaceParser
from src.multiplatform_code_generator.generators.android_jni import AndroidJniGenerator
from src.multiplatform_code_generator.generators.ios_oc import IosOcGenerator
from src.multiplatform_code_generator.generators.harmony_napi import HarmonyNapiGenerator
from src.multiplatform_code_generator.utils.file_manager import FileManager


# Test C++ interface
TEST_CPP_INTERFACE = """
namespace MathUtils {
    int add(int a, int b);
    double multiply(double x, double y);
    std::string formatNumber(double value, int precision);
    bool isPositive(double number);
}
"""


async def main():
    """Run the tests."""
    print("🚀 Starting Multiplatform Code Generator Python tests...\n")

    try:
        # Test 1: C++ Parser
        print("📝 Test 1: C++ Interface Parsing")
        parser = CppInterfaceParser()
        parsed = parser.parse(TEST_CPP_INTERFACE)
        
        print("✅ Parsing successful!")
        print(f"   Function: {parsed.function_name}")
        print(f"   Return Type: {parsed.return_type}")
        print(f"   Parameter Count: {len(parsed.parameters)}")
        print(f"   Namespace: {parsed.namespace or 'None'}\n")

        # Create temporary output directory
        with tempfile.TemporaryDirectory() as temp_dir:
            file_manager = FileManager(temp_dir)

            # Test 2: Android JNI Generator
            print("🤖 Test 2: Android JNI Code Generation")
            android_config = {
                "package_name": "com.example.mathutils",
                "class_name": "MathUtils",
                "language": "kotlin"
            }
            android_generator = AndroidJniGenerator(android_config)
            android_files = await android_generator.generate(parsed, file_manager)
            
            print("✅ Android code generation successful!")
            print(f"   Generated files: {len(android_files)}")
            for file in android_files:
                print(f"   - {file}")
            print()

            # Test 3: iOS Objective-C Generator  
            print("🍎 Test 3: iOS Objective-C Code Generation")
            ios_config = {
                "class_prefix": "MU",
                "framework_name": "MathUtils"
            }
            ios_generator = IosOcGenerator(ios_config)
            ios_files = await ios_generator.generate(parsed, file_manager)
            
            print("✅ iOS code generation successful!")
            print(f"   Generated files: {len(ios_files)}")
            for file in ios_files:
                print(f"   - {file}")
            print()

            # Test 4: HarmonyOS NAPI Generator
            print("📱 Test 4: HarmonyOS NAPI Code Generation")
            harmony_config = {
                "module_name": "MathUtils",
                "namespace": "mathutils"
            }
            harmony_generator = HarmonyNapiGenerator(harmony_config)
            harmony_files = await harmony_generator.generate(parsed, file_manager)
            
            print("✅ HarmonyOS code generation successful!")
            print(f"   Generated files: {len(harmony_files)}")
            for file in harmony_files:
                print(f"   - {file}")
            print()

            # Verify generated files
            print("🔍 Verifying generated files...")
            all_files = android_files + ios_files + harmony_files
            verified_count = 0
            
            for file in all_files:
                exists = await file_manager.file_exists(file)
                if exists:
                    content = await file_manager.read_file(file)
                    if content and len(content) > 0:
                        verified_count += 1
                        print(f"   ✅ {file} ({len(content)} characters)")
                    else:
                        print(f"   ⚠️  {file} (empty file)")
                else:
                    print(f"   ❌ {file} (file not found)")

            print(f"\n📊 Test Results:")
            print(f"   Total files: {len(all_files)}")
            print(f"   Verified: {verified_count}")
            print(f"   Success rate: {(verified_count / len(all_files) * 100):.1f}%")

            if verified_count == len(all_files):
                print("\n🎉 All tests passed! Python MCP tool is working correctly.")
            else:
                print("\n⚠️  Some tests failed, please check the error messages.")

            print(f"\n📁 Test files were created in: {temp_dir}")

    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return 1

    return 0


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    exit(exit_code)
