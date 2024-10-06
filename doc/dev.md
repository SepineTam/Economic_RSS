创建一个灵活的爬虫系统，用于追踪多个经济学顶级期刊的研究动态，生成 RSS feed，并提供邮箱订阅功能。系统应具备以下特性：

1. 多期刊支持:
   - 在 ./config/ 目录下为每个期刊创建单独的配置文件(如 ./config/qje.yaml)
   - 配置文件应包含期刊名称、URL、抓取频率、RSS 相关信息等

2. 页面变化检测:
   - 实现一个函数来获取期刊索引页面的内容
   - 开发一个算法来比较当前页面与之前保存的版本，检测是否有更新

3. 数据存储:
   - 为每个期刊创建一个目录来存储历史数据(如 ./data/qje/)
   - 保存每次抓取的页面内容，用于后续比较

4. 更新通知:
   - 当检测到新一期发布时，更新相应的 RSS feed
   - 向订阅该期刊的用户发送邮件通知

5. RSS 生成:
   - 为每个期刊创建和维护一个 RSS feed 文件
   - RSS 文件应位于可公开访问的位置，如 https://academic.sepinetam.com/rss/qje.xml
   - 当检测到新内容时，更新 RSS feed 的内容
   - 包含最新的文章标题、作者、摘要（如果可用）和链接

6. 邮箱订阅功能:
   - 创建一个用户订阅管理系统，存储用户邮箱和订阅的期刊信息
   - 提供一个简单的 Web 界面，允许用户订阅或取消订阅特定期刊
   - 实现邮件发送功能，在检测到更新时向订阅用户发送通知邮件
   - 在邮件中包含新文章的摘要信息和原文链接
   - 提供邮件退订链接，允许用户方便地取消订阅

7. 主程序流程:
   - 读取配置目录中的所有配置文件
   - 对每个期刊执行抓取和比较操作
   - 如有更新，生成或更新相应的 RSS feed
   - 向订阅该期刊的用户发送邮件通知
   - 按照指定的频率定期运行

8. 错误处理:
   - 实现健壮的错误处理机制，处理网络问题、解析错误、邮件发送失败等异常情况

9. 日志记录:
   - 记录每次运行的详细日志，包括抓取时间、结果、RSS 更新情况、邮件发送状态和任何错误

请使用 Python 实现这个系统，并确保代码模块化、易于扩展。使用适当的库来处理 HTTP 请求、HTML 解析、YAML/JSON 配置文件、RSS 生成和邮件发送。

示例配置文件结构(YAML格式):

```yaml
name: Quarterly Journal of Economics
url: https://academic.oup.com/qje
frequency: daily
selector: "#article-list"
rss:
  title: QJE Latest Articles
  description: Latest articles from the Quarterly Journal of Economics
  link: https://academic.sepinetam.com/rss/qje.xml
email:
  subject_template: "New articles in {journal_name}"
  body_template: "New articles have been published in {journal_name}:\n\n{article_list}"
```

请提供以下模块的实现:
1. 主程序
2. 配置解析模块
3. 网页抓取模块
4. 内容比较算法
5. RSS 生成模块
6. 邮件订阅管理模块
7. 邮件发送模块
8. 简单的 Web 界面（用于邮箱订阅管理）
9. 通用工具函数（如日志记录、错误处理等）

对于邮件发送，请使用 Python 的 `smtplib` 库或其他邮件发送库。确保实现邮件模板系统，以便轻松自定义邮件内容。

对于用户订阅管理，考虑使用简单的数据库（如 SQLite）来存储用户信息和订阅偏好。实现基本的安全措施，如邮箱验证和退订认证。

此外，考虑实现限流机制，以防止邮件发送过于频繁，影响服务器性能或触发垃圾邮件过滤器。