import paddle

# Установим девайс
paddle.device.set_device("gpu")

print("Девайс:", paddle.device.get_device())
print("Кол-во GPU:", paddle.device.cuda.device_count())

# Тензор сразу на GPU
x = paddle.ones([2, 3], dtype='float32')
print(x)
print("Тензор находится на:", x.place)
