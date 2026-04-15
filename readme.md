# MyBlog 首次启动说明

## 环境要求

- Python 3.10 及以上
- pip（通常随 Python 一起安装）

---

## 第一步：安装依赖

在项目根目录打开终端，执行：

```bash
# 创建虚拟环境（只需做一次）
python -m venv .venv

# 激活虚拟环境（Windows）
.venv\Scripts\activate

# 安装依赖包
pip install -r requirements.txt
```

---

## 第二步：初始化数据库

```bash
python manage.py migrate
```

执行完毕后，项目根目录会生成 `db.sqlite3` 文件，这就是数据库。

---

## 第三步：创建管理员账号

```bash
python manage.py createsuperuser
```

按提示输入：

```
用户名: admin          ← 自定义
邮箱地址: （可直接回车跳过）
密码: xxxxxxxx         ← 自定义，至少8位
密码（再次输入）: xxxxxxxx
```

> 密码不会显示在屏幕上，直接输入后回车即可。

---

## 第四步：启动服务器

```bash
python manage.py runserver
```

看到以下输出说明启动成功：

```
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

---

## 访问地址

| 页面 | 地址 |
|------|------|
| 博客首页 | http://127.0.0.1:8000/ |
| 后台管理 | http://127.0.0.1:8000/admin/ |

后台使用第三步创建的用户名和密码登录。

---

## 以后每次启动

第二次起只需激活虚拟环境并启动服务器：

```bash
.venv\Scripts\activate
python manage.py runserver
```

---

## 停止服务器

在终端按 `Ctrl + C` 即可。
