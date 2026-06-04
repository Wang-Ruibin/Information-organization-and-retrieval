# 物流服务分面分类导航系统 - 课程设计

本项目是《信息组织与检索》课程的设计成果，旨在为 **物流行业** 设计并实现一个基于分面分类的小型网站导航系统。

## 项目背景

我们选择以 **物流服务查询** 作为应用场景。物流服务具有多维度属性，非常适合通过分面分类进行组织和检索。用户可以通过组合不同的分面（如服务类型、运输方式、时效等）来精确地找到满足其需求的物流解决方案。

## 项目结构

```
.
├── backend/              # 后端服务
│   ├── node_modules/
│   ├── package.json
│   ├── server.js         # Express 服务器
│   └── database.js       # 数据库连接与操作
├── database/             # 数据库文件
│   ├── schema.sql        # 数据库表结构
│   └── data.sql          # 示例数据
├── docs/                 # 设计文档
│   ├── design_document.md  # 分面分类表设计思路
│   └── classification_diagram.md # 分面分类表图示
├── frontend/             # 前端应用
│   ├── index.html        # 页面结构
│   ├── script.js         # 交互逻辑
│   └── style.css         # 页面样式
└── README.md             # 项目说明（本文档）
```

## 技术栈

- **前端**: HTML, CSS, JavaScript (无框架)
- **后端**: Node.js, Express.js
- **数据库**: MySQL

## 系统配置与运行

### 1. 环境准备

- 安装 [Node.js](https://nodejs.org/) (版本 >= 16.x)
- 安装并运行 [MySQL](https://www.mysql.com/) 服务器。

### 2. 初始化数据库

首先，您需要一个有权创建数据库的 MySQL 用户。本项目将使用您提供的凭据（用户: `root`, 密码: `qw12qw12@`）自动创建名为 `logistics_db` 的数据库。

然后，您需要手动将 `database/schema.sql` 和 `database/data.sql` 的内容导入到您的 MySQL 服务器中。您可以使用 MySQL 命令行工具或图形化界面（如 MySQL Workbench）来执行这些脚本。

**使用命令行工具的示例：**

```bash
# 使用您的 root 用户登录 MySQL
mysql -u root -p

# 在 MySQL 提示符下，执行以下命令导入 schema 和 data
# 请确保将 'path/to/your/project' 替换为项目的实际路径
SOURCE path/to/your/project/database/schema.sql;
SOURCE path/to/your/project/database/data.sql;

# 退出 MySQL
EXIT;
```

### 3. 启动后端服务

进入 `backend` 目录，安装依赖并启动服务器。

```bash
cd backend
npm install
node server.js
```

服务器将连接到 MySQL 数据库并启动在 `http://localhost:3000`。

### 4. 访问前端页面

在浏览器中直接打开 `frontend/index.html` 文件即可访问分面导航系统。系统会自动向后端请求数据。