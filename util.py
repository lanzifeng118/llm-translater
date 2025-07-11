
from AppKit import NSWorkspace

def get_active_app_bundle_id():
    """获取当前活动应用的 Bundle ID"""
    active_app = NSWorkspace.sharedWorkspace().frontmostApplication()
    return active_app.bundleIdentifier()

# 检查是否在微信中
def is_in_wechat():
    # 微信的 Bundle Identifier (macOS 应用唯一标识)
    wechat_bundle_id = "com.tencent.xinWeChat"
    is_wechat = get_active_app_bundle_id() == wechat_bundle_id
    return is_wechat
