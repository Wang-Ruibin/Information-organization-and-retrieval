-- 数据库表结构 for 物流服务分面分类系统 (MySQL)

-- 创建数据库（如果不存在）并使用它
CREATE DATABASE IF NOT EXISTS `logistics_db`;
USE `logistics_db`;

-- 设置外键约束检查
SET FOREIGN_KEY_CHECKS=0;

-- 删除已存在的表，以便重新创建
DROP TABLE IF EXISTS `service_facet_values`;
DROP TABLE IF EXISTS `services`;
DROP TABLE IF EXISTS `facet_values`;
DROP TABLE IF EXISTS `facets`;

SET FOREIGN_key_checks=1;

-- 1. 分面定义表 (Facets)
-- 存储分面的基本信息，如“服务类型”、“运输方式”等。
CREATE TABLE `facets` (
    `id` INTEGER NOT NULL AUTO_INCREMENT,
    `name` TEXT NOT NULL, -- 分面的可读名称 (e.g., '服务类型')
    `code` VARCHAR(255) NOT NULL UNIQUE,  -- 用于代码中的标识符 (e.g., 'service_type')
    PRIMARY KEY (`id`)
);

-- 2. 分面值表 (Facet Values)
-- 存储每个分面的具体取值，如“快递”、“陆运”等。
CREATE TABLE `facet_values` (
    `id` INTEGER NOT NULL AUTO_INCREMENT,
    `facet_id` INTEGER NOT NULL, -- 关联到分面定义表
    `value` TEXT NOT NULL,       -- 分面值的具体内容 (e.g., '快递')
    PRIMARY KEY (`id`),
    FOREIGN KEY (`facet_id`) REFERENCES `facets`(`id`) ON DELETE CASCADE
);

-- 3. 物流服务产品表 (Services)
-- 存储作为分类对象的具体物流服务。
CREATE TABLE `services` (
    `id` INTEGER NOT NULL AUTO_INCREMENT,
    `name` TEXT NOT NULL,        -- 服务名称 (e.g., '顺丰标快')
    `description` TEXT,          -- 服务的详细描述
    PRIMARY KEY (`id`)
);

-- 4. 服务-分面值关联表 (Service-Facet Values Junction Table)
-- 这是一个多对多连接表，用于描述每个物流服务产品具体拥有哪些分面属性。
CREATE TABLE `service_facet_values` (
    `service_id` INTEGER NOT NULL,
    `facet_value_id` INTEGER NOT NULL,
    PRIMARY KEY (`service_id`, `facet_value_id`),
    FOREIGN KEY (`service_id`) REFERENCES `services`(`id`) ON DELETE CASCADE,
    FOREIGN KEY (`facet_value_id`) REFERENCES `facet_values`(`id`) ON DELETE CASCADE
);