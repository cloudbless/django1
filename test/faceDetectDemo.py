import cv2
import requests

# 修改后的图片路径（使用原始字符串避免转义问题）
imgPath = r"D:\shuxx\acm\test\face.jpg"
url = "http://localhost:8080/serviceApp/facedetect/"

# 上传图像并检测
tracker = None  # 若接口不需要tracker参数，可保持None；若需要特定格式可修改
files = {
    "image": ("filename2", open(imgPath, "rb"), "image/jpeg"),
}

try:
    # 发送POST请求
    response = requests.post(url, data=tracker, files=files)
    response.raise_for_status()  # 捕获HTTP请求错误
    req = response.json()
    print("获取信息: {}".format(req))

    # 验证返回结果是否包含人脸数据
    if "#faces" not in req or not req["#faces"]:
        print("未检测到人脸或返回格式异常")
    else:
        # 读取图像并绘制检测框
        img = cv2.imread(imgPath)
        if img is None:
            print(f"错误：无法读取图像文件 {imgPath}")
        else:
            # 注意：通常人脸检测返回的坐标格式是 (x, y, w, h) 或 (x1, y1, x2, y2)
            # 若绘制的框位置不正确，请根据实际返回的坐标格式调整
            for (x1, y1, x2, y2) in req["#faces"]:
                # 确保坐标是整数类型
                x1, y1, x2, y2 = map(int, [x1, y1, x2, y2])
                # 绘制绿色矩形框（厚度2）
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)

            # 显示结果
            cv2.imshow("face detection", img)
            print("按任意键关闭窗口...")
            cv2.waitKey(0)  # 等待按键输入
finally:
    # 确保文件句柄被关闭
    files["image"][1].close()
    # 释放窗口资源
    cv2.destroyAllWindows()