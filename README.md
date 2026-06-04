# 信息组织与检索 - 课程设计

> 信息组织与检索课程设计

本仓库包含三个课程设计项目，涵盖了 Web 日志分析、分面分类导航系统设计以及静态网页制作。

---

## 项目概览

| 课设 | 名称 | 简介 |
|------|------|------|
| 课设1 | Web 日志解析与分析 | 对服务器访问日志进行解析，提取关键指标并生成可视化图表 |
| 课设2 | 物流服务分面分类导航系统 | 基于分面分类法设计的物流服务查询导航系统 |
| 课设3 | 个人主页与企业主页 | 使用 HTML/CSS 制作的静态网页 |

---

## 课设1：Web 日志解析与分析

对 Apache/Nginx 格式的服务器访问日志进行解析和多维度统计分析。

**功能：**
- 日志字段解析（IP、时间、请求方法、URL、状态码、响应时间等）
- Top 10 活跃 IP 统计
- Top 20 热门页面统计
- HTTP 状态码分布分析
- 按小时访问量分布
- 会话分析（平均会话长度、跳出率）
- 爬虫与真人访问识别
- 响应时间分布分析
- 结果导出为 CSV 和可视化 PNG 图表

**运行方式：**
```bash
cd 课设1
pip install pandas matplotlib
python parse_and_analyze.py
```

**依赖：** Python 3、pandas、matplotlib

---

## 课设2：物流服务分面分类导航系统

为物流行业设计并实现的基于分面分类的小型网站导航系统。用户可通过组合服务类型、运输方式、时效等多维度分面进行精确检索。

**技术栈：**
- 前端：HTML, CSS, JavaScript
- 后端：Node.js, Express.js
- 数据库：MySQL

**运行方式：**
```bash
# 1. 初始化数据库（导入 schema.sql 和 data.sql）
# 2. 启动后端
cd 课设2/backend
npm install
node server.js
# 3. 浏览器打开 frontend/index.html
```

详细说明请参见 [课设2/README.md](课设2/README.md)。

---

## 课设3：个人主页与企业主页

使用纯 HTML/CSS 构建的静态网页，包含个人主页和物流企业介绍页面。

**文件说明：**
- `personal.html` — 个人主页
- `company.html` — 物流企业页面
- `css/` — 样式文件
- `images/` — 图片资源

**运行方式：** 直接在浏览器中打开对应的 HTML 文件即可。

---

## 项目结构

```
.
├── 课设1/                  # Web 日志解析与分析
│   ├── parse_and_analyze.py
│   ├── 课设1数据.log
│   ├── parsed_课设1数据.csv
│   ├── summary_课设1数据.txt
│   └── fig_*.png           # 可视化图表
├── 课设2/                  # 物流服务分面分类导航系统
│   ├── backend/            # Node.js 后端
│   ├── database/           # 数据库脚本
│   └── docs/               # 设计文档
├── 课设3/                  # 静态网页
│   ├── personal.html
│   ├── company.html
│   ├── css/
│   └── images/
└── README.md               # 本文件
```

---
