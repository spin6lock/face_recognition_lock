# face_recognition_lock
lock when you walk away from desk

离开工位自动锁屏

定期查询闲置时间，超过10秒后自动人脸识别，没人后自动锁屏。依赖任务计划在解锁时重新运行

### 添加任务计划 
创建任务

常规|触发器|操作
-|-|-
最高权限 选择对应系统win10|添加 工作站解锁时|添加hide.vbs


# ref
* [Lock-Unlock-Laptop](https://github.com/saksham-jain/Lock-Unlock-Laptop-PC-Screen-Using-Face-Recognition)
* [基于opencv tenserflow2.0实战CNN人脸识别锁定与解锁win10屏幕](https://github.com/Yiqingde/Lock-Unlock-Laptop-PC-Screen-Using-Face-Recognition-Opencv-Tensorflow)
