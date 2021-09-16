# tkinter

为毕业设计的代码添加图形界面


---
### 2021.9.11

#### 已解决
`1.` 图片缩放


`2.` 新增`Text`控件,显示当前视频检测进度


`3.` 新增辅助方法


`4.` 重新整理整体布局


`5.` 图片居中方法

#### 待解决

`1.` 关于文件功能按钮`init`的方法


`2.` 关于文件引入按钮与根据历史记录引入文件按钮逻辑的关系


`3.` 关于视频his的功能写入


`4.` 关于`fdshis` 与 `videohis`二者联系工作

#### 已解决

`1.` 关于文件功能按钮`init`方法
	* 主要实现对文件功能按钮的生成布局

`2.` 关于`fds`文件历史引入按钮以及视频文件历史引入按钮的逻辑关系
	* `video_his_btn`按钮在引入`fds`文件前处于无法选中
	* 当引入`fds`文件后(手动选择 或者 历史引入)后,视频选择按钮与视频历史按钮才被激活

`3.` 完成关于视频`his`的功能
	* 与`fds_his`不同的是:视频`his`在`.txt`文件内列表形式存在
	* 而`fds_his`只存储上一次所使用的`fds`文件组合

`4.` 关于`videohis`与`fdshis`的联系工作也就是两个按钮的逻辑关系


#### 新需求

`1` 对于`fdshis`应存储其历史使用组合,组织形式为:[list1[fdspath1, fdspath2, fdspath3...], list2, list3...]


`2.` 添加页面复原按钮, 在各个时期皆可将页面复原为程序刚启动时页面


### 2021.9.14

#### 已解决

`1.` 时间戳函数与各处时间戳与`his`状态 

`2.` 增加`save_his_auto`函数,存储所有用户存储的组合

`3.` 完成对`fds`与`video`文件路径用户自定义存储

`4.` 完成对界面复原按钮功能,及其后续各控件状态更新

`5.` 针对原本视频检测代码进行改造,目前已能顺利进行视频检测

#### 待解决

`1.` 对原本视频检测代码进行改造

#### 当日晚已解决

`1.` fds运行.bat文件写入

`2.` fds运算结果文件夹父目录 次级目录创建

`3.` 部分杂项功能
---

### 2021.9.15

#### 已解决
`1.` 完成了`fds`文件相关功能

`2.` 串联了视频检测与`fds`文件功能,以及与整个窗体的结合

`3.` 增加了部分附属功能窗口

`4.` 解决了部分控件间数据之间的逻辑关系与交互关系

#### 待解决

`1.` 两个附属图片展示`label`的显示时间关系,与其间涉及到的数据逻辑关系
> 其实该问题不算需要解决的问题,但为了整个窗口的显示美观,考虑将其修正

> 当前问题集中在:需在主体`label`显示的同时将附属`label`展示,并在后续改变其展示内容


---
### 2021.9.16

#### 已解决

`1.` 解决了两个附属`label`在窗口初始化时的显示问题:
> 1. 窗口更新时便显示这两个`label`
> 2. 其图片与主体`label`一致
> 3. 直到背景检测结束后将第一个`label`图片设置为`back`
> 4. 开始视频检测后将第二个`label`图片持续更新为视频检测的结果

`2.` 完成了视频检测与窗口的结合

`3.` 完成了`fds`运行与窗口的组合

`4.` 完成了窗口的整体布置,与各自的显示逻辑


#### 待解决

`1.` 相对路径识别出错

`2.` 帧数设置的相关用户自定义功能
