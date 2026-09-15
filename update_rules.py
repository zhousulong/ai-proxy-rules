#!/usr/bin/env python3
"""
一键更新与构建分流规则集脚本
"""
import subprocess
import sys
import time

def run_step(step_name, script_name):
    print(f"\n==========================================", flush=True)
    print(f"▶ 正在执行: {step_name}", flush=True)
    print(f"==========================================", flush=True)
    start = time.time()
    try:
        subprocess.run([sys.executable, "-u", script_name], check=True)
        elapsed = time.time() - start
        print(f"✓ {step_name} 完成 (耗时: {elapsed:.2f}s)", flush=True)
        return True
    except subprocess.CalledProcessError as e:
        elapsed = time.time() - start
        print(f"✗ {step_name} 失败 (退出码: {e.returncode}, 耗时: {elapsed:.2f}s)", flush=True)
        return False

def main():
    start_total = time.time()
    print("🚀 开始自动同步与构建 Loon 第三方 AI 分流规则集...", flush=True)

    # 1. 更新 TLD 列表
    run_step("1. 获取 IANA 官方顶级域名 (TLD)", "fetch_tlds.py")

    # 2. 抓取各开源数据源与导航站
    run_step("2. 抓取外部数据源与导航站首页", "fetch_sources.py")

    # 3. 深度解析重定向与目标真实域名
    run_step("3. 深度解析重定向与目标站点", "crawl_deep.py")

    # 4. 清洗与重新生成规则集
    success = run_step("4. 清洗过滤并构建分流规则列表", "build_rules.py")

    total_time = time.time() - start_total
    if success:
        print(f"\n🎉 规则集构建成功！总耗时: {total_time:.2f}s\n", flush=True)
    else:
        print(f"\n❌ 规则集构建过程中发生错误，请检查日志！总耗时: {total_time:.2f}s\n", flush=True)
        sys.exit(1)

if __name__ == "__main__":
    main()
