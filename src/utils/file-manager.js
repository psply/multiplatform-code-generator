import { promises as fs } from 'fs';
import path from 'path';

/**
 * 文件管理器
 * 用于处理文件的创建、写入和目录管理
 */
export class FileManager {
  constructor(baseDirectory) {
    this.baseDirectory = baseDirectory;
  }

  /**
   * 写入文件
   * @param {string} filePath - 相对于基础目录的文件路径
   * @param {string} content - 文件内容
   */
  async writeFile(filePath, content) {
    const fullPath = path.join(this.baseDirectory, filePath);
    const directory = path.dirname(fullPath);
    
    // 确保目录存在
    await this.ensureDirectory(directory);
    
    // 写入文件
    await fs.writeFile(fullPath, content, 'utf8');
  }

  /**
   * 确保目录存在
   * @param {string} directory - 目录路径
   */
  async ensureDirectory(directory) {
    try {
      await fs.access(directory);
    } catch (error) {
      if (error.code === 'ENOENT') {
        await fs.mkdir(directory, { recursive: true });
      } else {
        throw error;
      }
    }
  }

  /**
   * 读取文件
   * @param {string} filePath - 相对于基础目录的文件路径
   * @returns {string} 文件内容
   */
  async readFile(filePath) {
    const fullPath = path.join(this.baseDirectory, filePath);
    return await fs.readFile(fullPath, 'utf8');
  }

  /**
   * 检查文件是否存在
   * @param {string} filePath - 相对于基础目录的文件路径
   * @returns {boolean} 文件是否存在
   */
  async fileExists(filePath) {
    try {
      const fullPath = path.join(this.baseDirectory, filePath);
      await fs.access(fullPath);
      return true;
    } catch {
      return false;
    }
  }

  /**
   * 删除文件
   * @param {string} filePath - 相对于基础目录的文件路径
   */
  async deleteFile(filePath) {
    const fullPath = path.join(this.baseDirectory, filePath);
    await fs.unlink(fullPath);
  }

  /**
   * 列出目录内容
   * @param {string} dirPath - 相对于基础目录的目录路径
   * @returns {Array} 目录内容列表
   */
  async listDirectory(dirPath = '') {
    const fullPath = path.join(this.baseDirectory, dirPath);
    return await fs.readdir(fullPath);
  }

  /**
   * 复制文件
   * @param {string} sourcePath - 源文件路径
   * @param {string} targetPath - 目标文件路径
   */
  async copyFile(sourcePath, targetPath) {
    const sourceFullPath = path.join(this.baseDirectory, sourcePath);
    const targetFullPath = path.join(this.baseDirectory, targetPath);
    const targetDirectory = path.dirname(targetFullPath);
    
    await this.ensureDirectory(targetDirectory);
    await fs.copyFile(sourceFullPath, targetFullPath);
  }

  /**
   * 获取完整路径
   * @param {string} relativePath - 相对路径
   * @returns {string} 完整路径
   */
  getFullPath(relativePath) {
    return path.join(this.baseDirectory, relativePath);
  }
}
