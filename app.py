#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
超大视频自动化切片工具
根据SRT时间戳从大视频中提取片段并拼接成短视频
支持0-100GB大视频文件处理
"""

import os
import sys
import json
import subprocess
import tempfile
import threading
from tkinter import Tk, Label, Button, Entry, Text, Scrollbar, Frame, filedialog, StringVar
from tkinter import ttk


class VideoSlicerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("超大视频自动化切片工具")
        self.root.geometry("900x700")
        self.root.resizable(True, True)
        
        # 全局变量
        self.video_path = StringVar()
        self.output_dir = StringVar()
        self.json_data = StringVar()
        self.log_text = None
        
        # 检查FFmpeg
        self.check_ffmpeg()
        
        # 构建界面
        self.create_ui()
        
        # 设置默认JSON数据
        self.set_default_json()
    
    def check_ffmpeg(self):
        """检查FFmpeg是否安装"""
        try:
            subprocess.run(["ffmpeg", "-version"], capture_output=True, check=True)
            self.ffmpeg_available = True
        except (subprocess.CalledProcessError, FileNotFoundError):
            self.ffmpeg_available = False
    
    def create_ui(self):
        """创建GUI界面"""
        # 主框架
        main_frame = Frame(self.root, padx=20, pady=20)
        main_frame.pack(fill="both", expand=True)
        
        # 1. 原视频选择区
        video_frame = Frame(main_frame)
        video_frame.pack(fill="x", pady=10)
        
        Label(video_frame, text="原视频文件:", font=("微软雅黑", 12)).pack(side="left", padx=5)
        Entry(video_frame, textvariable=self.video_path, width=60, state="readonly").pack(side="left", padx=5)
        Button(video_frame, text="选择文件", command=self.select_video).pack(side="left", padx=5)
        
        # 2. 切片数据输入区
        data_frame = Frame(main_frame)
        data_frame.pack(fill="both", expand=True, pady=10)
        
        Label(data_frame, text="切片数据 (JSON):", font=("微软雅黑", 12)).pack(anchor="w", padx=5)
        
        scrollbar = Scrollbar(data_frame)
        scrollbar.pack(side="right", fill="y")
        
        text_widget = Text(data_frame, height=20, width=100, yscrollcommand=scrollbar.set)
        text_widget.pack(fill="both", expand=True, padx=5)
        scrollbar.config(command=text_widget.yview)
        
        # 绑定变量
        def on_text_change(event):
            self.json_data.set(text_widget.get(1.0, "end-1c"))
        
        text_widget.bind("<<Modified>>", on_text_change)
        self.text_widget = text_widget
        
        # 3. 输出目录设置
        output_frame = Frame(main_frame)
        output_frame.pack(fill="x", pady=10)
        
        Label(output_frame, text="输出目录:", font=("微软雅黑", 12)).pack(side="left", padx=5)
        Entry(output_frame, textvariable=self.output_dir, width=60, state="readonly").pack(side="left", padx=5)
        Button(output_frame, text="选择目录", command=self.select_output_dir).pack(side="left", padx=5)
        
        # 4. 执行与日志区
        execute_frame = Frame(main_frame)
        execute_frame.pack(fill="both", expand=True, pady=10)
        
        Button(execute_frame, text="开始一键批量剪辑", command=self.start_process, 
               font=("微软雅黑", 12, "bold"), bg="#4CAF50", fg="white", padx=20, pady=10).pack(pady=10)
        
        Label(execute_frame, text="执行日志:", font=("微软雅黑", 12)).pack(anchor="w", padx=5)
        
        log_scrollbar = Scrollbar(execute_frame)
        log_scrollbar.pack(side="right", fill="y")
        
        self.log_text = Text(execute_frame, height=10, width=100, yscrollcommand=log_scrollbar.set)
        self.log_text.pack(fill="both", expand=True, padx=5)
        log_scrollbar.config(command=self.log_text.yview)
        
        # 状态标签
        self.status_var = StringVar()
        self.status_var.set("就绪")
        Label(main_frame, textvariable=self.status_var, font=("微软雅黑", 10), fg="blue").pack(anchor="w", pady=5)
    
    def set_default_json(self):
        """设置默认JSON数据"""
        default_json = '''[
  {
    "title": "01_人际关系与痛苦的根源",
    "segments": [
      ["00:19:10,833", "00:19:18,266"],
      ["00:19:28,500", "00:19:38,100"],
      ["00:19:44,033", "00:19:48,966"],
      ["00:19:53,266", "00:19:58,100"],
      ["00:20:01,100", "00:20:06,566"]
    ]
  },
  {
    "title": "02_普通人逆袭的窄门法则",
    "segments": [
      ["00:20:54,433", "00:21:00,100"],
      ["00:21:08,200", "00:21:14,100"],
      ["00:20:29,666", "00:20:32,833"],
      ["00:20:44,466", "00:20:52,033"],
      ["00:20:36,466", "00:20:43,800"],
      ["00:22:04,866", "00:22:16,400"]
    ]
  },
  {
    "title": "03_最高级的销售逻辑",
    "segments": [
      ["00:32:49,700", "00:32:52,900"],
      ["00:33:36,966", "00:33:39,433"],
      ["00:37:46,600", "00:37:48,666"],
      ["00:34:44,566", "00:34:47,433"],
      ["00:35:01,900", "00:35:04,166"],
      ["00:37:50,966", "00:37:54,066"],
      ["00:36:08,966", "00:36:11,166"],
      ["00:36:17,033", "00:36:23,500"]
    ]
  },
  {
    "title": "04_你为什么一直在赚小钱",
    "segments": [
      ["01:35:30,866", "01:35:33,833"],
      ["01:35:38,133", "01:35:41,066"],
      ["01:35:45,266", "01:35:47,733"],
      ["01:35:57,100", "01:36:03,366"],
      ["01:36:08,966", "01:36:14,833"],
      ["01:36:17,733", "01:36:24,700"],
      ["01:36:39,233", "01:36:48,033"],
      ["01:36:57,933", "01:37:01,133"]
    ]
  },
  {
    "title": "05_潜龙勿用的生存破局学",
    "segments": [
      ["00:43:08,600", "00:43:10,800"],
      ["00:43:22,400", "00:43:23,600"],
      ["00:43:31,000", "00:43:40,266"],
      ["00:43:40,266", "00:43:45,600"],
      ["00:43:49,200", "00:43:51,300"],
      ["00:43:52,633", "00:43:58,866"],
      ["00:44:07,866", "00:44:13,800"],
      ["00:44:15,800", "00:44:21,966"],
      ["00:45:05,100", "00:45:11,166"],
      ["00:45:13,166", "00:45:19,500"],
      ["00:45:23,033", "00:45:29,066"]
    ]
  },
  {
    "title": "06_没钱更要有挡不住的自信",
    "segments": [
      ["00:24:26,466", "00:24:34,233"],
      ["00:24:36,033", "00:24:40,766"],
      ["00:24:48,800", "00:24:51,166"],
      ["00:25:10,466", "00:25:19,466"],
      ["00:25:43,800", "00:25:54,200"],
      ["00:25:56,066", "00:26:01,900"]
    ]
  },
  {
    "title": "07_想发财上讲台",
    "segments": [
      ["00:09:11,966", "00:09:17,300"],
      ["00:09:21,700", "00:09:23,900"],
      ["00:09:24,900", "00:09:35,700"],
      ["00:09:35,700", "00:09:37,900"],
      ["00:09:39,066", "00:09:40,366"],
      ["00:09:44,700", "00:09:46,400"],
      ["00:10:32,300", "00:10:38,200"],
      ["01:41:35,466", "01:41:38,366"],
      ["01:41:42,133", "01:41:44,633"]
    ]
  },
  {
    "title": "08_什么是真正的放下",
    "segments": [
      ["00:26:16,100", "00:26:19,766"],
      ["00:26:21,300", "00:26:27,666"],
      ["00:26:27,666", "00:26:30,000"],
      ["00:26:42,833", "00:26:49,566"],
      ["00:26:51,900", "00:26:56,666"],
      ["01:08:33,033", "01:08:38,366"],
      ["01:11:42,766", "01:11:46,666"]
    ]
  },
  {
    "title": "09_用终局思维降维打击",
    "segments": [
      ["02:10:22,033", "02:10:26,533"],
      ["02:10:26,900", "02:10:31,866"],
      ["02:10:38,333", "02:10:42,866"],
      ["02:10:44,466", "02:10:46,866"],
      ["02:12:46,466", "02:12:55,266"],
      ["02:13:03,533", "02:13:04,900"],
      ["02:13:11,100", "02:13:18,900"],
      ["02:39:31,466", "02:39:36,533"]
    ]
  },
  {
    "title": "10_物质在信仰面前一文不值",
    "segments": [
      ["02:01:57,033", "02:02:03,833"],
      ["02:02:15,633", "02:02:20,300"],
      ["02:02:24,233", "02:02:26,300"],
      ["02:03:36,233", "02:03:40,266"],
      ["02:03:52,533", "02:03:54,866"],
      ["02:03:59,433", "02:04:04,666"],
      ["01:55:08,900", "01:55:17,266"],
      ["02:29:38,300", "02:29:42,133"],
      ["02:29:43,666", "02:29:48,900"],
      ["02:29:56,433", "02:30:00,500"]
    ]
  }
]'''
        
        self.text_widget.delete(1.0, "end")
        self.text_widget.insert(1.0, default_json)
        self.json_data.set(default_json)
    
    def select_video(self):
        """选择原视频文件"""
        file_path = filedialog.askopenfilename(
            title="选择原视频文件",
            filetypes=[("视频文件", "*.mp4 *.mov *.avi *.mkv")]
        )
        if file_path:
            self.video_path.set(file_path)
    
    def select_output_dir(self):
        """选择输出目录"""
        dir_path = filedialog.askdirectory(title="选择输出目录")
        if dir_path:
            self.output_dir.set(dir_path)
    
    def start_process(self):
        """开始处理任务"""
        # 检查FFmpeg
        if not self.ffmpeg_available:
            self.log("错误: 未检测到FFmpeg，请先安装FFmpeg并添加到环境变量")
            return
        
        # 检查输入
        if not self.video_path.get():
            self.log("错误: 请选择原视频文件")
            return
        
        if not self.output_dir.get():
            self.log("错误: 请选择输出目录")
            return
        
        if not self.json_data.get():
            self.log("错误: 请输入切片数据")
            return
        
        # 检查视频文件大小
        video_path = self.video_path.get()
        try:
            file_size = os.path.getsize(video_path)
            file_size_gb = file_size / (1024 * 1024 * 1024)
            self.log(f"检测到视频文件大小: {file_size_gb:.2f} GB")
            if file_size_gb > 100:
                self.log("警告: 文件大小超过100GB，处理可能需要较长时间")
        except Exception as e:
            self.log(f"警告: 无法获取文件大小: {e}")
        
        # 检查输出目录是否存在
        output_dir = self.output_dir.get()
        if not os.path.exists(output_dir):
            try:
                os.makedirs(output_dir)
            except Exception as e:
                self.log(f"错误: 创建输出目录失败: {e}")
                return
        
        # 解析JSON数据
        try:
            tasks = json.loads(self.json_data.get())
        except json.JSONDecodeError as e:
            self.log(f"错误: JSON数据解析失败: {e}")
            return
        
        # 在新线程中执行处理
        self.status_var.set("处理中...")
        threading.Thread(target=self.process_tasks, args=(tasks,)).start()
    
    def process_tasks(self, tasks):
        """处理所有任务"""
        video_path = self.video_path.get()
        output_dir = self.output_dir.get()
        
        for i, task in enumerate(tasks, 1):
            title = task.get("title", f"视频{i}")
            segments = task.get("segments", [])
            
            if not segments:
                self.log(f"警告: {title} 没有片段数据，跳过")
                continue
            
            self.log(f"\n开始处理: {title}")
            
            try:
                # 创建临时目录
                with tempfile.TemporaryDirectory() as temp_dir:
                    # 处理每个片段
                    temp_files = []
                    for j, (start_time, end_time) in enumerate(segments, 1):
                        self.log(f"正在提取片段 {j}/{len(segments)}...")
                        
                        # 转换时间格式
                        start_sec = self.time_to_seconds(start_time)
                        end_sec = self.time_to_seconds(end_time)
                        duration = end_sec - start_sec
                        
                        if duration <= 0:
                            self.log(f"警告: 片段 {j} 时间无效，跳过")
                            continue
                        
                        # 生成临时文件名
                        temp_file = os.path.join(temp_dir, f"temp_{j}.mp4")
                        
                        # 执行FFmpeg切片
                        self.extract_segment(video_path, start_sec, duration, temp_file)
                        temp_files.append(temp_file)
                    
                    if not temp_files:
                        self.log(f"警告: {title} 没有有效片段，跳过")
                        continue
                    
                    # 生成concat文件
                    concat_file = os.path.join(temp_dir, "concat_list.txt")
                    self.create_concat_file(temp_files, concat_file)
                    
                    # 拼接视频
                    output_file = os.path.join(output_dir, f"{title}.mp4")
                    self.log(f"正在拼接并导出 {title}...")
                    self.concat_segments(concat_file, output_file)
                    
                    self.log(f"✓ {title} 处理完成")
                    
            except Exception as e:
                self.log(f"错误: 处理 {title} 时出错: {e}")
                continue
        
        self.status_var.set("处理完成")
        self.log("\n所有任务处理完成！")
    
    def time_to_seconds(self, time_str):
        """将SRT时间格式转换为秒"""
        # 格式: 00:19:10,833
        parts = time_str.split(",")
        hms = parts[0].split(":")
        ms = int(parts[1]) if len(parts) > 1 else 0
        
        hours = int(hms[0])
        minutes = int(hms[1])
        seconds = int(hms[2])
        
        total_seconds = hours * 3600 + minutes * 60 + seconds + ms / 1000
        return total_seconds
    
    def extract_segment(self, input_path, start_sec, duration, output_path):
        """使用FFmpeg提取片段"""
        cmd = [
            "ffmpeg",
            "-ss", str(start_sec),  # 必须放在-i前面，确保大文件秒级定位
            "-i", input_path,
            "-t", str(duration),
            "-c:v", "libx264",
            "-c:a", "aac",
            "-preset", "fast",
            "-movflags", "+faststart",  # 优化MP4文件结构，加速播放
            "-threads", "0",  # 使用所有可用线程
            "-y",  # 覆盖输出
            output_path
        ]
        
        subprocess.run(cmd, capture_output=True, check=True)
    
    def create_concat_file(self, files, output_path):
        """创建concat文件"""
        with open(output_path, "w", encoding="utf-8") as f:
            for file in files:
                # 使用相对路径，避免空格和特殊字符问题
                rel_path = os.path.relpath(file, os.path.dirname(output_path))
                rel_path = rel_path.replace("\\", "/")  # 使用正斜杠
                f.write(f"file '{rel_path}'\n")
    
    def concat_segments(self, concat_file, output_path):
        """使用FFmpeg拼接片段"""
        cmd = [
            "ffmpeg",
            "-f", "concat",
            "-safe", "0",
            "-i", concat_file,
            "-c", "copy",
            "-y",  # 覆盖输出
            output_path
        ]
        
        subprocess.run(cmd, capture_output=True, check=True)
    
    def log(self, message):
        """记录日志"""
        if self.log_text:
            self.log_text.insert("end", message + "\n")
            self.log_text.see("end")
            self.root.update_idletasks()


if __name__ == "__main__":
    root = Tk()
    app = VideoSlicerApp(root)
    root.mainloop()
