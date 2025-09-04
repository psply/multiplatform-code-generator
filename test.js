#!/usr/bin/env node

/**
 * 简单测试脚本
 * 用于验证 MCP 工具的基本功能
 */

import { CppInterfaceParser } from './src/parsers/cpp-parser.js';
import { AndroidJniGenerator } from './src/generators/android-jni.js';
import { IosOcGenerator } from './src/generators/ios-oc.js';
import { HarmonyNapiGenerator } from './src/generators/harmony-napi.js';
import { FileManager } from './src/utils/file-manager.js';
import { promises as fs } from 'fs';
import path from 'path';

// 测试用的 C++ 接口
const testCppInterface = `
namespace MathUtils {
    int add(int a, int b);
    double multiply(double x, double y);
    std::string formatNumber(double value, int precision);
    bool isPositive(double number);
}
`;

async function runTests() {
    console.log('🚀 开始测试跨平台代码生成器...\n');

    try {
        // 测试 1: C++ 解析器
        console.log('📝 测试 1: C++ 接口解析');
        const parser = new CppInterfaceParser();
        const parsed = parser.parse(testCppInterface);
        
        console.log('✅ 解析成功!');
        console.log(`   函数名: ${parsed.functionName}`);
        console.log(`   返回类型: ${parsed.returnType}`);
        console.log(`   参数数量: ${parsed.parameters.length}`);
        console.log(`   命名空间: ${parsed.namespace || '无'}\n`);

        // 创建临时输出目录
        const tempDir = './test-output';
        await fs.mkdir(tempDir, { recursive: true });
        const fileManager = new FileManager(tempDir);

        // 测试 2: Android JNI 生成器
        console.log('🤖 测试 2: Android JNI 代码生成');
        const androidConfig = {
            package_name: 'com.example.mathutils',
            class_name: 'MathUtils',
            language: 'kotlin'
        };
        const androidGenerator = new AndroidJniGenerator(androidConfig);
        const androidFiles = await androidGenerator.generate(parsed, fileManager);
        
        console.log('✅ Android 代码生成成功!');
        console.log(`   生成文件数: ${androidFiles.length}`);
        androidFiles.forEach(file => console.log(`   - ${file}`));
        console.log();

        // 测试 3: iOS Objective-C 生成器
        console.log('🍎 测试 3: iOS Objective-C 代码生成');
        const iosConfig = {
            class_prefix: 'MU',
            framework_name: 'MathUtils'
        };
        const iosGenerator = new IosOcGenerator(iosConfig);
        const iosFiles = await iosGenerator.generate(parsed, fileManager);
        
        console.log('✅ iOS 代码生成成功!');
        console.log(`   生成文件数: ${iosFiles.length}`);
        iosFiles.forEach(file => console.log(`   - ${file}`));
        console.log();

        // 测试 4: 鸿蒙 NAPI 生成器
        console.log('📱 测试 4: 鸿蒙 NAPI 代码生成');
        const harmonyConfig = {
            module_name: 'MathUtils',
            namespace: 'mathutils'
        };
        const harmonyGenerator = new HarmonyNapiGenerator(harmonyConfig);
        const harmonyFiles = await harmonyGenerator.generate(parsed, fileManager);
        
        console.log('✅ 鸿蒙代码生成成功!');
        console.log(`   生成文件数: ${harmonyFiles.length}`);
        harmonyFiles.forEach(file => console.log(`   - ${file}`));
        console.log();

        // 验证生成的文件
        console.log('🔍 验证生成的文件...');
        const allFiles = [...androidFiles, ...iosFiles, ...harmonyFiles];
        let verifiedCount = 0;
        
        for (const file of allFiles) {
            const exists = await fileManager.fileExists(file);
            if (exists) {
                verifiedCount++;
                const content = await fileManager.readFile(file);
                if (content && content.length > 0) {
                    console.log(`   ✅ ${file} (${content.length} 字符)`);
                } else {
                    console.log(`   ⚠️  ${file} (文件为空)`);
                }
            } else {
                console.log(`   ❌ ${file} (文件不存在)`);
            }
        }

        console.log(`\n📊 测试结果:`);
        console.log(`   总文件数: ${allFiles.length}`);
        console.log(`   验证通过: ${verifiedCount}`);
        console.log(`   成功率: ${((verifiedCount / allFiles.length) * 100).toFixed(1)}%`);

        if (verifiedCount === allFiles.length) {
            console.log('\n🎉 所有测试通过! MCP 工具运行正常。');
        } else {
            console.log('\n⚠️  部分测试失败，请检查错误信息。');
        }

        // 显示输出目录位置
        console.log(`\n📁 生成的文件位于: ${path.resolve(tempDir)}`);

    } catch (error) {
        console.error('❌ 测试失败:', error.message);
        console.error(error.stack);
        process.exit(1);
    }
}

// 运行测试
runTests().catch(error => {
    console.error('💥 测试过程中发生未捕获的错误:', error);
    process.exit(1);
});
