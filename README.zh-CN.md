# MidiPainter

**MidiPainter 可以将图片轮廓转换成 MIDI Piano Roll 图案。**

目前该项目还在测试阶段，后续继续完善。

[English README](README.md)

## 效果展示

![UI 效果截图](docs/assets/ui.png)

## 功能

- 导入图片并提取轮廓。
- 将图片轮廓转换为 MIDI 音符。
- 导出 `.mid` 文件，供 DAW 使用。
- 在打开 DAW 前生成 Piano Roll 预览图。
- 生成边缘检测预览图，方便排查图像处理问题。
- 控制音符密度、音域、时间长度、轮廓过滤和图片比例。
- 使用 `contain` 模式保持图片比例，或使用 `stretch` 模式铺满整个 Piano Roll。

## 桌面 MVP

启动桌面应用：

```powershell
python -m midipainter.app
```

当前桌面 MVP 包含：

- 图片选择
- 输入图片预览
- Piano Roll 预览
- MIDI 导出
- 边缘检测预览导出
- 核心转换参数
- 转换统计信息

## 命令行用法

```powershell
python -m midipainter input.png output.mid --preview piano_roll.png --edge-preview edges.png
```

常用参数示例：

```powershell
python -m midipainter input.png output.mid `
  --preview piano_roll.png `
  --edge-preview edges.png `
  --min-pitch 36 `
  --max-pitch 96 `
  --total-beats 64 `
  --note-beats 0.125 `
  --quantize-beats 0.125 `
  --aspect-mode contain `
  --display-aspect 2.012 `
  --min-contour-area 8 `
  --max-contours 512 `
  --simplify-epsilon 1.5 `
  --sample-step 2 `
  --max-notes 5000
```

## 图片比例模式

`contain` 会在 Piano Roll 视图中保持原图比例。竖图会在横向留白，宽图会在纵向留白。这是默认模式。

`stretch` 会铺满完整的时间轴和音域，更充分利用空间，但可能导致图片变形。

`display-aspect` 用于控制 `contain` 模式参考的 Piano Roll 物理宽高比。如果你的 DAW 缩放比例和 MidiPainter 预览不同，可以调整这个值。

## 开发

安装依赖：

```powershell
python -m pip install numpy opencv-python Pillow matplotlib pytest
```

运行测试：

```powershell
python -m pytest
```

运行语法检查：

```powershell
python -m compileall midipainter
```


## 路线图

- 提升 Piano Roll 中的连续线条效果。
- 增加质量预设。
- 增强背景移除和主体分离。
- 支持 SVG 输入。
- 支持多轨道和彩色图片映射。
- 打包 Windows/macOS portable 版本。

详见 [docs/algorithm-backlog.md](docs/algorithm-backlog.md)。

## 状态

MidiPainter 当前处于 MVP 阶段。核心转换管线已经可用，但图像处理质量和视觉效果还会继续优化。
