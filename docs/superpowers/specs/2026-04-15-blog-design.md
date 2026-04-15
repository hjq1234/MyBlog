# 个人博客网站设计文档

**日期：** 2026-04-15  
**项目：** MyBlog  
**技术栈：** Django + SQLite + django-summernote + Bootstrap 5

---

## 1. 项目概述

纯本地个人博客，供作者自用，不对外开放。支持混合内容（技术笔记、日记随笔、图文内容），通过 Django Admin 后台写作，前台提供舒适的阅读和浏览体验。

---

## 2. 技术选型

| 组件 | 选型 | 说明 |
|---|---|---|
| 后端框架 | Django 4.x | 标准 Django 项目 |
| 数据库 | SQLite | 默认配置，零安装，文件即数据库 |
| 富文本编辑器 | django-summernote | Admin 集成，支持图片直接粘贴/上传 |
| 图片处理 | Pillow | 封面图上传 |
| 前端框架 | Bootstrap 5 (CDN) | 响应式布局，明暗模式 |
| 主题切换 | CSS 变量 + localStorage | 刷新保持用户选择 |

**Python 依赖（requirements.txt）：**
```
django
django-summernote
pillow
```

---

## 3. 项目结构

```
MyBlog/
├── myblog/                  # Django 项目配置包
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── blog/                    # 唯一业务 app
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   ├── templates/
│   │   └── blog/
│   │       ├── base.html        # 公共布局（导航、页脚、明暗切换）
│   │       ├── index.html       # 首页
│   │       ├── post_list.html   # 文章列表
│   │       ├── post_detail.html # 文章详情
│   │       ├── tag_posts.html   # 标签筛选页
│   │       └── search.html      # 搜索结果页
│   └── static/
│       └── blog/
│           ├── css/custom.css   # 明暗模式变量、自定义样式
│           └── js/theme.js      # 主题切换逻辑
├── media/                   # 用户上传图片（封面图、正文图片）
├── manage.py
├── db.sqlite3               # SQLite 数据库文件
└── requirements.txt
```

---

## 4. 数据模型

### Tag（标签）

| 字段 | 类型 | 说明 |
|---|---|---|
| `id` | AutoField | 主键 |
| `name` | CharField(50), unique | 标签名，如"Django"、"日记" |
| `slug` | SlugField(50), unique | URL 友好名，自动由 name 生成 |

### Post（文章）

| 字段 | 类型 | 说明 |
|---|---|---|
| `id` | AutoField | 主键 |
| `title` | CharField(200) | 文章标题 |
| `content` | SummernoteTextField | 富文本正文 |
| `summary` | TextField, blank | 摘要，用于列表页展示；留空则截取正文前 150 字 |
| `cover_image` | ImageField, blank | 封面图，可选 |
| `tags` | ManyToManyField(Tag), blank | 文章标签，可多选 |
| `is_draft` | BooleanField, default=True | True=草稿（不在前台显示），False=已发布 |
| `created_at` | DateTimeField, auto_now_add | 创建时间 |
| `updated_at` | DateTimeField, auto_now | 最后修改时间 |

---

## 5. URL 结构

| URL 路径 | 视图 | 页面说明 |
|---|---|---|
| `/` | `IndexView` | 首页：最近 10 篇已发布文章 + 右侧标签云 |
| `/posts/` | `PostListView` | 文章列表：分页（每页 10 篇）+ 右侧标签筛选 |
| `/posts/<int:pk>/` | `PostDetailView` | 文章详情：全文 + 标签 + 上一篇/下一篇导航 |
| `/tag/<slug:slug>/` | `TagPostsView` | 标签页：该标签下所有已发布文章 |
| `/search/` | `SearchView` | 搜索结果：GET 参数 `?q=`，搜索标题+正文 |
| `/admin/` | Django Admin | 后台管理：写文章、管理标签、上传图片 |

---

## 6. 各页面说明

### 6.1 公共布局（base.html）
- 顶部导航：博客名称（左）、"首页 / 文章 / 搜索框"（右）、明暗模式切换按钮（最右）
- 右侧边栏：标签云（所有标签，按文章数排序）、简短的搜索框
- 页脚：简单版权信息

### 6.2 首页 / 文章列表页
- 文章卡片：封面图（有则显示）、标题、摘要、标签徽章、发布日期
- 分页控件（Bootstrap Pagination）
- 侧边栏标签云：点击标签跳转至标签筛选页

### 6.3 文章详情页
- 大标题 + 发布/更新时间
- 富文本正文（Summernote 输出，含图片）
- 底部标签列表
- 上一篇 / 下一篇文章导航链接

### 6.4 标签筛选页
- 复用文章列表布局
- 顶部显示：「标签：xxx」+ 文章数量
- 支持分页

### 6.5 搜索结果页
- 复用文章列表布局
- 顶部显示：「搜索「xxx」，共找到 N 篇」
- 使用 Django ORM `__icontains` 搜索 `title` 和 `content` 字段
- 结果分页

---

## 7. 明暗模式实现

- Bootstrap 5 的 `data-bs-theme="light" / "dark"` 属性加在 `<html>` 标签
- 自定义 CSS 变量覆盖 Bootstrap 主题色，保证一致性
- `theme.js`：页面加载时读取 `localStorage.getItem('theme')`，切换按钮点击时写入并切换 `<html>` 的 `data-bs-theme`
- 图标：☀️ / 🌙（或 Bootstrap Icons）

---

## 8. Django Admin 配置

- `PostAdmin`：集成 Summernote 编辑器，`list_display` 显示标题、标签、草稿状态、创建时间，支持按标签和草稿状态过滤，支持标题搜索
- `TagAdmin`：`slug` 字段由 `name` 自动生成（`prepopulated_fields`）
- 图片上传：Summernote 内置图片上传，存至 `media/` 目录；封面图通过 `ImageField` 上传

---

## 9. 不在范围内

以下功能明确不做（保持简单）：

- 用户注册/登录（纯自用，只有 Admin 超级用户）
- 评论功能
- RSS 订阅
- 部署配置（Nginx、Gunicorn 等）
- 多语言支持
