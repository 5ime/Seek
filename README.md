# Seek - 同IP站点和域名信息查询工具

Seek 是一个可以帮助您自动查找给定IP地址相关的站点和域名信息的工具。

## 功能

Seek具有以下主要功能：

- 同IP站点查询：通过输入IP地址，Seek可以自动获取与该IP地址相关联的所有站点的备案信息。
- 域名备案查询：通过输入域名，Seek可以提供与该域名关联的备案信息。
- 域名权重查询：通过输入域名，Seek可以提供与该域名的权重信息(谷歌PR、百度权重和百度移动权重)。

## 如何使用

要使用Seek，您需要按照以下步骤进行操作：

安装依赖：在您的计算机上安装Python，并确保您已安装所有必需的依赖项。您可以在项目根目录下的 `requirements.txt` 文件中找到所需的依赖项列表。

```
pip install requirements.txt
```

更改token：更换为自己的爱站API token用以查询百度权重信息，获取地址 https://www.aizhan.com/apistore/detail_23/

```python
# utils\utils.py 第16行
TOKEN = "" # 请填写您的爱站接口私钥
```

运行应用程序：使用命令行界面导航到项目根目录，并执行以下命令来启动Seek：

```
python seek.py
```

根据您的需求，输入要查询的文件。Seek将自动检索相关的信息并显示在控制台上，并将结果保存在名为 `results.xlsx` 的文件中。**目前站群判定规则为该IP下存在5个以上的域名**。

```
python seek.py -file <filename>
```

![image](https://github.com/5ime/seek/assets/31686695/60bbe4ce-a59a-4fc0-af98-1e15316cadc7)
