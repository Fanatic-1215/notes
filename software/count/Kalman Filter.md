![image-20240519145438394](C:\Users\fan\AppData\Roaming\Typora\typora-user-images\image-20240519145438394.png)

<img src="C:\Users\fan\AppData\Roaming\Typora\typora-user-images\image-20240519155218873.png" alt="image-20240519155218873" style="zoom:50%;" />

~~~c
// 

typedef struct {
    float E_est_last; // 上次估计误差
    float E_est_now; // 当前估计误差
    float E_mea; // 测量误差
    float Data_last_Predict; // 上次估计值
    float Data_Current_Predict; // 当前估计值
    float Data_Curent_Measure; // 当前测量值
    float K; // Kalman增益系数
    
}KalmanFilter;

float Kalman_Init(KalmanFilter * kf,) {
    // 第一步：计算Kalman Gain
    kf->K = kf->E_est_last/(E_est_last +E_mea);
    // 第二步：计算当前估计值
    kf->Data_Current_Predict = kf->K+(kf->Data_Curent_Measure-Data_last_Predict);
    // 第三步：更新E_est
    kf->E_est_now = (1-kf->K)E_est_last
    return ;
}
~~~



~~~c
#include <stdio.h>

// 定义卡尔曼滤波器结构体
typedef struct {
    float Q; // 过程噪声协方差,Q越大滤波器更加依赖于新的测量数据而非模型预测
    float R; // 测量噪声协方差，实际测量值与真实值之间的误差，R越大滤波器会更倾向于信任模型预测而非测量数据
    float x; // 估计值
    float P; // 估计误差协方差，波器对当前状态估计的自信程度的度量，P越大意味着当前的估计值不太可靠
    float K; // 卡尔曼增益，如果K值较大，新的测量值对最终估计的影响更大
} KalmanFilter;

// 初始化卡尔曼滤波器
void KalmanFilter_Init(KalmanFilter *kf, float Q, float R, float initial_value) {
    kf->Q = Q;
    kf->R = R;
    kf->x = initial_value;
    kf->P = 1.0;
    kf->K = 0.0;
}

// 更新卡尔曼滤波器
float KalmanFilter_Update(KalmanFilter *kf, float measurement) {
    // 预测更新
    kf->P = kf->P + kf->Q;

    // 计算卡尔曼增益
    kf->K = kf->P / (kf->P + kf->R);

    // 更新估计值
    kf->x = kf->x + kf->K * (measurement - kf->x);

    // 更新估计误差协方差
    kf->P = (1 - kf->K) * kf->P;

    return kf->x;
}

int main() {
    // 创建并初始化卡尔曼滤波器
    KalmanFilter kf;
    KalmanFilter_Init(&kf, 0.1, 0.1, 0.0);

    // 模拟测量数据
    float measurements[10] = {1.0, 2.0, 3.0, 2.5, 3.5, 3.0, 4.0, 5.0, 4.5, 5.5};

    // 使用卡尔曼滤波器处理测量数据
    for (int i = 0; i < 10; i++) {
        float estimate = KalmanFilter_Update(&kf, measurements[i]);
        printf("Measurement: %f, Estimate: %f\n", measurements[i], estimate);
    }

    return 0;
}
~~~

